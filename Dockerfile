FROM python:3.10.14-slim
LABEL maintainer="midoude163@163.com"
LABEL name="qq-bot-midou"

ENV SHELL=/bin/bash
SHELL [ "/bin/bash", "-c" ]

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone
RUN pip install --user pipx -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN /root/.local/bin/pipx ensurepath
RUN /root/.local/bin/pipx install nb-cli -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app
COPY plugins /app/plugins

WORKDIR /app/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["/root/.local/bin/nb","run"]
