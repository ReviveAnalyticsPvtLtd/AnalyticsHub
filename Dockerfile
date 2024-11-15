FROM python:3.10-slim

COPY . /app

WORKDIR /app

USER root

RUN pip install -r requirements.txt

RUN chmod -R 777 /app

EXPOSE 7860

CMD ["python", "app.py"]