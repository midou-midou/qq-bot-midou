FROM python:3.10.14-slim
LABEL maintainer="midoude163@163.com"

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone
RUN python -m pip install --user pipx
RUN python -m pipx ensurepath
RUN pipx install nb-cli

COPY ./ /app
WORKDIR /app/
CMD ["nb","run"]
