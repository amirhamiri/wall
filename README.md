# Wall
## a real world open source example of django-rest-framework (DRF)
### some features:
- Compliance with the principles of test writing DRF
- Compliance with the principles of clean coding
- Dockerized
- Using the nginx web server
- Documented and visualized by Swagger
#### Wall is a Django project based on DRF to share advertisements
#### If you want to get a good understanding of API and DRF, fork the project and participate in its development.
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