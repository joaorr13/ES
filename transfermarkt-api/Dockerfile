FROM python:3.9-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app
COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dateutil


COPY . ./

CMD ["python", "app/main.py"]