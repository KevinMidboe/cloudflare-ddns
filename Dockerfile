FROM python:3.10-alpine

COPY *.py ./

RUN pip install requests python-dotenv
CMD python3 main.py
