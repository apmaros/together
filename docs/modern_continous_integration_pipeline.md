# Modern Continous Integration Pipeline
_For TLDR, reader can also focus on code snippets and use text as reference._

This post describes a continous integration and deployment pipeline. It aims to be simple and lightweight while robust and scalable. 

Typical pipeline has following steps:

  - package code into docker container
  - publish packaged artefact to a repository
  - deploy artefact to the cluster

Requirements:

  - Docker Engine - v19+

## CI/CD Pipeline
Once application is dockerised, next step is to setup a continues integration server
 that will build the image at desired time. Typically, on each PR tests and static analysis is done to ensure code quality. To keep deployment as small as possible, the ideal option would be to deploy server on each push to `master` branch. After push, the code is packaged, image is publiched to repository and deployed to production server. 

As this project is focusing on being lightweight, we will attempt to use [Github Action](https://github.com/features/actions), which promises to _"make it easy to automate all software workflows"_

## Workflow
The build is defined by its workflow. Workflow is automatize process that will carry on our build. It is configured in `steps`. Steps can be either preconfigured commonly used steps, or manual shell commands. Because we are using commonly used tools, all the steps will be already defined by community. 

This sections describes key points of typical workflow. More information can be found in [reference documentation](https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions). Building application often requires secrets such as passwords, tokens or encryption keys. They are conveniently handled by [Github Secrets](https://developer.github.com/v3/actions/secrets/).

**Workflow Trigger**<br>

```
on:
  push:
    branches: [ master ]
```

Trigger is a activity which starts executing the build - executing the workflow steps. It is typicall defined by activity on Github, but also by webhook, time based trigger, or other. Full list and events can be found in [documentation](https://help.github.com/en/actions/reference/events-that-trigger-workflows).

**Checkout Repository**<br>

```
steps:
    - name: checkout repo
      uses: actions/checkout@v2
```

First step is to checkout the repository to build host machine.

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

After repository is checked out, it can be used to build the image. The process is similar to the one (`docker build . -t <image_name>) demonstrated in Part I.

Build images is then registered to Dockere Hub in a repository (under `name` argument. In his case `apmaros/together`. In order to be able to push the image, the repository must exists and user with login `DOCKER_USERNAME` and `DOCKER_PASSWORD` must have access to the repo. Login details are secrets stored in github and names used here e.g. `DOCKER_USERNAME`.

For security reason, it is recommended to use a new registration and separate account for build process. It is important to keep in mind that if image in the repository is compromised, it can be then run to production and compromise system.

**Install SSH Key**<br>

```
- name: install ssh key
  uses: shimataro/ssh-key-action@v2
  with:
    key: ${{ secrets.DOCKER_SSH_PRIVATE_KEY }}
    name: id_rsa # optional
    known_hosts: ${{ secrets.KNOWN_HOSTS }}
```

CI/CD host uses ssh to deploy application to server cluster. This step ensures that ssh connection can be established with remote server. It registers private key and adds remote server fingerprint to known hosts.

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

3. add public key to `known_hosts` in remote server:<br>
  Use your typical way to ssh to the remote server and add public key created in step 1 to the `known_hosts`, typically in `/home/$USER/.ssh/known_hosts`. This will inform remote server to enable traffic for holder of private key corresponding the public key. Ensure that `$HOST` is the same as the one used in the `deploy api` step, for example in case of `deployuser` it would be (`/home/deployuser/.ssh/known_hosts`)
  
4. create `KNOWN_HOSTS` secret:<br>
  To prevent [man in the middle attack](https://www.ssh.com/attack/man-in-the-middle), it is required to store remote server fingerprint in the local `known_hosts`. Note, this is different from public key. There are multiple ways to get the fingerprint, the one I used was to simply copy the one from my laptop which has already registered the remote server after its first ssh access. Format of fingerpring is:
  
  ```
  <IP> <HOST KEY SIGNATURE ALGORITHMS> <FINGERPRINT>
  ```
  for example:
  
  ```
8.8.8.8 ssh-rsa AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
  ```
 
**Deploy APP**<br>

```
- name: deploy api
- run: docker --host ${{ secrets.DOCKER_SWARM_HOST }} stack deploy -c stack.yml together
```

This is the only manual step in this build. There is no reliable plugin for deploying swarm application. It is also not necessary as Docker Swarm is expected to be used via API.

Executing docker command `stack deploy` application is deployed to server with host stored in `DOCKER_SWARM_HOST`. The host address is using following format:
  
```
ssh://<username>@<ip/hostname>
```
  
for example:
  
```
ssh://deployuser@8.8.8.8
```

`stack.yml` provides image name and runtime configuration for running container. It also provides information about scaling the application and what to do 

provides configuration for deploying containers to Docker Swarm, that will be described in next section.


Possible failures are:

- permission denied and message `Permission denied (publickey).` or similar, make ensure that SSH key is installed properly in previous step.

- connection is established, but deployment failed for other reason, it migt be useful to debug this deployment locally with debug logs by adding flag `--log-level debug`



Here is full version of deploy image that was explained in the post

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