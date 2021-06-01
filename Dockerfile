FROM python:3.8-slim

ENV folder=/opt/venv
RUN python3 -m venv $folder
ENV PATH="$folder/bin:$PATH"

WORKDIR /usr/src/app


COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt




COPY . .
RUN pytest

