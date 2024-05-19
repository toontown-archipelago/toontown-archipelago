FROM ubuntu:22.04
WORKDIR /app

# Install Python
ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update
RUN apt-get install -y python3.11 python3-pip

# Install Panda dependencies
RUN apt-get install -y \
    libassimp-dev \
    libeigen3-dev \
    libgl1-mesa-dev \
    libharfbuzz-dev \
    libjpeg-dev \
    libode-dev \
    libpng-dev \
    libsquish-dev \
    libssl-dev

# Install game dependencies \
COPY requirements.txt .
RUN python3.11 -m pip install -r requirements.txt
RUN python3.11 -m pip install "https://github.com/toontown-archipelago/panda3d/releases/latest/download/panda3d-1.11.0-cp311-cp311-linux_x86_64.whl"

# Start the server
ENTRYPOINT ["python3.11", "-m", "launch.launcher.launch"]
