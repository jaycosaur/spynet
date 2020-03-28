FROM mohaseeb/raspberrypi3-python-opencv:latest

COPY . /root/app

RUN python -m pip app/requirements.txt

WORKDIR /root/app

CMD ["python", "main.py"]

