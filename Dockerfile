FROM public.ecr.aws/bitnami/python:3.10 as pyBuilder

LABEL description="Deploy to Drive"
LABEL maintainer="kemalcanbora@gmail.com"

COPY . /app/
WORKDIR /app

RUN apt update && apt install -y apt-transport-https ca-certificates sqlite3
RUN /opt/bitnami/python/bin/pip3 install -r /app/requirements.txt
CMD ["/opt/bitnami/python/bin/python3", "/app/app.py"]