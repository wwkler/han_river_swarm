#!/bin/bash

# airflow init이 먼저 실행되고 다른 worker, webserver 등의 컨테이너가 띄워져야 하기 때문에 shell 사용
sudo docker stack deploy -c /home/b04/docker/airflow_init.yml seoul_api

sleep 15

sudo docker stack deploy -c /home/b04/docker/airflow_action.yml seoul_api
sleep 3

sudo docker stack deploy -c /home/b04/docker/kafka.yml seoul_api
sleep 3

sudo docker stack deploy -c /home/b04/docker/elk_stack.yml seoul_api