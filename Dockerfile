FROM python:3.10-alpine

COPY requirements.txt .
COPY src/*.py ./

RUN pip install -r requirements.txt
CMD python3 main.py
