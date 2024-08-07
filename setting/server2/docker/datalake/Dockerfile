FROM python:3.11.9

WORKDIR /home/

RUN apt update -y
RUN pip install kafka-python
RUN pip install pytz
RUN mkdir /home/datalake/

COPY ./datalake_con.py /home/