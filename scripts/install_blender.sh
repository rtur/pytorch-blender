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

echo "export PATH=${CACHE}/${NAME}:${PATH}" > ENVS
