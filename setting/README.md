# 실행 환경 세팅하기

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
- [setting](setting/) 폴더에 존재하는 서버에 맞게 각각 파일을 넣어주기
- 
