bsub -q gpu.legacy -gpu num=1:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test.sh 996"
bsub -q gpu.legacy -gpu num=1:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test.sh 997"
bsub -q gpu.legacy -gpu num=1:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test.sh 998"
bsub -q gpu.legacy -gpu num=1:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test.sh 999"


bsub -q gpu.legacy -gpu num=2:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test_trainingOnly_DDP.sh 996"
bsub -q gpu.legacy -gpu num=2:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test_trainingOnly_DDP.sh 997"
bsub -q gpu.legacy -gpu num=2:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test_trainingOnly_DDP.sh 998"
bsub -q gpu.legacy -gpu num=2:j_exclusive=yes:gmem=1G -L /bin/bash ". /home/isensee/load_env_cluster4.sh && cd /home/isensee/git_repos/nnunet_remake && export nnUNet_keep_files_open=True && . nnunetv2/tests/integration_tests/run_integration_test_trainingOnly_DDP.sh 999"
