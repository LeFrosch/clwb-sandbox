#!/bin/bash

set -e

# get arguments
IDE_BIN=$1
VERSION=$2

# get plugins to install
shift 2
PLUGINS=$(echo "$@")

if [[ $(arch) == "arm64" ]]; then
  ARCH_SUFFIX="-aarch64"
else 
  ARCH_SUFFIX=""
fi

case ${IDE_BIN} in
  "idea")
    IDE_NAME=IntelliJ
    URL="https://download.jetbrains.com/idea/ideaIU-$VERSION$ARCH_SUFFIX.tar.gz"
    ;;
  "clion")
    IDE_NAME=CLion
    URL="https://download.jetbrains.com/cpp/CLion-$VERSION$ARCH_SUFFIX.tar.gz"
    ;;
  *)
    echo "unsupported IDE: ${IDE_BIN}"
    exit 1
    ;;
esac

DIRECTORY=/opt/jetbrains/${IDE_BIN}-${VERSION}

# download the installation package
mkdir -p $DIRECTORY 
curl -sL $URL | tar -xz --strip-components=1 -C $DIRECTORY

# install the plugins for the abc user
su abc -c "$DIRECTORY/bin/$IDE_BIN installPlugins https://plugins.jetbrains.com/plugin $PLUGINS"
su abc -c "$DIRECTORY/bin/remote-dev-server registerBackendLocationForGateway"
su abc -c "$DIRECTORY/bin/remote-dev-server installPlugins https://plugins.jetbrains.com/plugin $PLUGINS"

# install the .desktop file
cat > "/usr/share/applications/$IDE_BIN-$VERSION.desktop" << EOF
[Desktop Entry]
Version=$VERSION
Type=Application
Name=$IDE_NAME ($VERSION)
Icon=$DIRECTORY/bin/$IDE_BIN.png
Exec=$DIRECTORY/bin/$IDE_BIN %f
EOF

# update alternative for the IDE
update-alternatives --install "/usr/local/bin/$IDE_BIN" "$IDE_BIN" "/opt/jetbrains/$IDE_BIN-$VERSION/bin/$IDE_BIN" 1
