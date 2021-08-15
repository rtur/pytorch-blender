set -e

NAME="blender-2.91.2-linux64"
NAMETAR="${NAME}.tar.xz"
CACHE="${HOME}/pytorch-blender"
TAR="${CACHE}/${NAMETAR}"
URL="https://mirror.clarkson.edu/blender/release/Blender2.91/${NAMETAR}"

echo "Installing Blender ${NAME}"
mkdir -p $CACHE
if [ ! -f $TAR ]; then
    wget -O $TAR $URL
fi
tar -xf $TAR -C $CACHE

BLENDER_PATH=${CACHE}/${NAME}
BLENDER_BIN=${BLENDER_PATH}/blender
echo "Installed Blender into:"
echo "${BLENDER_PATH}"
