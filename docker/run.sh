#!/bin/bash

# Modify these paths and GPU ids
DATA_PATH="/media/jp/T7_opslag1/data/MS3D_data"
CODE_PATH="/home/jp/thesis_ws/MS3D"
GPU_ID="0"
ENVS="  --env=NVIDIA_VISIBLE_DEVICES=$GPU_ID
        --env=CUDA_VISIBLE_DEVICES=$GPU_ID
        --env=NVIDIA_DRIVER_CAPABILITIES=all"
VOLUMES="       --volume=$DATA_PATH:/MS3D/data"
VISUAL="        --env=DISPLAY
                --env=QT_X11_NO_MITSHM=1
                --volume=/tmp/.X11-unix:/tmp/.X11-unix"
                
xhost +local:docker
echo "Running the docker image [GPUS: ${GPU_ID}]"

docker_image="jpsimons95/ms3d_cuda_11.3.1-cudnn8"
container_name="ms3d_cuda113_container"

# Start docker image
docker run -d -it \
	--restart unless-stopped \
	$VOLUMES \
	$ENVS \
	$VISUAL \
	--mount type=bind,source=$CODE_PATH,target=/MS3D \
	--privileged \
	--gpus $GPU_ID \
	--net=host \
	--ipc=host \
	--shm-size=12G \
	--workdir=/MS3D \
	--name=$container_name \
	$docker_image   

# ORIGINAL: shm-size=30G
