import subprocess
import sys

from scripts.selectdisk.select_disk import select_disk

def run(cmd, description=""):    
    if description:
        print(f"\n[📌 {description}]")
    print(f"→ {cmd}")
    
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"⚠️  {result.stderr.strip()}")
    
    if result.returncode != 0:
        print(f"Command Error")
        sys.exit(1)
    
    print("✓ Успешно")
    return result.stdout.strip()

def main():
    subprocess.run(['clear'], shell=True)
    print("-" * 50)
    print()
    print("Wierd Core Insall Script")
    print()
    print("-" * 50)
    print()

    disk = select_disk()

    efi_part = f"{disk}p1" if "nvme" in disk else f"{disk}1"
    root_part = f"{disk}p2" if "nvme" in disk else f"{disk}2"

    print("Formating disk...")
    run(f"mkfs.fat -F32 {efi_part}")
    run(f"mkfs.btrfs -f -L root {root_part}")

    print("Create btrfs partition...")
    run("mkdir /mnt")
    run(f"mount {root_part} /mnt")
    run(f"btrfs subvolume create /mnt/@")
    run(f"btrfs subvolume create /mnt/@home")
    run(f"umount /mnt")

    print("Install packages...")
    
    packages = [
        "base", "linux-zen", "linux-firmware", "intel-ucode",
        "btrfs-progs", "systemd", "systemd-sysvcompat",
        "hyprland", "waybar", "wofi", "dunst", "hyprlock", "hyprpaper", "hyprshot",
        "grim", "slurp", "kitty", "firefox", "yazi", "fastfetch", "starship", "btop",
        "pipewire", "pipewire-pulse", "wireplumber", "xdg-desktop-portal-hyprland"
    ]

    run(f"pacstrap -K /mnt " + "".join(packages))

    print("Setting system... (fstab, bootloader, users)")
    run("genfstab -U /mnt >> /mnt/etc/fstab")

    chroot_script = f"""
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

    """

    with open("/mnt/root/setup.sh", "w") as f:
        f.write(chroot_script)

    run("chmod +x /mnt/root/setup.sh")
    run("arch-chroot /mnt /root/setup.sh")

    print("Copy configs...")
    run(f"mkdir -p /mnt/home/weird/.config/")
    run(f"cp -r /etc/skel/.config/* /mnt/home/weird/.config/ 2>/dev/null || true")
    run(f"chown -R weird:weird /mnt/home/weird/.config")

    print('Install completed')
    print(f"   DISK {disk}")
    print(f"   USERNAME: weird")
    print(f"   PASSWORD: weird")
    is_reboot = input("Reboot system ? ")

    if is_reboot.lower() == "yes" or is_reboot.lower() == "y":
        run("reboot")
    else:
        sys.exit(1)


    



if __name__ == "__main__":
    main()

