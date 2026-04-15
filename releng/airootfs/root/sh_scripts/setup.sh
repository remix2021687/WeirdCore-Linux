#!/bin/bash

set -e

ln -sf /usr/share/zoneinfo/Europe/Prague /etc/localtime

hwlock --systohc

echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
local-gen

echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "weirdcore" > /etc/hostname

useradd -m -G wheel,audio,video,storage weird
echo "weird:weird" | chpasswd
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/weird

bootctl --path=/boot install

cat > /boot/loader/loader.conf << EOC
defualt weirdcore
timout 3
EOC

cat > /boot/loader/entries/wierdcore.conf << EOC
title   WierdCore Linux
linux   /vmlinuz-linux-zen
initrd  /intel-ucode.img
initrd  /initramfs-linux-zen.img
options root=UUID=$(blkid -s UUID -o value {root_part}) rootflags=subvol=@ rw
EOC

mkinitcpio -P

