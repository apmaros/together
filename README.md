![build and deploy](https://github.com/apmaros/together/workflows/build%20and%20deploy/badge.svg?branch=master)

# Together API

## Usage (development)
There are number of ways to run the application:

1. **run application manually:**<br>
  This option gives more control over application settings. It is required that
   database is listening on default port (see Configuration)
  ```shell script
  # install evironment
  $ source ./bin/install_venv.sh
  # run application
  $ ./bin/run_app.sh
  ```

2. **run docker compose:**<br>
  Run application bundled and configured with database

  ```shell script
  $ docker-compose up -d
  ```

  useful commands to inspect and manage docker-compose:
  ```shell script
    # see logs
    $ docker-compose logs -f api
    # build image
    $ docker-compose build api
    # stop container (or use kill)
    $ docker-compose stop
  ```

### Migrations
Database migrations are handled by Alembic (read [tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to learn more)

Migration is triggered on each application run, or can be manually triggered. It is
 required that the virtual env and environment is configured (See Usage)

```shell script
make migrate
```  

**Author Migration***
New migration is created adding a python file into `./wetogether/api/db/migration
/versions`.

This **should not** be done manually, but by using CLI command:

```shell script
alembic revision -m '<name of the migration>'
```

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
| API_PORT      | 4000 |  |


## Add dependencies
Be considerate of the dependency libraries pulled to the project. Each of them requires
 maintenance and cost.

1. make sure you are under virtualenv environment
1. install locally `pip install <my-lib>`
1. freeze library to requirements `pip freeze -l > requirements.txt` 

## Docker Debug
Based docker image is minimal linux distribution to minimize the size and build time.
This cause running container not having suitable tools for debugging.

To solve this limitation, it is possible to attach a sidecar to the container with
 appropriate tools. Following was specified in slim image [documentation](https://github.com/docker-slim/docker-slim#debugging-minified-containers)

**attach sidecar** 
```shell script
docker run --rm -it --pid=container:node_app_alpine --net=container:node_app_alpine --cap-add sys_admin alpine sh
```

**debug**
  - inspect processees `ps`
  - inspect network `netstat -ltnp`
  - access target container file system `/proc/<target-pi>/root`
    - e.g. `ls /proc/1/root/usr/src/app/`

## Contribute Guide
There is an effort to keep the code base consistent and simple. This guide outlines
 few style rules to keep effort of figuring the style to minimum

### Naming conventions
    - file and packege names should be singular - it removes making decision whether
     it is more appropriate using e.g. _model_ - or _models_ package name.
