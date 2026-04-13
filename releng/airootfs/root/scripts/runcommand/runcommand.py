import subprocess
import sys

def runcommand(cmd: str, check=True):
    print(f"-> {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0 and check:
        print(f"Error Command: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()


if __name__ == "__main__":
    runcommand()
