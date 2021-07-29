# Movie Database API using Django REST Framework
A simple movie database API created using Django REST Framework.

##### Live Project API

1.[Swagger OpenAPI UI](https://movie-db04.herokuapp.com/)<br>
2.[Redoc API UI](https://movie-db04.herokuapp.com/redoc/)<br>
3.[Browsable API UI](https://movie-db04.herokuapp.com/api/movies/)<br>

#### To Run Locally
```
    python manage.py makemigrations
    
    python manage.py migrate
    
    python manage.py runserver

```

#### Test Data Set
This Test Data Set is generated randomly by a custom django management command.

To generate this test data set run the following command
```
    python manage.py generate_test_data

```
This will generate 100 users, 4 Streaming Platfors, 100 Actors, 500 Movies, and 1500 Reviews.
