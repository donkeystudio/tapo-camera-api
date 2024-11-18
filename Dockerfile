FROM python:3.10-slim-bookworm

WORKDIR /donkeystudio

ADD . .

ENV TZ="Asia/Singapore"
RUN ln -snf /user/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -r requirements.txt

CMD [ "python3", "tapo_camera_api.py" ]