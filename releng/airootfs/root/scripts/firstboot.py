import os
import subprocess
import time


def run_command(cmd: str):
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"Command: {cmd}")
    except subprocess.CalledProcessError as error:
        print(f"Error command: {cmd} Error: {error}")


print("")
print("=" * 50)
print("System First Boot")
print("=" * 50)
print("")
time.sleep(3)

run_command("fastfetch")

username="wierd"

if os.path.exists(f"/home/{username}"):
    print(f"Copy Hyprland files from {username}")
    run_command(f"cp -r /etc/skel/.config /home/{username}/.config/ 2> /dev/null || true")
    run_command(f"chown -R {username}:{username} /home/{username}/.config")

print("FirstBoot is complitied")
time.sleep(5)

run_command("systemctl enable sddm")
run_command("systemctl start sddm")

with open("/etc/firstboot-done", "w") as f:
    f.write("done")

time.sleep(3)

