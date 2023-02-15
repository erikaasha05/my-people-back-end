<h1 align="center">My People back-end</h1>
<p>My People was created for my Ada Developers Academy's Capstone project. This web app helps you organize your contacts. Users can add contacts, view contact information, and set reminders for important dates, and search for contacts by name. This repo is the back-end for My People.</p>

  
# About The Project

## Features

* Endpoints for:
  * Getting a list of contacts
  * Getting a list of reminders
  * Creating a contact
  * Creating a reminder
  * Creating a user
  * Deleting a contact
  * Deleting a reminder
  * User authentication (login/logout)

## Built With

* Flask
* PostgreSQL (database)

## Dependencies

* Flask
* flask_jwt_extended
* datetime

## Setup

To get a local copy, fork and clone this repo. 

Create a virtual environment:

```
$ python3 -m venv venv
$ source venv/bin/activate
```
Install dependences:
```
(venv) $ pip install -r requirements.txt
```

## Set Up the Database

Create a database named `my_people_development`.

## Create `.env` File

Create a file named `.env`.

Add the following environment variables to your `.env` file:
```
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/my_people_development
```
Since the `flask-JWT-extended` package is used for user authentication, also include the following in your `.env` file.
```
JWT_SECRET_KEY=CHANGE THIS KEY
```
Replace `CHANGE THIS KEY` with your own key.

## Run `$ flask db upgrade`

Run `$ flask db upgrade` to get your database to the current migration.

## Run `$ flask run`

To begin the local Flask server, run `$ flask run` to enable development mode.

<!-- MARKDOWN LINKS & IMAGES -->
