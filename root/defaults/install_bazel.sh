#!/bin/bash

set -e

if [[ $(arch) == "arm64" ]]; then
  ARCH_SUFFIX="arm64"
else 
  ARCH_SUFFIX="amd64"
fi

curl -sL "https://github.com/bazelbuild/bazelisk/releases/download/v1.27.0/bazelisk-linux-$ARCH_SUFFIX" > /usr/local/bin/bazelisk
chmod +x /usr/local/bin/bazelisk

# update alternative for bazel 
update-alternatives --install /usr/local/bin/bazel bazel /usr/local/bin/bazelisk 1
