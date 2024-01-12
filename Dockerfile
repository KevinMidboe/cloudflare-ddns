FROM python:3.10-alpine

COPY *.py .
COPY .env .

RUN pip install requests python-dotenv
CMD python3 main.py
