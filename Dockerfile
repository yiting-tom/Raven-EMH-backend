FROM python:3.10.12-slim-buster

# Set up the app
RUN mkdir -p /app && cd /app/
WORKDIR /app
RUN chmod -R a+w /app

# Install common packages and dependencies
RUN export DEBIAN_FRONTEND=noninteractive RUNLEVEL=1 ; \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git curl wget ca-certificates gnupg libssl-dev vim \
    python3-pip python3-dev python3-wheel \
    libglib2.0-0 libxrender1 python3-soundfile ffmpeg

# Remove useless stuff
RUN rm -rf /var/lib/apt/lists/*

# clone project
COPY requirements.txt /app/requirements

# Install Python requirements
RUN pip3 install --upgrade setuptools
RUN pip3 install -r /app/requirements.txt
