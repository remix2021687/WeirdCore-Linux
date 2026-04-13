import subprocess
import sys

def list_disks():
    try:
        result = subprocess.run(
            ["lsblk", "-d", "-o", "NAME,SIZE,TYPE,MODEL"],
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout)

    except Exception as err:
        print(f"lsblk isn't completed: {err}")
        sys.exit(1)

if __name__ == "__main__":
    list_disks()
