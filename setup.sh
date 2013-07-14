mkdir -p /gravel/system/
useradd --system --uid 502 --gid 1 \
    --create-home --home-dir /gravel/system/gravelmaster \
    gravelmaster

ln -sf $PWD/command.py /usr/local/bin/gravel

echo "gravelmaster ALL = (ALL) NOPASSWD: ALL" > /etc/sudoers.d/gravelmaster
chmod 440 /etc/sudoers.d/gravelmaster
