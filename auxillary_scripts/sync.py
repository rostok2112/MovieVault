import subprocess

if __name__ == '__main__':
    try:
        subprocess.run(["docker", "compose", "-f", "inventory-compose.yml", "down"])
        subprocess.run(["docker", "compose", "-f", "inventory-compose.yml", "up", "-d"])
        subprocess.run(["pipenv", "sync"]) 
        subprocess.run(["pipenv", "run", "collectstatic", "--no-input"])
        subprocess.run(["pipenv", "run", "migrate"])
    except:
        pass