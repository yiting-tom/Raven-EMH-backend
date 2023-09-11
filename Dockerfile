FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04
# FROM pengchuanzhang/pytorch:ubuntu20.04_torch1.9-cuda11.3-nccl2.9.9

# Set up the app
RUN mkdir -p /app /data/db && cd /app/
WORKDIR /app
RUN chmod -R a+w /app

# Install common packages and dependencies
RUN export DEBIAN_FRONTEND=noninteractive RUNLEVEL=1 ; \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake git curl wget ca-certificates gnupg libssl-dev vim \
        python3-pip python3-dev python3-wheel \
        libglib2.0-0 libxrender1 python3-soundfile ffmpeg

# Additional setup for nvidia-driver (as in your original Dockerfile)
RUN export DEBIAN_FRONTEND=noninteractive RUNLEVEL=1 ; \
    apt-get install -y --no-install-recommends \
        nvidia-driver-450 mesa-utils

# Install MongoDB
RUN apt-get install -y mongodb

# Remove useless stuff
RUN rm -rf /var/lib/apt/lists/*

# Additional setup for app
RUN mkdir -p /root/.cache/torch/checkpoints && \
    curl -SL -o /root/.cache/torch/checkpoints/s3fd-619a316812.pth "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth"

# clone project
RUN git clone https://github.com/yiting-tom/Raven-EMH-backend.git /app

# Install Python requirements
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

# Copy init script for mongodb
COPY scripts/init_mongodb.sh /usr/local/bin/init_mongodb.sh
RUN chmod +x /usr/local/bin/init_mongodb.sh 

# Create the user
RUN service mongodb start
RUN mongod --repair

# downlaod the model
RUN gdown "https://drive.google.com/uc?id=1ejJUSuMb2v4u9gA7QkcMp8kXaKt0N4gI" -O /app/Wav2Lip/checkpoints/wav2lip.pth

# Entrypoint setup
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# clone project
RUN git pull https://github.com/yiting-tom/Raven-EMH-backend.git
RUN git pull https://github.com/yiting-tom/Raven-EMH-backend.git
RUN git pull https://github.com/yiting-tom/Raven-EMH-backend.git

RUN pip3 install pydantic\[email\]
ENTRYPOINT ["entrypoint.sh"]
