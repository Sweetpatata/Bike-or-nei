FROM python:3.10.6
FROM --platform=linux/amd64 tensorflow/tensorflow:2.10.0
COPY product product
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn product.api.fast:app --reload --host 0.0.0.0 --port $PORT
