import subprocess

if __name__ == '__main__':
    try:
        subprocess.run(["docker", "compose", "down"])
        subprocess.run(["docker", "compose", "up", "-d"])
    except:
        pass