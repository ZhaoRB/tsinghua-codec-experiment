FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    bash \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && apt-get clean

SHELL ["/bin/bash", "-c"]

WORKDIR /workspace

CMD ["/bin/bash"]
