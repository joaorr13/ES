FROM python:3.11

WORKDIR /usr/src/backend

COPY . .

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libhdf5-dev -y

RUN pip3 install -r requirements.txt

RUN pip3 install tf-keras

ENV MONGO_CONNECTION=mongodb://mongo:27017

ENV DB_NAME=zerozero

EXPOSE 3001

CMD [ "python3", "src/run.py"]