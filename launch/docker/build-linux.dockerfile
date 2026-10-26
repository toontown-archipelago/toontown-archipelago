FROM ubuntu:24.04

ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install runtime and build dependencies for Panda3D, Python 3.11, and Toontown
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
        software-properties-common \
        build-essential \
        bison \
        flex \
        curl \
        git \
        zip \
        pkg-config \
        patchelf \
        libgl1-mesa-dev \
        libopenal-dev \
        libasound2-dev \
        libpulse-dev \
        libx11-dev \
        libxrandr-dev \
        libxcursor-dev \
        libassimp-dev \
        libeigen3-dev \
        libfreetype6-dev \
        libharfbuzz-dev \
        libjpeg-dev \
        libode-dev \
        libpng-dev \
        libsquish-dev \
        libssl-dev \
        libvorbis-dev \
        libvorbisfile3 \
        libtiff-dev && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-venv

# Set up an isolated Python 3.11 virtual environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install nuitka

# Clone and build the Panda3D wheel from source (master branch)
WORKDIR /panda3d-src
RUN git clone --depth 1 https://github.com/toontown-archipelago/panda3d.git . && \
    python makepanda/makepanda.py \
        --wheel \
        --optimize 3 \
        --lzma \
        --threads=$(nproc) \
        --archipelago && \
    pip install panda3d-*.whl && \
    mkdir -p /dist && cp panda3d-*.whl /dist/

# Copy repository
WORKDIR /app
COPY . /app

# Install project Python requirements
RUN pip install -r requirements.txt

CMD ["/bin/bash", "-c", "PYTHON=/opt/venv/bin/python /app/build/compile_linux.sh"]
