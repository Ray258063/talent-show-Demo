FROM python:3.10.12

ADD weight weight

WORKDIR /app

ADD requirements.txt .

ADD .env /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt install curl -y

COPY src .

RUN rm requirements.txt && \
    pip cache purge

EXPOSE 8000

CMD uvicorn main:app --workers 1 --host 0.0.0.0 --port 8000 --timeout-keep-alive 30