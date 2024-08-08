<img width="500" alt="image"  src= "https://github.com/user-attachments/assets/e1a77045-ac90-45f5-bf32-7668307d792a">


# Docker & Docker Swarm 사용 이유 
- 도커
  - 버전관리 용이
  - 컨테이너 관리의 편리성
  - 일관된 개발 환경
  - 프로그램 격리성 제공
- Docker Swarm
  - 한꺼번에 도커 컨테이너들을 확인하고 관리하기 쉬움
  - Cluster 구성에 용이
  - 따로 설치할 필요가 없음
  - 컨테이너의 상태를 확인하여 죽게되면 다시 띄워주는 등 자동적으로 관리해줌
  - 소규모 컨테이너들을 관리하게 편리함
  - 한개의 yml 파일을 통해서 다양한 서버에 container를 한번에 띄울 수 있음
 

# Docker 설치 

- 모든 서버에서 실행 (server1, server2, server3)

## 설치 명령어
```
sudo apt-get update
sudo apt-get install ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $USER
exec $SHELL

```

## 설치 확인
```
systemctl status docker

docker --version 
```
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/245e553c-5c39-4b35-9cbc-e74727e63457">

## Docker 명령어
- image build (Dockerfile -> Image)
```
cd /path/to/Dockerfile_folder/
sudo docker build -t image_name .
``` 

# docker swarm 구성
- docker swarm은 따로 설치할 필요가 없음. (docker 설치시 함께 설치됨)

## 네트워크 구성 
- 한개의 서버에서만 init을 쓰고, 다른 서버는 출력값을 복사 붙여넣기 해주기
- 이유 : 한개만 manager(leader 로 사용하고 나머지는 다 worker로 사용해주기 위해서 
```
# 서버1 
sudo docker swarm init
```
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/80e20015-3d8d-499e-a0a4-5526a0f92ebf">

```
# 서버2, 서버3
sudo docker swarm join --token ~~~~
```

- 만약 3개를 모두 매니저(+워커 기능 포함) 으로 해주고싶다면? 
```
# server1
sudo sudo docker swarm join-token manager
```
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/8054aa9a-5e2b-4eb3-9956-3e264f936461">

```
# server2, server3
sudo docker swarm join --token ~~~~
```



## node 확인
- manager node에서만 명령어 실행 가능
- Leader만 
```
docker node ls
```
