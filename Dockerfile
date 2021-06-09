FROM python:3.8-slim-buster

#install git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git netcat gcc postgresql && \
    apt-get clean

# Install Python requirements
COPY backend/requirements.txt /app/
WORKDIR /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Python app
COPY backend /app/backend

WORKDIR /app/backend/
