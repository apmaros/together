![build and deploy](https://github.com/apmaros/together/workflows/build%20and%20deploy/badge.svg?branch=master)

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
| API_PORT      | 4000 |  |


## Add dependencies
Be considerate of the dependency libraries pulled to the project. Each of them requires
 maintenance and cost.

1. make sure you are under virtualenv environment
1. install locally `pip install [my-lib]`
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
  - access target container file system `/proc/[target-pid]/root`
    - e.g. `ls /proc/1/root/usr/src/app/`

## Contribute Guide
There is an effort to keep the code base consistent and simple. This guide outlines
 few style rules to keep effort of figuring the style to minimum

### Naming conventions
    - file and packege names should be singular - it removes making decision whether
     it is more appropriate using e.g. _model_ - or _models_ package name.
