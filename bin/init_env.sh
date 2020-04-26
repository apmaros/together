#!/bin/bash

## Initialize environment and injects secrets

DAFAULT_DB_HOST='0.0.0.0';
DEFAULT_DB_USER='postgres';
DEFAULT_DB_PASS='password'

echo "`date` Initializing application environment"

# set db host
if [ -z ${DB_HOST+x} ];
then
  DB_HOST_PARAM=${DAFAULT_DB_HOST};
else
 echo "DB_HOST already set to ${DB_HOST}"
 DB_HOST_PARAM=${DB_HOST}
fi

# set db username
if [ -z ${DB_USERNAME_FILE+x} ];
then
  echo "username: secret not found, falling back to default ${DEFAULT_DB_USER} "
  DB_USERNAME_PARAM=${DEFAULT_DB_USER}
else
   DB_USERNAME_PARAM=$(cat ${DB_USERNAME_FILE});
fi

# set db password
if ! [ -z ${DB_PASSWORD_FILE+x} ];
then
  DB_PASSWORD_PARAM=$(cat ${DB_PASSWORD_FILE});
else
  echo "password: secret not found, falling back to default <******>"
  DB_PASSWORD_PARAM=${DEFAULT_DB_PASS}
fi

echo "configuring dev env"
export DB_USERNAME=${DB_USERNAME_PARAM}
export DB_PASSWORD=${DB_PASSWORD_PARAM}
export DB_HOST=${DB_HOST_PARAM}
export DB_PORT=5432
export DB_NAME=together
echo '  √ database configured'

export API_HOST='0.0.0.0'
export API_PORT=4000
echo "  √ API configured"
