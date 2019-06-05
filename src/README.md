# Django Web App
This is a demo app that allows users to view all campgrounds, create new campground and comment on existed campground.
The app is implemented using Django framework

## Getting started
First you'll need to get the source of the project. Do this by cloning the whole repository:
```commandline
# Get the example project code
git clone https://github.com/vtannguyen/DjangoWebApp.git
cd DjangoWebApp/
```
It is good idea (but not required) to create a virtual environment for this project. We'll do this using [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) to keep things simple:
```commandline
# Create a virtualenv in which we can install the dependencies
virtualenv env
source env/bin/activate
```
Now we can install our dependencies:
```commandline
pip install -r requirements.txt
```

Now setup our database. The project uses MySQL as the database. To use another database, please go to [Django Documentation](https://docs.djangoproject.com/en/2.2/intro/tutorial02/) for more information.
* Change the DATABASE setting at mysite/settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_data_base_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
* Start database service
```commandline
/etc/init.d/mysqld start
```
* Run the following commands to finish setting up the database:
```commandline
# Setup the database
python manage.py migrate

# Create an admin user (useful for logging into the admin UI
# at http://127.0.0.1:8000/admin)
python manage.py createsuperuser
```

We can start our server by running:
```commandline
python manage.py runserver
```
Now you can check out the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
