#!/bin/bash
DB_NAME=donauhandj87mysql11
DB_FILE=${DB_NAME}.sql
URL=yxw8ZKJ4oxpz3xG
DATA_DIR=datadir/
echo ${DB_FILE}
echo ${DB_NAME}
export DB_USER="root"
export DB_PW="donauhandel"
export DB_NAME=${DB_NAME}
mkdir ${DATA_DIR}
wget -O ${DATA_DIR}${DB_FILE} https://oeawcloud.oeaw.ac.at/index.php/s/${URL}/download/${DB_FILE}

docker run \
  -d \
  --name ${DB_NAME}  \
  -e MYSQL_ROOT_PASSWORD=${DB_PW} \
  -e MYSQL_DATABASE=${DB_NAME} \
  -v ${PWD}/${DATA_DIR}/${DB_FILE}:/docker-entrypoint-initdb.d/${DB_FILE} \
  -p 3307:3306 \
  mariadb:latest

sleep 60
docker container ps
sleep 30
docker container ps -a

docker container start ${DB_NAME}
docker container ps