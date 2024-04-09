FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install basics
RUN apt-get update -y \
    && apt-get install build-essential \
    && apt-get install -y apt-utils git curl ca-certificates bzip2 tree htop wget \
    && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev bmon iotop g++ python3.7 python3-dev python3-distutils

# Install cmake v3.13.2
RUN apt-get purge -y cmake && \
    mkdir /root/temp && \
    cd /root/temp && \
    wget https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2.tar.gz && \
    tar -xzvf cmake-3.13.2.tar.gz && \
    cd cmake-3.13.2 && \
    bash ./bootstrap && \
    make && \
    make install && \
    cmake --version && \
    rm -rf /root/temp

# Install python
RUN ln -sv /usr/bin/python3.7 /usr/bin/python
RUN wget https://bootstrap.pypa.io/get-pip.py && \
	python3 get-pip.py && \
	rm get-pip.py

# Install python packages
RUN PIP_INSTALL="python3 -m pip --no-cache-dir install" && \
    $PIP_INSTALL numpy==1.24.4 llvmlite==0.41.1 numba==0.58.1

# Install torch, torchvision & torch-scatter
RUN pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113 && \
    pip install torch-scatter==2.1.0 -f https://data.pyg.org/whl/torch-1.12.1+cu113.html

# Install python packages
RUN PIP_INSTALL="python3 -m pip --no-cache-dir install" && \
    $PIP_INSTALL tensorboardX easydict pyyaml scikit-image tqdm SharedArray six

WORKDIR /root

# Install Boost geometry
RUN wget https://jaist.dl.sourceforge.net/project/boost/boost/1.68.0/boost_1_68_0.tar.gz && \
    tar xzvf boost_1_68_0.tar.gz && \
    cp -r ./boost_1_68_0/boost /usr/include && \
    rm -rf ./boost_1_68_0 && \
    rm -rf ./boost_1_68_0.tar.gz 

# A weired problem that hasn't been solved yet
RUN pip uninstall -y SharedArray && \
    pip install SharedArray

# ADDED BY JP: 
# Dependencie issues
RUN pip install setuptools==65.7.0 \
    ipykernel \
    opencv-python==4.9.0.80 \
    open3d \
    spconv-cu111 \
    kiss-icp[all]
    
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6
    
WORKDIR /MS3D
