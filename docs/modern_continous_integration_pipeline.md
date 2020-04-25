# Modern CI/CD - Application Packaging
_For TLDR, reader can also skip most of the text and focus on code snippets._

In this post I describeA a CI/CD lifecycle. Steps to neccessary for application to:

  - package into docker container
  - publish to the registry
  - deploy to the cluster.

Technologies for the project were chosen with focus on making the process as simple as possible at highest quality.

Requirements:

  - Docker Engine - v19+

## Packaging Application into Docker Image
First step is to package application into single runnable artefact containing application code with all its dependencies. This artefact should be self contained and not have dependencies on host system. Docker is industry standard for packaging code into docker images that can be run as containers.

Application should contain a single `Dockerfile` containing instructions for building the image.

### Anatomy of Dockerfile
This section describes a realistic Dockerfile example containing typical steps in dockerizing application. It is good start, but to fully understand it is useful to read [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

**Base Image - FROM \<image:tag\>**<br>
Most Dockerfiles start with a parent image called base image. Base image is optimise and pre-configure for specific purpose such as python application in this case. Its emphasis is on size and speed of the build.

**Working Directory - WORKDIR \<path\>**<br>
Sets working directory for further instructions such as COPY, RUN, CMD. It is considered as the main directory which will contain source code

**Copy Files from  Repository - COPY . .**<br>
Being in working directory, we copy files from local filesystem into the image.

**Install System Dependencies - RUN apt-get \<packages\>**<br>
Result of docker isolation is that it does not have access to applications and libraries installed on the host system. This is to decouple containers and be able to run them on any host without complicated orchestration. All system dependencies to run the application will be installed in this step.
Docker container is isolated using technology namespaces and uses cgroups to limit access to resources

**Install Application Dependencies - RUN pip install …**<br>
Installs all application dependencies used in the project. It is important that all dependencies are listed in the manifest, otherwis the application will crash in runtime

**Expose Ports - EXPOSE \<port\>**<br>
Informs docker that container listens on specified ports in runtime. It does not advertise these ports. They need to be bind on container startup

**Run Command - CMD [\<command\>, \<param\>, \<other-params\>]**<br>
Defines a command which is executed when application start

```bash
#./Dockerfile
FROM python:3.8-slim

# setup working directory for container
WORKDIR /usr/src/app

# copy project to the image
COPY . .

# install system dependencies
RUN apt-get update \
  && apt-get install gcc -y \ 
  && apt-get clean

# install application dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# expose ports
EXPOSE 4000 

CMD [ "/bin/bash", "./bin/run_dev.sh" ]
```

### Building the Image and Running the Container
Image is built by executing the set of instructions described in `Dockerfile`. It is not necessary to build the image locally. It comes useful during it development for debugging purposes.

**build image**

```
$ docker build . -t apmaros/together:new-image
#> Sending build context to Docker daemon  105.4MB
#> Step 1/8 : FROM python:3.8-slim
#> ---> e8ad3533cb52
#> Step 2/8 : WORKDIR /usr/src/app
```

**list images**

```
$ docker images
#> REPOSITORY          TAG                 IMAGE ID            CREATED              SIZE
#> apmaros/together    new-image           b22efd69b9d0        About a minute ago   477MB
#> together            latest              f82b7525aa94        17 hours ago         477MB
...
```

**run container**
container is image runtime, similar to a object is a instance of class.

```
$ docker run -p "4000:4000" wetogether_webapp
$ curl http://127.0.0.1:4000/statz
#> {"version": "0.0.1"}

```

Note `-p "4000:4000"` is mapping port exposed in `Dockerfile` to docker host port in pattern `"<host-port>:<container-port>"`. Running container is now listening on port `4000`.
