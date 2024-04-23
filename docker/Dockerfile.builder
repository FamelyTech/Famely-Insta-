# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev libc-dev\
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /

# Install Python dependencies
COPY requirements.txt /
COPY requirements_prod.txt /
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements_prod.txt
