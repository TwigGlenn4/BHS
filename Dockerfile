# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Set the working directory
WORKDIR /Docker

# Copy the Docker directory to the container
COPY Docker /Docker

# Install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    ninja-build \
    clang \
    systemtap-sdt-dev \
    libbsd-dev \
    linux-libc-dev \
    curl \
    tar \
    grep \
    mawk \
    patchelf \
    libgnustep-base-dev \
    libobjc4 \
    libgnutls28-dev \
    libgcrypt20-dev \
    libxml2-dev \
    libffi-dev \
    libnsl-dev \
    zlib1g-dev \
    libicu-dev \
    libstdc++6 \
    libgcc-9-dev \
    && rm -rf /var/lib/apt/lists/*

# Ensure Docker.sh is executable
RUN chmod +x /Docker/Docker.sh

# Set Docker.sh as the entry point
ENTRYPOINT ["/Docker/Docker.sh"]
