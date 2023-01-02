FROM python:3.10.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /support

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /support


