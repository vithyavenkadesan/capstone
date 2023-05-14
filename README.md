# Casting Agency

Render Link: https://capstonefinal-deployment.onrender.com

While running locally: http://localhost:5000

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Set up the Database

With Postgres running, create a `castingagency` database:

```bash
CREATE DATABASE castingagency;
```

Populate the database using the `casting_agency.psql` file provided. From the `database` folder in terminal run:

```bash
psql castingagency < casting_agency.psql
```

## Running the server

From within the `./starter` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

To run the server, execute:

```bash
python app.py
```

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actors`
   - `get:actor-detail`
   - `get:movies`
   - `get:movie-detail`
   - `post:actors`
   - `patch:actors`
   - `delete:actors`
   - `post:movies`
   - `patch:movies`
   - `delete:movies`

6. Create new roles for:
   - Casting Assistant
     - can `get:actors`
     - can `get:actor-detail`
     - can `get:movies`
     - can `get:movie-detail`
   - Casting Director
     - can `get:actors`
     - can `get:actor-detail`
     - can `get:movies`
     - can `get:movie-detail`
     - can `post:actors`
     - can `patch:actors`
     - can `delete:actors`
     - can `patch:movies`
   - Casting Producer
     - can perform all actions


7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the Casting Assistant role to one and Director role to the other and Producer role to the third one.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter/udacity-fsnd-castingagency.postman_collection.json`
   - Right-clicking the collection folder for Assistant and Director and Producer, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors

### API Documentation 

`GET '/actors'`

- Fetches the actors from database
- Request Arguments: None
- Returns: actors and its attributes`.

```json
{
    "actors": [
        {
            "id": 2,
            "name": "Kamal"
        },
        {
            "id": 3,
            "name": "Jothika"
        },
        {
            "id": 4,
            "name": "Trisha"
        }
    ],
    "success": true
}


```


`GET '/movies'`

- Fetches all movies from database.
- Request Arguments: None
- Returns: movies and its attributes.

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 28 Sep 2023 00:00:00 GMT",
            "title": "Kabali"
        },
        {
            "id": 2,
            "release_date": "Fri, 28 Apr 2023 00:00:00 GMT",
            "title": "Vikram"
        }
    ],
    "success": true
}

```

`GET '/actors/${actor_id}'`

- Fetches detailed actor information
- Request Arguments: actor_id integer value
- Returns: detailed actor information

```json
{
    "actor": {
        "date_of_birth": "September 28, 1987",
        "gender": "Male",
        "name": "Karthi"
    },
    "success": true
}

```

`GET '/movies/${movie_id}'`

- Fetches detailed movie information
- Request Arguments: movie_id integer value
- Returns: detailed movie information

```json
{
    "movie": {
        "cast": [
            "Kamal",
            "Trisha"
        ],
        "release_date": "Fri, 28 Apr 2023 00:00:00 GMT",
        "title": "Vikram"
    },
    "success": true
}

```

`DELETE '/actors/${actor_id}'`

- Deletes a actor using the id
- Request Arguments: actor_id integer value
- Returns: Success code along with deleted id

```json
{
    "delete": "6",
    "success": true
}

```

`DELETE '/movies/${movie_id}'`

- Deletes a movie using the id
- Request Arguments: movie_id integer value
- Returns: Success code along with deleted id

```json
{
    "delete": "6",
    "success": true
}

```

`POST '/actors'`

- Create actor info
- Request Body:
```json
    {
    "name" : "Surya",
    "gender": "Male",
    "dob": "1989-09-28"
    }

```
- Returns: created response

```json
{
    "actors": [
        {
            "date_of_birth": "September 28, 1989",
            "gender": "Male",
            "name": "Surya"
        }
    ],
    "success": true
}

```

`POST '/movies'`

- Create movie info
- Request Body:
```json
   {
    "title" :"1947",
    "release_date": "2023-04-28"
   }

```
- Returns: created response

```json
{
    "movies": [
        {
            "cast": [],
            "release_date": "Fri, 28 Apr 2023 00:00:00 GMT",
            "title": "1947"
        }
    ],
    "success": true
}

```

`PATCH '/actors/2'`

- Update actor info
- Request Body:
```json
    {
    
    "dob": "1989-09-28"
    }

```
- Returns: updated response

```json
{
    "actors": [
        {
            "date_of_birth": "September 28, 1989",
            "gender": "Male",
            "name": "Surya"
        }
    ],
    "success": true
}

```

`PATCH '/movies/2'`

- Update movie info
- Request Body:
```json
   {
    "release_date": "2023-04-28"
   }

```
- Returns: updated response

```json
{
    "movies": [
        {
            "cast": [],
            "release_date": "Fri, 28 Apr 2023 00:00:00 GMT",
            "title": "1947"
        }
    ],
    "success": true
}



```


