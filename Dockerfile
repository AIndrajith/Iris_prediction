# Use the official python image as a base
FROM python:3.9-slim

# set environment variables to prevent python from writing .pyc files and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# copy the requirements file to the container
COPY requirements.txt /app/requirements.txt

# Install he python dependencies
RUN pip install -r /app/requirements.txt

# copy the application code to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]