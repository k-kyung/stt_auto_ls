FROM python:3.11-slim
ENV LANG ko_KR.utf-8
RUN set -ex \
    && ln -s -f /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN apt install ffmpeg