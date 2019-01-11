FROM alpine:latest
LABEL authors="kud.rom.sh@gmail.com"

RUN apk upgrade --no-cache
RUN apk add --no-cache \
openssh \
rsync \
python3 \
build-base \
python3-dev \
libffi-dev \
openssl-dev
RUN pip3 install --upgrade --no-cache-dir pip
RUN pip3 install ansible-lint
RUN apk del python3-dev libffi-dev build-base openssl-dev
RUN rm -rf /var/cache/* && rm -rf /root/.cache/*
RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi
