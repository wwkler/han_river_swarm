# Kafka consuemr 선택
- kafka 에서 데이터를 받아오기 위해 consumer를 다양한 방법으로 선택할 수 있음.
- 실시간 대시보드를 위해 ES -> Kibana에 가장 적합한 Consumer를 선택해야할 필요가 있음.
- 총 3가지의 Consumer를 비교하여 최종 아키텍쳐 선택


## Logstash 사용
<img width="500" alt="image" src="https://github.com/user-attachments/assets/da211f0a-9465-4e6f-8ec1-52e8fdec848a">

- Logstash를 Kafka의 consumer로 활용
- 전처리는 Logstash conf 파일의 Filter 기능을 활용
- [Logstash consumer conf](./logstash.conf)
  - kafka_topic, kafka_server_ip, es_server_ip 수정 필요 
- 장점
  - conf 파일 하나로 consumer 기능, 전처리, DB(ES) 적재까지 한번에 가능
  - ES(Elastic Search)와 호환성이 좋아서 속도가 빠름
  - kafka의 consumer로 사용시, 기본적으로 'logstash'라는 consumer 그룹을 생성해서 offset을 저장해놓음
  - kafka에 바라보는 topic이 없으면 새롭게 생성됨 ( kafka 설정에서 제거 가능) 
- 단점  
  - 전처리가 더 복잡해지면 filter 기능은 제한이 있음
  - 빅데이터가 된다면 성능이 달라질 수 있음


## Spark 사용
<img width="500" alt="image" src="https://github.com/user-attachments/assets/730be3ba-616d-4d6d-8399-9a01ae9035d7">

- Spark를 Kafka의 consumer로 활용
- spark가 제공하는 pyspark로 작성한 python code를 수행
- [Spark consumer conf](./spark.py)
- 장점
  - python에 익숙하다면 전처리하기 편리함
  - python 라이브러리를 활용하기 편리함
  - 빅 데이터를 활용한다면, 가장 적합
  - ES의 라이브러리를 활용하여 손쉽게 적재 가능 
- 단점
  - kafka의 consumer 기능을 설정할 수 있는 방법이 없어서 데이터 유실 가능성이 존재
  - pip install과 같이 라이브러리를 활용하는 것이 아닌, 다른 방식으로 경로를 지정해줘야 하기 때문에 라이브러리 사용이 불편함

## python consumer + logstash 활용
<img width="500" alt="image" src="https://github.com/user-attachments/assets/e7a8333e-67ab-4fbf-b805-13d4f4266b94">

- python consumer를 통해 Logstash가 실시간으로 감시하는 JSON 파일에 데이터를 추가
- python Consumer는 kafka를 바라보고 , logstash는 임시 json파일만 바라봄
- [Python consumer code](./python_con.py)
- [Python consumer logstash code](./python_con_log.conf)
- 장점
  - 파이썬 코드 혹은 Logstash filter 아무곳에서나 전처리를 할 수 있음
- 단점
  - 파이프라인 과정이 복잡하고 설계하기 어려운 부분이 존재
  - 시간이 가장 오래걸림
 
--------
=> 다양한 장단점을 비교해 보았을 때, 현 데이터와 프로젝트에 가장 적합한 방식은 첫번째 방식이라고 결정
선택이유
- 빠른 속도
- 엘라스틱서치와의 호환성 문제
- 단순한 전처리를 간편하게 가능
