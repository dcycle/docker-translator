FROM python:alpine

RUN pip install requests pyyaml && mkdir -p /app/code

WORKDIR /app

COPY docker-resources /app

ENTRYPOINT [ "python3" ]
