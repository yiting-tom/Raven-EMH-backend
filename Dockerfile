FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

# Set up the workspace
WORKDIR /workspace
RUN chmod -R a+w /workspace

# Install common packages and dependencies
RUN export DEBIAN_FRONTEND=noninteractive RUNLEVEL=1 ; \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake git curl ca-certificates gnupg \
        libssl-dev \
        vim \
        python3-pip python3-dev python3-wheel \
        libglib2.0-0 libxrender1 python3-soundfile \
        ffmpeg && \

# Additional setup for nvidia-driver (as in your original Dockerfile)
RUN export DEBIAN_FRONTEND=noninteractive RUNLEVEL=1 ; \
    apt-get install -y --no-install-recommends \
        nvidia-driver-450 mesa-utils

# Install MongoDB
RUN apt-get install -y mongodb

# Remove useless stuff
RUN rm -rf /var/lib/apt/lists/*


# Install Python requirements
RUN pip3 install --upgrade setuptools
RUN pip3 install torch torchvision python-dotenv firebase_admin fastapi uvicorn pymongo loguru openai boto3 pydantic\[email\] librosa numpy opencv-contrib-python opencv-python tqdm numba

# Additional setup for your app (as in your original Dockerfile)
RUN mkdir -p /root/.cache/torch/checkpoints && \
    curl -SL -o /root/.cache/torch/checkpoints/s3fd-619a316812.pth "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth"

# Copy init script for mongodb
COPY scripts/init_mongodb.sh /usr/local/bin/init_mongodb.sh
RUN chmod +x /usr/local/bin/init_mongodb.sh && bash /usr/local/bin/init_mongodb.sh

# Final setup
RUN mkdir /workspace/src && cd /workspace/src/
WORKDIR /workspace/src
ENTRYPOINT ["make dev"]
