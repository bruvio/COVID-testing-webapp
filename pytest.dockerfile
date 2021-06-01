FROM python:$VERSION_IF_NOT_SET-slim
MAINTAINER bruvio

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

RUN pip install pytest

ENTRYPOINT [ "pytest","/usr/src/app/tests" ]