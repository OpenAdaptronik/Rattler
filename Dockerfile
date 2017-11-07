FROM alpine:latest

MAINTAINER Alexander Kopp "alexander.kopp@stud.tu-darmstadt.de"

RUN apk add --no-cache python3 ca-certificates && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache


COPY . /app
WORKDIR /app

EXPOSE 5000

RUN pip -V
RUN pip install --no-cache-dir -r requirements

ENTRYPOINT ["python"]
CMD ["rattler.py", "run"]