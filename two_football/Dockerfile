FROM tiangolo/uwsgi-nginx-flask:python3.6

ARG ENV
ENV ENV ${ENV}

RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev || apt-get -y install libmysqlclient-dev

ADD ./requirements.txt /two-football-backend/requirements.txt
# ADD ./uwsgi.ini /two-football-backend/uwsgi.ini

WORKDIR /two-football-backend

RUN pip install -r requirements.txt

COPY . /two-football-backend

# RUN chmod +x /two-football-backend/wait-for-it.sh
RUN chmod +x /two-football-backend/run.sh

CMD python database.py

CMD ./run.sh