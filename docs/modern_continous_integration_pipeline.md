# Modern CI/CD - Application Packaging
_For TLDR, reader can also focus on code snippets and use text as reference._

This post describes a continous integration and deployment pipeline. It aims to be simple and lightweight while robust and scalable. 

Typical pipeline has following steps:

  - package code into docker container
  - publish packaged artefact to a repository
  - deploy artefact to the cluster

Requirements:

  - Docker Engine - v19+

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
