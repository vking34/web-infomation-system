FROM node:8.11

ARG REACT_APP_ENV
ENV REACT_APP_ENV ${REACT_APP_ENV}

#ADD package.json /frontend/package.json
#ADD package-lock.json /frontend/package.json
ADD server.js /frontend/server.js

WORKDIR /frontend

#RUN npm install

RUN npm install express

#ADD src /frontend/src
#ADD public /frontend/public
ADD build /frontend/build

#COPY . /frontend

RUN npm build

CMD node server.js
