FROM ubuntu:24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       ca-certificates curl zstd \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L --fail --retry 3 \
      https://github.com/leanprover/lean4/releases/download/v4.32.0/lean-4.32.0-linux.tar.zst \
      -o /tmp/lean.tar.zst \
    && tar --zstd -xf /tmp/lean.tar.zst -C /opt \
    && rm /tmp/lean.tar.zst

ENV PATH="/opt/lean-4.32.0-linux/bin:${PATH}"
WORKDIR /src
