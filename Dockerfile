FROM python:3.7-alpine3.11
WORKDIR /usr/src/app

# Install lxml
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir lxml>=3.5.0 && \
    apk del .build-deps

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY . /usr/src/app
EXPOSE 80
# Command to run when running docker run
CMD [ "gunicorn", "--timeout", "90",  "-b", "0.0.0.0:80", "server:app" ]
# docker build -t <tag-name> <path>
# docker container run -it -p 127.0.0.1:1420:80 -v /home/liao/Desktop/glossing/:/usr/src/app/corp/ asbc

