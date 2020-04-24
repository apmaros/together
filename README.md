# Together API

## Usage (development)
- reset env
    - `rm -rf ./venv; virtualenv venv; source ./venv/bin/activate; pip install
 -r requirements.txt`
- setup environment `source ./bin/init_dev`
- start API `make run`

### Migrations
Manipulating DB is via Alembic migrations (read [tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to learn more)

Database connection is using environment variables to set the URL. See configuration
 section


## Configuration
Application is using environment variables for all configuration where it can be used.

| name | dev |description |
| ------------- |:-------------:| -----:|
| DB_USERNAME   |  |  |
| DB_HOST       |  |  |
| DB_PORT       |  |  |
| DB_NAME       |  |  |
| API_HOST      | localhost |  |
| API_PORT      | 8080 |  |


## Add dependencies
Be considerate of the dependency libraries pulled to the project. Each of them requires
 maintenance and cost.

0. make sure you are under virtualenv environment
0. install locally `pip install [my-lib]`
0. freeze library to requirements `pip freeze -l > requirements.txt` 


## Contribute Guide
There is an effort to keep the code base consistent and simple. This guide outlines
 few style rules to keep effort of figuring the style to minimum

### Naming conventions
    - file and packege names should be singular - it removes making decision whether
     it is more appropriate using e.g. _model_ - or _models_ package name.
