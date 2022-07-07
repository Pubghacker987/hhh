FROM python:3.10.5-buster

WORKDIR /root/bot

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

# Starting Worker directory
CMD ["python3","-m","bot"]
