FROM python:3.11-slim

RUN pip install psycopg2-binary

WORKDIR /app
COPY *.sql ./
COPY setup.py ./

CMD ["python", "setup.py"]