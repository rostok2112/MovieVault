import subprocess

if __name__ == '__main__':
    try:
        subprocess.run(["pipenv", "run", "makemigrations"])
        subprocess.run(["pipenv", "run", "migrate"])
    except:
        pass