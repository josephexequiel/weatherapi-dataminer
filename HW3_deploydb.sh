#!/bin/bash

# Pull latest docker image for mysql
docker pull mysql:latest

# Start mysql docker instance under maria_db container name using mysql:latest image
# MYSQL_ROOT_PASSWORD is the variable that contains the password for user root
docker run --name mysql -e MYSQL_ROOT_PASSWORD=dlsu_password -p 3306:3306 -d mysql:latest