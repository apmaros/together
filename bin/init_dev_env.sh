#!/bin/sh

echo "configuring dev env"
export DB_USERNAME=postgres
export DB_PASSWORD=password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=together
echo '  √ database configured'

export API_HOST='127.0.0.1'
export API_PORT=8080
echo "  √ API configured"
