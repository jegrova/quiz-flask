# quiz-flask

Simple web application in Flask, project uses Sql database.

### Serve application with gunicorn


```
gunicorn -w 10 'flask_main:create_app()' -b 0.0.0.0:80
```