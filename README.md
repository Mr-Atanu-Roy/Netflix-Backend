
## Features

- Authentication which includes user-regisration, login, email-verification, reset-password, otp-generation
- Json Web Token(JWT) authentication also enabled
- User watchlist
- User Review
- User Profile
- Retrive Movie details, trailer details
- Retrive Cast and genres details
## Tech Stack

**Client Side:** HTML, SCSS, TailwindCSS

**Server Side:** Django, Django Rest Framework (DRF)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DEBUG = TRUE`

`SECRET_KEY = 'django-insecure-lcu2s1v)m50-l#$mpapl3cx!=jwj=(i9=^67-)kipy1^-d!2sn`

### For sending emails
`EMAIL_HOST_USER = 'email address from which email will be send'`

`EMAIL_HOST_PASSWORD = 'its app password'`

Note : You have to create app password for the email you are using in `EMAIL_HOST_USER` and put it in `EMAIL_HOST_PASSWORD`
## Installation

Create a folder and open terminal and install this project by
command 
```bash
git clone https://github.com/Mr-Atanu-Roy/Netflix-Backend

```
or simply download this project from https://github.com/Mr-Atanu-Roy/Netflix-Backend

In project directory Create a virtual environment(say env)

```bash
  virtualenv env

```
Activate the virtual environment

For windows:
```bash
  env\Script\activate

```
Install dependencies
```bash
  pip install -r requirements.txt

```
To migrate the database run migrations commands
```bash
  py manage.py makemigrations
  py manage.py migrate

```

Create a super user
```bash
  py manage.py createsuperuser

```
Then add some data into database


To run the project in your localserver
```bash
  py manage.py runserver

```
## API Documentations

To read the api documentaion of this API visit

#### Swagger Docs
`http://127.0.0.1:8000/netflix/api/swagger/`

#### ReDocs Docs
`http://127.0.0.1:8000/netflix/api/redoc/`

## Postman API Collection
You can also export the [postman api collection](https://github.com/Mr-Atanu-Roy/Netflix-Backend/blob/master/Netflix%20API.postman_collection.json) and import in postman.

## Author

- [@Mr-Atanu-Roy](https://www.github.com/Mr-Atanu-Roy)