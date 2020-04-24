#!/bin/bash

DAFAULT_DB_HOST='0.0.0.0';

if [ -z ${DB_HOST+x} ];
  then DB_HOST_PARAM=${DAFAULT_DB_HOST};
else
 echo "DB_HOST already set to ${DB_HOST}"
 DB_HOST_PARAM=${DB_HOST}
fi


echo "configuring dev env"
export DB_USERNAME=postgres
export DB_PASSWORD=password
export DB_HOST=${DB_HOST_PARAM}
export DB_PORT=5432
export DB_NAME=together
echo '  √ database configured'

export API_HOST='0.0.0.0'
export API_PORT=4000
echo "  √ API configured"
