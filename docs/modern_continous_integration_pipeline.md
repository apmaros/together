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

## CI/CD Pipeline
Once application is dockerize, next step is to setup a continues integration server that will build the image at the the right time. Typically, on each PR tests and static analysis is done to ensure code quality. On pushing to `master` branch is code packaged, published and deployed.
As this project is focusing on being lightweight, we will attempt to use [Github Action](https://github.com/features/actions), which promises to _"make it easy to automate all software workflows"_

## Workflow
Workflow is automatize process that will carry on our build. It is configured in `steps`. Steps can be either preconfigured commonly used steps, or manual commands. Because we are using commonly used tools, all the steps will be already defined by community. 
This sections describes key points of typical workflow. More information can be found in [reference documentation](https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions). Building application often requires secrets such as passwords, tokens or encryption keys. They are conveniently handled by [Github Secrets](https://developer.github.com/v3/actions/secrets/).

**Event That Trigger Workflow**<br>

```
on:
  release:
    types: [published]
```

Workflow trigger is defined by activity on Github. It closely follows git events such as `pull_request`, `push`, or `release`. This case sets up `release` to be trigger the build to have better control over deployment. However, it is common practice to deploy upon push to master.

**Checkout Repository**<br>

```
steps:
    - name: checkout repo
      uses: actions/checkout@v2
```

First step is to checkout the repository. The code is required to build the image.

**Build and Push Image**<br>

```
- name: build and push docker image
  uses: elgohr/Publish-Docker-Github-Action@master
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
    name: apmaros/together
    tag: latest
```

After repository is checked out, it can be used to build the image. The process is similar to the one (`docker build . -t ...`) demonstrated in above section.

Build images is then registered to Dockere Hub in repository (repo) under `name` argument. In his case `apmaros/together`. In order to be able to push the image, the repository must exists and user with login `DOCKER_USERNAME` and `DOCKER_PASSWORD` must have access to the repo. Login details are secrets stored in github and names used here e.g. `DOCKER_USERNAME`

**Install SSH Key**<br>

```
- name: install ssh key
  uses: shimataro/ssh-key-action@v2
  with:
    key: ${{ secrets.DOCKER_SSH_PRIVATE_KEY }}
    name: id_rsa # optional
    known_hosts: ${{ secrets.KNOWN_HOSTS }}
```

CI/CD host uses ssh to deploy application to server cluster. This step ensures that ssh connection can be established with remote server. It registers private key and add remote server fingerprint to known hosts.

For security reason, new ssh key pair should be used for deployment. You can follow these steps:

1. create SSH key pair:<br>
  This creates public, private key pair that will be used for SSH communication with remote server. Make sure no passhprase is setup for the key to enable automation. Step used in this workflow requires key to be formatted in legacy format `PEM`.

  ```
  $ ssh-keygen -i PEM -t rsa -b 4096 -C "<email@address.org>”
  ``` 


2. format private key ro PEM format:<br>
  <b>!Warning!</b> This step reformats the key<br>
  This key should be stored in secret `DOCKER_SSH_PRIVATE_KEY`

  ```
  $ ssh-keygen -f <key-location> -m pem -p
  ```

3. add public key to known\_hosts in remote server:<br>
  Use your typical way to ssh to the remote server and add public key created in step 1 to the known\_hosts, typically in `/home/$USER/.ssh/known_hosts`. This will inform remote server to enable traffic for holder of private key corresponding the public key. Ensure that `$HOST` is the same as the one used in the `deploy api` step, for example in case of `deployuser` it would be (`/home/deployuser/.ssh/known_hosts`)
  
4. create `KNOWN_HOSTS` secret:<br>
  To prevent man in the middle attack, it is required to store remote server fingerprint in the local `known_hosts`. Note, this is different from public. There are multiple ways to get the fingerprint, the one I used was to simply copy the one from my laptop which has already registered the remote server after its first ssh access. Format of fingerpring is:
  
  ```
  <IP> <HOST KEY SIGNATURE ALGORITHMS> <FINGERPRINT>
  ```
  for example:
  
  ```
8.8.8.8 ssh-rsa AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
  ```

5. deploy APP
  Executing docker command `stack deploy` application is deployed to server with host stored in `DOCKER_SWARM_HOST`. The host address is using following format:
  
  ```
  ssh://<username>@<ip/hostname>
  ```
  
  for example:
  
  ```
  ssh://deployuser@8.8.8.8
  ```
  
  `stack.yml` provides configuration for deploying containers to Docker Swarm, that will be described in next section
  ```
	- name: deploy api
     run: docker --host ${{ secrets.DOCKER_SWARM_HOST }} stack deploy -c stack.yml together
  ```


Complete file described above:

```
# file: .github/workflows/deploy_image.yml

name: deploy image

on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: check repo
      uses: actions/checkout@v2

    - name: build and push docker image
      uses: elgohr/Publish-Docker-Github-Action@master
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
        name: apmaros/together
        tag: latest

    - name: install ssh key
      uses: shimataro/ssh-key-action@v2
      with:
        key: ${{ secrets.DOCKER_SSH_PRIVATE_KEY }}
        name: id_rsa # optional
        known_hosts: ${{ secrets.KNOWN_HOSTS }}

    - name: deploy api
      run: docker --host ${{ secrets.DOCKER_SWARM_HOST }} stack deploy -c stack.yml together
```
