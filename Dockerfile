FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 instal -r requirements.txt
COPY . .