
## Packaging Application into Docker Image
First step is to package application into single runnable artefact containing application code with all its dependencies. In docker the artefact is called **image** and should be self contained and not depend on the host system applications, or libraries. Being self contained makes the image portable to any host and also makes orchestration of the host easier.<br>
Docker is currently considered as standart for packaging applications and is well integrated with most popular orchestration and scheduling tools such as Kubernetes, Marathon, or Nomad. They manage images runtime. Running instance of image is called container, similarly to object being called initiated class.

In order to create a image, docker requires a set of instructions. These instructions are typically in file called `Dockerfile` placed in the root of application.

### Anatomy of Dockerfile
This section describes a realistic Dockerfile example containing typical steps in dockerizing application. You can learn more in the [reference documentation](https://docs.docker.com/engine/reference/builder/)

**Base Image - FROM \<image:tag\>**<br>
Most Dockerfiles start with a parent image called base image. Base image is optimised and pre-configure for specific purpose such as python application in this case. Its emphasis is on size and speed of the build. Thats why it is usually desired to be contain only essntial tools.

Itamar Turner-Trauring wrote good [article](https://pythonspeed.com/articles/base-image-python-docker-images/) advocating for the base image I chose in the end.

**Working Directory - WORKDIR \<path\>**<br>
Sets working directory that is considered to be the main directory which will contain the source code. Further instructions such as `COPY`, `RUN`, `CMD` will be executed from this directory.

**Copy Files from  Repository - COPY . .**<br>
Being in working directory, we copy files from local filesystem into the image. In this case it is whole content of the folder, however often it can be only source code with configuration file.

**Install System Dependencies - RUN apt-get \<packages\>**<br>
Result of docker isolation is that it does not have access to applications and libraries installed on the host system. This is to decouple containers and be able to run them on any host without complicated orchestration. All system dependencies to run the application will be installed in this step.
Docker container is isolated using technology namespaces and uses cgroups to limit access to resources

**Install Application Dependencies - RUN pip install …**<br>
Installs all application dependencies used in the project. It is important that all dependencies are listed in the manifest, otherwise they will be missing and the application will fail in runtime

**Expose Ports - EXPOSE \<port\>**<br>
Informs docker that container listens on specified ports in runtime. It does not advertise these ports. They need to be bind on container startup

**Run Command - CMD [\<command\>, \<param\>, \<other-params\>]**<br>
Defines a command which is executed when application start

Here is a full version of `Dockerfile` explained above:

```bash
# file ./Dockerfile
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
Image is built by executing the set of instructions described in `Dockerfile`. It is not necessary to build the image locally. Sometimes during its development, it might however be useful to debug either build process or the container itself.

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

**run container**<br>
Some of the frequent issues are caused by misconfigured environment, or networking issues. Here are few commands that can help to resolve them

```
# run container
$ docker run -p "4000:4000" wetogether_webapp
$ curl http://127.0.0.1:4000/statz
#> {"version": "0.0.1"}

```

Note `-p "4000:4000"` is mapping port exposed in `Dockerfile` to docker host port in pattern `"<host-port>:<container-port>"`. Running container is now listening on port `4000`.

**attach sidecar**<br>
Container has its own system and environment and often it is useful to access it from inside. However, because it is running minimalistic version to save space and build time it does not have almost any tooling. For this purpose we can attach another container with more rich environment.

```
docker run --rm -it --pid=container:<running_container> --net=container:<running_container> --cap-add sys_admin alpine sh
debug
```

Here are some useful commands to:
  - inspect processees `ps`
  - inspect network `netstat -ltnp`
  - access target container file system `/proc/<target-pi>/root`
    - e.g. ls /proc/1/root/usr/src/app/

