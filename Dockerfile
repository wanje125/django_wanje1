#pull official base image 파이썬 이미지를 불러온다
FROM python:3.8.0-alpine

#set work directory 프로젝트 작업폴더를 /usr/src/app으로 지정한다.
WORKDIR /usr/src/app

#set environment variable 
ENV PYTHONDONTWRITEBYTECODE 1
#파이썬은 종종 소스 코드를 컴파일해서 확장자가 .pyc인 파일을 생성한다. 도커를 이용할때는 pyc가 필요하지 않아 .pyc를 생성하지 않게 한다.
ENV PYTHONUNBUFFERED 1
#파이썬 로그가 버퍼링없이 즉각적으로 출력하게 한다.

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev libc-dev
RUN apk add --no-cache \
        libressl-dev \
        musl-dev \
        libffi-dev && \
    pip install --upgrade pip --no-cache-dir cryptography==3.3.1 && \
    apk del \
        libressl-dev \
        musl-dev \
        libffi-dev
#requirements.txt에서 살펴본 라이브러리를 설치하기 위해 필요한 gcc, musl-dev등을 미리 설치한다. 
#오류가 나서 2시간동안 미칠뻔햇다.  찾아보고 위에거를 더 추가하니 해결됐다.

COPY . /usr/src/app/
#로컬 컴퓨터의 현재위치에 있는 모든 파일을 작업폴더로 복사한다.(/usr/src/app/으로)
#install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#requiredments.txt에 나열된 라이브러리를 설치한다.
EXPOSE 8000