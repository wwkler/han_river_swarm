# 너랑 한강갈래 :relaxed:

## 프로젝트 개요 및 목표 

- 서울 실시간 도시 데이터를 활용한 한강 공원 데이터 파이프라인 구축
- 한강 공원 실시간 현황 데이터를 보기 쉽게 시각화

## 팀원 

|신윤재|서영수|이연호|김영우|박윤수|정지석|
|--|--|--|--|--|--|
|<img width="100" alt="image" src="https://github.com/user-attachments/assets/711bd24b-02b0-4515-8c42-feb87f47ff33">|<img width="100" alt="image" src="https://github.com/user-attachments/assets/9ab53d0c-6ba4-45b9-aaef-032918bac885">|<img width="100" alt="image" src="https://github.com/user-attachments/assets/31148c90-50b8-4b01-9b02-0845e9226275">|<img width="100" alt="image" src="https://github.com/user-attachments/assets/7db3eda9-319c-4fd4-aa87-023d82c65560">|<img width="100" alt="image" src="https://github.com/user-attachments/assets/48dab61e-66ca-4af0-9f8f-91a81782109c">|<img width="100" alt="image" src="https://github.com/user-attachments/assets/44160bab-2c35-4576-a4e3-ada84714a7ad">|
|[yoonjaeo](https://github.com/yoonjaeo)|[SeoYeong-su](https://github.com/SeoYeong-su)|[CUAGAIN-95](https://github.com/CUAGAIN-95)|[wwkler](https://github.com/wwkler)|[dnlpys](https://github.com/dnlpys)|[jiseok6843](https://github.com/jiseok6843)|


## :bar_chart: 사용 데이터
- 서울 실시간 도시데이터 API 활용
  - https://data.seoul.go.kr/dataVisual/seoul/guide.do
  - API Key 발급 필요 

## :low_brightness: 요구사항 확인 및 분석
- 수집
  - 전체 115개의 핫스팟에 대한 데이터를 모두 수집 
  - 실시간으로 데이터 수집
  - 1분 이내의 빠르게 수집 
- 저장
  - 데이터 중복 및 유실 방지
  - 데이터 Lake 및 DB 활용
  - 시각화에 가장 적합한 DB 활용
- 변환 및 전처리
  - 115개의 핫 스팟 중 11개의 한강 공원 지역만 전처리
  - 다양한 데이터 중 인구, 도로, 주차장, 날씨 데이터 전처리 
- 사용
  - 실시간 데이터를 효과적으로 시각화하는 툴 사용하여 시각화
  - 다양하게 활용할 수 있도록 데이터 파이프라인 구축
- 관리
  - 플렛폼들의 버전 관리를 손쉽게 할 수 있도록 함
  - 플렛폼들의 서비스를 모니터링 하고 시스템 가용성 유지
  - 일관된 개발환경 사용

## :desktop_computer: 개발환경 설정
- AWS EC2 활용
  - 총 3개의 서버
  - Image : Ubuntu 24.04 LTS
  - Instance Type : t2.xlarge
  - Storage : 100GB

## 📐 최종 아키텍쳐 
<img width="675" alt="image" src="https://github.com/user-attachments/assets/a96a7350-7b16-4bbe-b1b6-7bc18ea94161">


#### 개발 환경 및 사용 이유
- 해당 데이터에 가장 적합한 파이프라인를 찾기 위해 여러 아키텍쳐 실험 및 선정
  - [Airflow](architecture/airflow)
  - [ELK Stack](architecture/kafka_consumer)
  - [Docker & Swarm](setup/docker.md)

#### 최종 아키텍쳐 구축 방법 확인
- [Docker 설치 및 세팅](setup/docker.md)
- [ubuntu 세팅](setup/ubuntu.md)
- [Docker swarm으로 pipeline 한꺼번에 띄우는 방법](setting/README.md) 


## :video_camera: 시연 영상
- Server3에서 Docker swarm을 이용하여 각 서버에 모든 Container를 띄움
- 각 서버에서 띄워진 Container 확인
- Airflow 시연
- 시각화 시연
- 시연 영상 확인 :point_down::point_down:

<br>
<a href="https://youtu.be/83F02z5lzX8" target="_blank">
  <img src="https://github.com/user-attachments/assets/4aa4ecc0-80e8-4d24-a154-7dc1c869f3c2" alt="Demo Video Thumbnail" width="400" />
</a>


## 	:bulb: 대시보드 
- 전체 한강 공원 
![image](https://github.com/user-attachments/assets/feb8e51d-bb94-4f41-aadf-9031bfb03e8d)

- 원하는 한강공원 Filtering
![image](https://github.com/user-attachments/assets/7a3e3a2b-e232-47bd-a6a7-b716f3c0cfc0)

## :mag_right: 트러블 슈팅 관련 내용 
