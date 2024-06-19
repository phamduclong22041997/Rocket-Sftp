FROM registry-supra.winmart.vn/lib/python:3.8-alpine-template

WORKDIR /app
RUN mkdir tmp
COPY . .

ENV MAKEFLAGS="-j$(nproc)"

RUN apk add --no-cache tzdata openssh \
    && mkdir /root/.ssh \
    && ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime \
    && pip install --trusted-host 10.235.206.105 --index-url http://10.235.206.105:8888/nexus/repository/python-proxy/simple/ --upgrade pip \
    && pip3 install --trusted-host 10.235.206.105 --index-url http://10.235.206.105:8888/nexus/repository/python-proxy/simple/ -r requirements.txt


# && pyinstaller  --onefile build.spec \
# && mv dist/ovsftp ovsftp_bin

CMD ["python","main.py"]
