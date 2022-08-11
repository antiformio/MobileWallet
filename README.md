## **Usage:**
 - In order to be able to use the api you would need to create a new user on the api:
   - use the endpoint create-user
 - Mostly all the endpoints require authentication, so after creating a user add the headers 'username' and 'password'
   with the correspondant user credentials, to every http request.
 - You should create a wallet for your user, in order to make (and receive) transfers. Create the wallet while 
    authenticated.
 - Only the owner of the wallet can delete it. The authenticated user only has access to its own wallet and transaction
    history. Only the authenticated user can make transactions from his wallet.
 - The transaction is only made if the user has enough balance to support it on his wallet.


# **local dev setup:**
- `pip install -r local-requirements.txt`
- on .env file change the DATABASE_URL to `sqlite:///.mobilewallet.db` (comment out the docker postgres db)

- The project contains an initial migration, but in case of need to change the models delete that migration
- (on alembic/versions/) and run `alembic revision --autogenerate -m "Initial Migration"`

- `alembic upgrade head`
- `python main.py`


# **Docker setup (alternative):**
**Note**:
- **Remember to change the .env variable DATABASE_URL (from postgres to sqlite)**, when switching from dev to docker

- on .env file change the DATABASE_URL 
     to `postgresql+psycopg2://root:password@db:5432/mobilewallet` (comment out the local sqlite db)

Navigate to the root folder of the project and run
- `docker-compose --env-file .env up --build`

#### (optional) apply migrations:

It runs already automaticly as a command per service app definition (on docker-compose). But in case of need:
  `docker-compose run app alembic upgrade head`


## **Pgadmin:**

On browser navigate to [http://127.0.0.1:5050/browser/]((on browser navigate to http://127.0.0.1:5050/browser/))

**username**: `admin@admin.com`
**password**: `admin`

- Add new server:
  - name: `db`
  - in connection:
  - hostname: `db`
    - username: `root`
    - password: `password`

## **Fastapi Documentation:**

On browser navigate to [http://127.0.0.1:8000/docs]( (on browser navigate to http://127.0.0.1:8000/docs))


# Logging Instrumentation:
 - Instrumentation done with Prometheus using starlette-prometheus
 - On the browser, navigate to [http://127.0.0.1:8000/metrics](http://127.0.0.1:8000/metrics) to check the logs.


#TODO:
 - pytests
 - export insomnia collection and add to the project
 - git !!!
