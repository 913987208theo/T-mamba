
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import os 
import cv2
from skimage import measure
import shutil
from matplotlib.patches import Rectangle, ConnectionPatch


def load_npy(npy_path):
    """Load a .npy file containing a 3D array."""
    data = np.load(npy_path)
    return data

def load_nii(file_path):
    # Load the image file
    img = nib.load(file_path)
    # Convert image data to a numpy array
    data = img.get_fdata()
    return data

def move_files(original_dir, seg_dir, model_name="Ours"):
    # Construct the directory path where the files will be moved
    save_dir = os.path.join(seg_dir, model_name)
    # Ensure the directory exists, if not create it
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Gather all files ending with '_segmentation.npy'
    original_files = [f for f in os.listdir(original_dir) if f.endswith('_segmentation.npy')]
        
    # Move these files to the save directory
    for _file in original_files:
        original_file_path = os.path.join(original_dir, _file)
        save_file_path = os.path.join(save_dir, _file)
        shutil.move(original_file_path, save_file_path)
        print(f"Moved {_file} to {save_dir}")
        
def compute_mse(y_true, y_pred):
    """Compute Mean Squared Error between two images."""
    return np.mean((y_true - y_pred) ** 2)

def visualize_slices(data, slice_indices, axis ,cols=3):
    """
    Visualize multiple slices from a 3D array using subplots.
    
    Parameters:
    - data: The 3D numpy array from which slices will be taken.
    - slice_indices: A list of integers indicating the slice indices to visualize.
    - cols: Number of columns in the subplot grid.
    """
    # Calculate the number of rows needed based on the number of columns and number of slices
    rows = (len(slice_indices) + cols - 1) // cols
    
    plt.figure(figsize=(cols * 5, rows * 5))  # Adjust the size as needed
    
    for i, slice_index in enumerate(slice_indices):
        if slice_index < data.shape[axis]:
            ax = plt.subplot(rows, cols, i + 1)
            if axis == 0:
                ax.imshow(data[slice_index, :, :], cmap='gray')
            elif axis == 1:
                ax.imshow(data[:, slice_index, :], cmap='gray')
            elif axis ==2:
                ax.imshow(data[:, :, slice_index], cmap='gray')
                
            ax.title.set_text(f'Slice {slice_index}, axis={axis}')
            ax.axis('off')  # Hide axes ticks
        else:
            print(f"Slice index {slice_index} out of range.")
    
    plt.tight_layout()
    plt.show()


def visualize_slice(data, slice_index, axis=0):
    # Check which axis is specified for slicing
    if axis == 0:
        slice_data = data[slice_index, :, :]
    elif axis == 1:
        slice_data = data[:, slice_index, :]
    elif axis == 2:
        slice_data = data[:, :, slice_index]
    else:
        raise ValueError("Invalid axis for slicing. Use 0, 1, or 2.")

    # Plotting the slice
    plt.imshow(slice_data, cmap='gray')
    plt.title(f'Slice {slice_index} along axis {axis}')
    plt.axis('off')  # Hide axes ticks
    
    base_save_path = "/root/work_dir/Result/test/tmp"
    os.makedirs(base_save_path, exist_ok=True)
    plt.savefig(os.path.join(base_save_path, "vs.png"))
    plt.close()



def visualize_all_data(model_names, original_dir, label_dir, seg_dir, output_dir):   #no rotation
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List all NIfTI files in the original path
    original_files = [f for f in os.listdir(original_dir) if f.endswith('.nii.gz')]

    for file_name in original_files:
        print(file_name)
        # Load original and label images
        original_image = nib.load(os.path.join(original_dir, file_name)).get_fdata()
        label_image = nib.load(os.path.join(label_dir, file_name)).get_fdata()

        # Convert label image to binary for clear black and white visualization
        label_image = (label_image > 0).astype(int)

        slice_idx = original_image.shape[2] // 2  # Middle slice index

        # Prepare subplot layout
        num_models = len(model_names)
        fig, axes = plt.subplots(1, 2 + num_models, figsize=(5 * (2 + num_models), 5))

        # Display original image
        axes[0].imshow(np.rot90(original_image[:, :, slice_idx],-1), cmap='gray')
        axes[0].set_title('Original Image')
        axes[0].axis('off')

        # Display label image
        axes[1].imshow(np.rot90(label_image[:, :, slice_idx],-1), cmap='gray')
        axes[1].set_title('Label Image')
        axes[1].axis('off')

        # Load and display each model's segmented image
        for i, model_name in enumerate(model_names):
            seg_path = os.path.join(seg_dir, model_name, file_name.replace('.nii.gz', '_segmentation.npy'))

            if os.path.exists(seg_path):
                segmentation_image = load_npy(seg_path)
                axes[i + 2].imshow(np.rot90(segmentation_image[:, :, slice_idx],-1), cmap='gray')
                axes[i + 2].set_title(f'{model_name} Segmented')
                axes[i + 2].axis('off')
            else:
                print("loading failed for:", seg_path)
                axes[i + 2].set_visible(False)

        # Save the full comparison image
        plt.tight_layout()
        save_path = os.path.join(output_dir, f'comparison_{file_name}.png')
        print(f"saving visualization of {file_name} to {save_path}")
        plt.savefig(save_path)
        plt.close()
        
def visualize_all_data_single_fig(model_names, original_dir, label_dir, seg_dir, output_dir, slice_offset):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)  # Adjusted variable name to 'output_dir'
    
    # List all NIfTI files in the original directory
    original_files = [f for f in os.listdir(original_dir) if f.endswith('.nii.gz')]
    
    # Determine the number of rows needed in the subplot for all samples
    num_models = len(model_names)
    num_files = len(original_files)
    num_cols = 2 + num_models  # Columns for original, label, and each model
    
    # Create a figure to contain all subplots
    fig_all, axes_all = plt.subplots(num_files, num_cols, figsize=(5 * num_cols, 5 * num_files), squeeze=False)
    
    for idx, file_name in enumerate(original_files):
        # Load original and label images
        original_image = nib.load(os.path.join(original_dir, file_name)).get_fdata()
        label_image = nib.load(os.path.join(label_dir, file_name)).get_fdata()
         # Convert label image to binary for clear black and white visualization
        label_image = (label_image > 0).astype(int)
        
        middle_slice = original_image.shape[2] // 2  # Middle slice index
        slice_idx = middle_slice + slice_offset  # Adjusted slice index based on the offset

        # Display original and label images
        axes_all[idx, 0].imshow(np.rot90(original_image[:, :, slice_idx], -1), cmap='gray')
        axes_all[idx, 0].set_title('Original Image')
        axes_all[idx, 0].axis('off')

        axes_all[idx, 1].imshow(np.rot90(label_image[:, :, slice_idx], -1), cmap='gray')
        axes_all[idx, 1].set_title('Label Image')
        axes_all[idx, 1].axis('off')

        # Load and display each model's segmented image
        for i, model_name in enumerate(model_names):
            seg_path = os.path.join(seg_dir, model_name, file_name.replace('.nii.gz', '_segmentation.npy'))
        
            if os.path.exists(seg_path):
                segmentation_image = load_npy(seg_path)
                axes_all[idx, i + 2].imshow(np.rot90(segmentation_image[:, :, slice_idx], -1), cmap='gray')
                axes_all[idx, i + 2].set_title(f'{model_name} Segmented')
                axes_all[idx, i + 2].axis('off')
            else:
                print("loading failed for:", seg_path)
                axes_all[idx, i + 2].set_visible(False)
    
    # Save the full comparison image for all samples
    plt.tight_layout()
    all_samples_path = os.path.join(output_dir, f'all_samples_comparison_offset_{slice_offset}.png')
    plt.savefig(all_samples_path)
    plt.close(fig_all)
    print(f"Saved all samples visualization to {all_samples_path}")
        

def place_rectangle_and_enlarge(image, rect=None):
    if rect is None:
        return image, "None", "None"  # No rectangle provided, return the image unchanged.
    
    # Example of rect: (x, y, width, height)
    rect_patch = Rectangle((rect[0], rect[1]), rect[2], rect[3], linewidth=2, edgecolor='r', facecolor='none')

    # Crop the region of interest from the image
    cropped_region = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    
    # Calculate position for the enlarged rectangle at the bottom right of the image
    enlarged_rect = (
        image.shape[1] - rect[2] * 2 - 10,  # Double the size for enlargement and position
        image.shape[0] - rect[3] * 2 - 10,
        rect[2] * 2,  # Double width
        rect[3] * 2   # Double height
    )
    # Resize the cropped region to fill the enlarged rectangle
    enlarged_region = cv2.resize(cropped_region, (enlarged_rect[2], enlarged_rect[3]), interpolation=cv2.INTER_LINEAR)
    
    # Place the enlarged region into a copy of the original image (for display purposes only)
    image_with_enlarged = np.copy(image)
    image_with_enlarged[enlarged_rect[1]:enlarged_rect[1]+enlarged_rect[3], enlarged_rect[0]:enlarged_rect[0]+enlarged_rect[2]] = enlarged_region
    
    enlarged_patch = Rectangle((enlarged_rect[0], enlarged_rect[1]), enlarged_rect[2], enlarged_rect[3], 
                               linewidth=2, edgecolor='yellow', facecolor='none')
    
    # Create a connection line between the centers of the original and enlarged rectangles
    connection_line = ConnectionPatch(
        xyA=((rect[0] + rect[2]/2), (rect[1] + rect[3]/2)),
        xyB=((enlarged_rect[0] + enlarged_rect[2]/2), (enlarged_rect[1] + enlarged_rect[3]/2)),
        coordsA="data", coordsB="data",
        arrowstyle="-", color="blue", linewidth=2)

    return image_with_enlarged, rect_patch, enlarged_patch, connection_line

def visualize_all_models_comprehensive(model_names, original_dir, label_dir, seg_dir, output_dir, top_k):
    model_dirs = {model_name: os.path.join(seg_dir, model_name) for model_name in model_names}
    os.makedirs(output_dir, exist_ok=True)
    top_k_results = topk_difference_mse_data(label_dir, model_dirs, top_k)
    print(f"Top results: {top_k_results}")

    num_rows = len(top_k_results)
    num_cols = 2 + len(model_names)

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 5, num_rows * 5))

    for idx, (file_name, slice_idx, mse) in enumerate(top_k_results):
        original_image = nib.load(os.path.join(original_dir, file_name)).get_fdata()
        label_image = nib.load(os.path.join(label_dir, file_name)).get_fdata()
        
        label_image = (label_image > 0).astype(int)
        rect = (50, 50, 100, 100)  # Placeholder rectangle

        original_slice = np.rot90(original_image[:, :, slice_idx],-1)
        label_slice, rect_patch, enlarged_patch, connection_line = place_rectangle_and_enlarge(np.rot90(label_image[:, :, slice_idx],-1), rect)

        axes[idx, 0].imshow(original_slice, cmap='gray')
        axes[idx, 0].set_title(f'Original: {file_name}')
        axes[idx, 0].axis('off')

        axes[idx, 1].imshow(label_slice, cmap='gray')
        axes[idx, 1].add_patch(rect_patch)
        axes[idx, 1].add_patch(enlarged_patch)
        axes[idx, 1].add_artist(connection_line)
        axes[idx, 1].set_title('Label Image')
        axes[idx, 1].axis('off')

        for m_idx, model_name in enumerate(model_names):
            seg_path = os.path.join(model_dirs[model_name], file_name.replace('.nii.gz', '_segmentation.npy'))
            if os.path.exists(seg_path):
                segmentation_image = load_npy(seg_path)
                segmentation_slice, _, _, _ = place_rectangle_and_enlarge(np.rot90(segmentation_image[:, :, slice_idx],-1), rect)
                axes[idx, m_idx + 2].imshow(segmentation_slice, cmap='gray')
                axes[idx, m_idx + 2].set_title(f'{model_name} Segmented')
                axes[idx, m_idx + 2].axis('off')
            else:
                print(f"Loading failed for: {seg_path}")
                axes[idx, m_idx + 2].set_visible(False)

    plt.tight_layout()
    save_path = os.path.join(output_dir, f'comprehensive_comparison_{top_k}.png')
    plt.savefig(save_path)
    plt.close()
    print(f"Saved comprehensive visualization of top {top_k} data to {save_path}")
    save_path =os.path.join(output_dir, f'top{top_k}_result.txt')
    print(f"Saved top {top_k} result to {save_path}")
    with open(save_path,"w") as file:
        file.write("Filename, Slice ,MSE\n")
        for filename, slice, mse in top_k_results:
            file.write(f"{filename}, {slice}, {mse}\n")
    

def topk_difference_mse_data(label_path, model_dirs, top_k):
    """Calculate the top k MSE differences for label vs. segmented images from various models.
    
    Args:
        label_path (str): Path to the directory containing label images.
        model_dirs (dict): Dictionary of model names and their respective directories containing segmented images.
        top_k (int): Number of top results to return based on MSE differences.
        
    Returns:
        list: Sorted list of tuples containing file name, slice index, and MSE difference.
    """
    label_files = sorted(f for f in os.listdir(label_path) if f.endswith('.nii.gz'))
    mse_differences = []

    for file_name in label_files:
        label_file_path = os.path.join(label_path, file_name)
        label_image = load_nii(label_file_path)
        
        label_image = (label_image > 0).astype(int)

        # Focusing on slices around the middle of the volume
        middle_index = label_image.shape[2] // 2
        slice_indices = range(max(middle_index - 3, 0), min(middle_index + 4, label_image.shape[2]))

        for slice_idx in slice_indices:
            label_slice = label_image[:, :, slice_idx]
            slice_mse_models = {}

            for model_name, model_path in model_dirs.items():
                segmented_file_path = os.path.join(model_path, file_name.replace('.nii.gz', '_segmentation.npy'))
                if os.path.exists(segmented_file_path):
                    segmented_image = load_npy(segmented_file_path)[:, :, slice_idx]
                    mse = compute_mse(label_slice, segmented_image)
                    slice_mse_models[model_name] = mse
                else:
                    print(f"Path does not exist: {segmented_file_path}")
                    continue

            # Normalize MSE and calculate differences
            if slice_mse_models:
                min_mse = min(slice_mse_models.values())
                max_mse = max(slice_mse_models.values())
                mse_range = max_mse - min_mse
                if mse_range > 0:
                    normalized_mse = {k: (v - min_mse) / mse_range for k, v in slice_mse_models.items()}
                    if 'Ours' in normalized_mse:
                        our_mse = normalized_mse['Ours']
                        other_mses = sum(v for k, v in normalized_mse.items() if k != 'Ours')
                        mse_difference = other_mses - our_mse
                        mse_differences.append((file_name, slice_idx, mse_difference))

    # Return top k results with the highest differences where 'Ours' performed better
    return sorted(mse_differences, key=lambda x: x[2], reverse=True)[:top_k]

def main():
    # Example usage:
    slice_offsets = [-3,-2,0,1,2,3]  # Example slice indices

    model_names =  ['Ours','nnFormer', 'DenseVNet', 'PMFSNet','SwinUNETR']  
   
    original_dir, label_dir, seg_dir, output_dir= '/root/work_dir/PMFSNet/datasets/NC-release-data-checked/valid/images','/root/work_dir/PMFSNet/datasets/NC-release-data-checked/valid/labels', '/root/work_dir/Result/test','/root/work_dir/Result/test/result'
    #visualize_all_data(model_names, original_dir, label_dir, seg_dir, output_dir)         #Middle index, all fig for every sample saved to save_dir
    #for slice_offset in slice_offsets:
        #visualize_all_data_single_fig(model_names, original_dir, label_dir,seg_dir, output_dir,slice_offset=slice_offset) #slice index offset, all sample in single fig  saved to save_dir
    visualize_all_models_comprehensive(model_names, original_dir, label_dir,seg_dir, output_dir,top_k=15)
    


main()