FROM python:3.13.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /project-root

COPY requirements.txt /project-root/
RUN pip install -r requirements.txt

COPY . /project-root/
