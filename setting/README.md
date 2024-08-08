
## 폴더 생성
- docker container 와 volume(mount)를 연결해줄 폴더를 생성해주기

```
# server1
mkdir -p docker/airflow && cd docker/airflow
mkdir dags logs config plugins temp

# server2
mkdir -p docker/datalake && cd docker/datalake
mkdir data

# server3
mkdir -p docker && cd docker
mkdir -p elasticsearch/config
mkdir -p logstash/config logstash/pipeline
mkdir -p kibana/config
```

## 파일 생성 
- 폴더에 존재하는 서버에 맞게 각각 파일을 생성
  - [server1](./server1)
  - [server2](./server2)
  - [server3](./server3) 

|server1|server2|server3|
|--|--|--|
|<img width="250" alt="image" src="https://github.com/user-attachments/assets/ddfffa93-8951-4c3d-b7fc-b41f87e2d3ab">|<img width="250" alt="image" src="https://github.com/user-attachments/assets/74a9a7d7-b252-4b6f-bd98-af4f56751fac">|<img width="250" alt="image" src="https://github.com/user-attachments/assets/eb9d7c6c-cdc4-4114-b4eb-4362af414905">|
|dag안에 폴더 혹은 logs 안에 폴더는 따로 설정하지 않아도 됨.|--|--|


## 도커 이미지 생성
- airflow와 datalake의 image는 커스텀해서 생성해줘야 함.
- 컨테이너를 띄우고싶은 각 서버에 커스텀한 이미지가 있어야지만 swarm을 통해서 한 서버에서 컨테이너 관리가 가능함.
- 혹은, docker image를 docker hub에 넣어놓기.

|server|Dockerfile|설명|
|--|--|--|
|server1|[Airflow Dockerfile](setting/server1/docker/airflow/Dockerfile)|Kafka, 비동기 처리를 위한 라이브러리 설치|
|server2|[Datalake Dockerfile](setting/server2/docker/datalake/Dockerfile)|실행시킬 python file 및 필요한 라이브러리 설치|

```
# server1
cd ~/docker/airflow

## airflow_custom이라는 이름으로 이미지를 생성
sudo docker build -t airflow_custom .
```

```
# server2
cd ~/docker/datalake

sudo docker build -t datalake .
```


```
# image 확인
sudo docker images
```

## Swarm 실행
- [swarm_start shell 파일](/setting/server1/docker/swarm_start.sh)
- shell 파일을 실행시키기 위해서는 실행 권한을 줘야함

```
# server1
cd ~/docker
chmod 744 swarm_start.sh
```

- 실행 (조금 시간이 걸림.)  
```
./swarm_start.sh

-----
# 실행결과
...
Since --detach=false was not specified, tasks will be created in the background.
In a future release, --detach=false will become the default.
Creating service seoul_api_elasticsearch
Creating service seoul_api_logstash
Creating service seoul_api_kibana
```

- 제대로 실행되었는지 확인

```
# service 확인 - server1에서만 가능
## 명령어 실행시 replicas에 1/1이 뜨면 되는것
## init은 실행되고 죽는 컨테이너라 0이 되더라도 괜찮음. 
sudo docker service ls

# container 확인 - 각 서버에서 확인 가능
sudo docker container ls 
```
