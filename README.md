# Wall
Wall is a Django project based on DRF to share advertisements.
## Run project on localhost
- In terminal: `git clone https://github.com/amirhamiri/wall`
- cd `/wall` Where the manage.py is
- In terminal: `python -m venv venv`
- activate your venv: in windows `cd venv\scripts\activate` in linux: `venv/bin/activate`
- Run `pip install requirements.txt`
- Run `python manage.py collectstatic`
- Run `python manage.py runserver --settings=wall.settings.dev`
- Visit http://127.0.0.1:8000/swagger to watch the api documentation
## Run project with docker
make sure you`ve installed docker
- In terminal: `git clone https://github.com/amirhamiri/wall`
- cd `/wall` Where the docker-compose.yaml is
- In terminal: `docker-compose up -d`
- Visit http://127.0.0.1:8000/swagger to watch the api documentation
that`s it...