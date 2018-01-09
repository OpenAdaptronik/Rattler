FROM python:3.6-alpine3.6

# logging to the console breaks without this
ENV PYTHONUNBUFFERED 1
ENV PYTHONFAULTHANDLER 1

LABEL maintainer Alexander Kopp "alexander.kopp@stud.tu-darmstadt.de"

RUN apk add --no-cache --virtual build-base && \
    apk add --no-cache ca-certificates mariadb-dev libffi-dev libjpeg freetype freetype-dev lcms2 lcms2-dev libjpeg-turbo libjpeg-turbo-dev zlib zlib-dev libwebp musl libgcc libgfortran libstdc++ gfortran openjpeg tiff lapack-dev openblas gettext && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

COPY . /app
WORKDIR /app

EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt
RUN apk del build-base

ENTRYPOINT ["python", "/app/manage.py"]
CMD ["runserver", "0:5000"]
