# MOVIE VAULT 

Welcome to repository with test web application for [Bond ua](https://bond.ua/) COMPANY! 🔥🔥🔥

---

## Sections

- [Installation  of necessary tools](#tools-and-installation)
- [Development process in docker](#development-with-docker)
- [Development process in docker](#development-without-docker)
- [Shortcuts](#shortcuts)
- [Useful commands](#additional-commands)

---

## Tools and installation

Install Docker (for linux):

```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt install docker-ce
sudo systemctl status docker
sudo usermod -aG docker ${USER}
su - ${USER}
```

Or install Docker Desktop: [Installation instruction](https://docs.docker.com/desktop/install/windows-install/)

Copy and paste values of .env.example file to .env file and edit it for your purposes:

```bash
cat .env.example > .env
```

---

## Development with Docker

Start application:

```bash
docker compose up -d
```

Open in browser: [Site](http://localhost:8005/)

Or write in adress line `localhost:<port>/` where <port> is a value of PORT in .env

For creating super user (Account with unlimited rights on admin panel):

```bash
docker exec -it free_vpn python manage.py  createsuperuser
```

After any changes in models create and apply migrations:

```bash
docker exec free_vpn  python manage.py makemigrations
docker exec free_vpn  python manage.py migrate
```

---

## Development without Docker

Install python:

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt install python-is-python3
sudo apt install python3-pip
python -m pip install --upgrade pip
```

Install pipenv:

```bash
pip install --user pipenv
```

Sync dependencies:

```bash
pipenv sync
```

Run important inventory :

```bash
docker compose -f inventory-compose.yml up -d
```

Sync migrations:

```bash
pipenv run python manage.py migrate
```

Collect static filest to static/ directory:

```bash
pipenv run python manage.py collectstatic
```

Create super user (Account with unlimited rights on admin panel):

```bash
pipenv run python manage.py createsuperuser
```

Run app for development purposes:

```bash
pipenv run python manage.py runserver 8005
```

After any changes in models create and apply migrations:

```bash
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

---

## Shortcuts

### Docker

Sync after pull changes:
```bash
pipenv run deploy
```

### Without docker 

Sync after pull changes:
```bash
pipenv run sync
```

Run necessary inventory:
```bash
pipenv run inventory
```
Run application (specify port if its necessary):
```bash
pipenv run serve
```

Collect static:
```bash
pipenv run python manage.py collectstatic
```

Sync migrations:
```bash
pipenv run migrate
```

Create migrations:
```bash
pipenv run makemigrations
```

Create migrations and migrate:
```bash
pipenv run migrations
```

---

## Additional commands

Delete build cache:
```bash
docker builder prune -af
```

Delete all containers and flash all trash:

```bash
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker container prune -f
```

Delete all images:

```bash
docker image rm $(docker image ls -q) && docker image prune -af
```
