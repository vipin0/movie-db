# Movie Database API using Django REST Framework
A simple movie database API created using Django and Django REST Framework.

## Live Project API

1. [Swagger OpenAPI UI](http://moviedb.dev.vipinyadav.in/)<br>
2. [Redoc API UI](http://moviedb.dev.vipinyadav.in/redoc/)<br>
3. [Browsable API UI](http://moviedb.dev.vipinyadav.in/api/movies/)<br>

## To Run Locally
Clone the repository and navigate to the main directory.

**Install the requirements**
```
pip install -r requirements.txt
```

**Run Migrations**
```python
python manage.py makemigrations
    
python manage.py migrate
```

**Start Development Server**
```
python manage.py runserver
```

## Generate Test Data [ OPTIONAL ]
This is completely optional, however if you want the test data the you can generate by following instructions.

This test data is generated randomly by a custom django management command.

To generate this test data set run the following command
```
python manage.py generate_test_data
```
_This command will create 100 users, 4 Streaming Platforms, 100 Actors, 2000 Movies, and 1500 Reviews._


If this project helps you, don't forget to star the repository.