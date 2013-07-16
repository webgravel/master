mkdir -p /gravel/system/master
GHOME=/gravel/system/master/home
useradd --system --uid 502 --gid 1 \
    --create-home --home-dir $GHOME \
    gravelmaster

ln -sf $PWD/command.py /usr/local/bin/gravel

echo "gravelmaster ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/gravelmaster
chmod 440 /etc/sudoers.d/gravelmaster

mkdir -p $GHOME/.ssh

if [ ! -e $HOME/.ssh/id_rsa ]; then
    mkdir $HOME/.ssh
    ssh-keygen -f $HOME/.ssh/id_rsa -N '' || exit 1
fi
