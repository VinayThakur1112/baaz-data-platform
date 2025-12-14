FROM python:3.12-slim

WORKDIR /app

COPY app/ /app/

RUN pip install pandas pyarrow azure-storage-blob

CMD ["python", "process_landing.py"]