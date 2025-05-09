FROM python:alpine

RUN pip install requests pyyaml && mkdir -p /app/code

WORKDIR /app

COPY docker-resources /docker-resources

RUN cp /docker-resources/*.py /app/

ENTRYPOINT [ "python3" ]
