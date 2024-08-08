
![image](https://github.com/user-attachments/assets/b71fc0e9-bd24-4946-b38a-09d27312c628)
# Airflow 사용

## 아키텍쳐 변화
- Docker가 아닌, 그냥 Local Ec2에서 사용

|crontab|Airflow|
|--|--|
|<img width="537" alt="image" src="https://github.com/user-attachments/assets/b606d6dc-2527-4576-8890-80da6e2a496c">|<img width="533" alt="image" src="https://github.com/user-attachments/assets/69b2609b-becf-4263-b3c0-7076fa2f8c3a">|


## Crontab 
- 크론탭 설정
- 크론탭 이전에 가상환경을 설정 후 your_pyenv_name 변경 필요
- crontab.py 설정 경로도 함께 지정 필요 : [crontab 실행파일](crontab.py)

```
crontab -e

---
*/1 * * * * /home/ubuntu/.pyenv/versions/3.11.9/envs/your_pyenv_name/bin/python /path/to/crontab.py 
```

#### 장점
1. 다른 플랫폼을 사용하지 않더라도 손쉽게 사용할 수 있음.
2. 속도가 더 빠름
3. 저장소 혹은 자원의 사용량이 적음

#### 단점
1. 의존성 관리가 부족함
   - API 호출이 실패시 재호출의 어려움
   - API 호출 실패시 파이썬 프로세스가 죽음
2. 에러 코드 확인 어려움 
3. Task를 분리하여 활용할 수 없음


## Airflow 
- [Airlow Code](/setting/server1/docker/airflow/dags/)


#### 장점
1. Crontab에서 하지 못했던 단점들을 모두 보완해서 활용할 수 있음
2. 모니터링의 간편함
3. 복잡한 작업으로도 사용 가능
   - 의존성, 순서 등 지원
4. 연동이 편리함

#### 단점
1. DAG 사용이 쉽지 않음.
2. 유지 관리 작업 비용이 많이 들어감
3. Crontab에 비해 자원을 더 많이 사용함

----------
=> 프로젝트 안정성을 높이고 Task의 의존성 설정 및 모니터링 기능등을 통한 부분에 필요성을 느꼈고 Airflow를 사용함. 
