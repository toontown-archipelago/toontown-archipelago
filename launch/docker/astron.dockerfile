FROM ubuntu:22.04

# Install Astron Dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    cmake \
    build-essential \
    git \
    libboost-dev \
    libyaml-cpp-dev \
    libuv1-dev

# Build Astron
WORKDIR /app/build
RUN git clone https://github.com/Astron/Astron.git .
RUN mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make

# Start Astron
WORKDIR /app/game/astron
ENTRYPOINT [ "/app/build/build/astrond", "config/astrond.yml" ]
