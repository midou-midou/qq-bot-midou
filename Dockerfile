FROM python:3.10.14-slim
LABEL maintainer="midoude163@163.com"
LABEL name="qq-bot-midou"

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone
RUN python -m pip install --user pipx
RUN python -m pipx ensurepath
RUN /root/.local/bin/pipx install nb-cli -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app
COPY .venv /app/.venv
COPY plugins /app/plugins
WORKDIR /app/
RUN ln -s /usr/local/bin/python .venv/bin/python
CMD ["/root/.local/bin/nb","run"]
