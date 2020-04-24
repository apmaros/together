FROM python:3.8-slim

# setup working directory for container
WORKDIR /usr/src/app
# copy project to the image
COPY . .

# install psql drivers
RUN apt-get update \
  && apt-get install gcc -y \
  && apt-get clean

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose API port
EXPOSE 4000
EXPOSE 5432

CMD [ "/bin/bash", "./bin/run_dev.sh" ]
