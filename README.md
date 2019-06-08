# Django Web App
This is a demo app that allows users to view all campgrounds, create new campground and comment on existed campground.
The app is implemented using Django framework

## Installation
1. Install Docker follow the instruction [here](https://docs.docker.com/install/)
2. Install Docker-compose follow the instruction [here](https://docs.docker.com/compose/install/)
3. Create an empty directory and clone the project's source code
```commandline
git clone https://github.com/vtannguyen/DjangoWebApp.git mysite
cd mysite
```
4. Create file .env which hold environment variables' values for django web app and set values for `SECRET_KEY`, `SQL_DATABASE`, `SQL_USER` and `SQL_PASSWORD`
```editorconfig
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=<your_django_app_key>
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=<your_database_name>
SQL_USER=<your_username>
SQL_PASSWORD=<your_password>
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
ALLOWED_HOST=<your_host_name>
```
5. Create file .env.db which hold environment variables' values for database and set values for those variables
```editorconfig
POSTGRES_DB=<your_database_name>
POSTGRES_USER=<your_username>
POSTGRES_PASSWORD=<your_password>
```
**Note** The value of `POSTGRES_DB`, `POSTGRES_USER` and `POSTGRES_PASSWORD` should be 
matched with `SQL_DATABASE`, `SQL_USER` and `SQL_PASSWORD`, respectively.

The project structure now should look like:

    .
    ├── docker-compose.yml
    ├── docker-compose..prod.yml                  
    ├── .env                  
    ├── .env.db                  
    ├── nginx/
    ├── README.md
    └── src/

## Set up environment
### Development
- To build the dev images and spin up the containers:
```commandline
sudo docker-compose -f docker-compose.yml up -d --build
```
- To bring down the dev containers:
```commandline
sudo docker-compose -f docker-compose.yml down -v
```
### Production
- To build the production images and spin up the containers:
```commandline
sudo docker-compose -f docker-compose.prod.yml up -d --build
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
```
- To bring down the production containers:
```commandline
sudo docker-compose -f docker-compose.prod.yml down
```

## Test
### Development
**Note:** Before running test, the docker dev containers should be running already.
- To run test:
```commandline
sudo docker-compose -f docker-compose.yml exec web coverage run --source='.' manage.py test yelpCamp
```
- To get test coverage report:
```commandline
sudo docker-compose -f docker-compose.yml exec web coverage report
```

## Usage
### Development
 -  Access the app at http://127.0.0.1:8000
### Production
 -  Access the app at http://<your_host_name>

