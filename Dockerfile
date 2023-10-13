
FROM python:3.10.5-alpine3.15

RUN apk add --no-cache build-base

COPY ./requirements.txt requirements.txt
WORKDIR /code
ADD . /code
RUN pip install -r requirements.txt

CMD ["python", "cleanup-hum-preview-envs.py"]