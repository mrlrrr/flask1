FROM ubuntu:latest
LABEL authors="erdem"

ENTRYPOINT ["top", "-b"]

# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 2 --timeout 0 main:app
# Make port 5000 available to the outside world
#EXPOSE 8080

# Define environment variable for Flask to run in production mode
#ENV FLASK_APP=app.py
#ENV FLASK_RUN_HOST=0.0.0.0
#ENV FLASK_ENV=production

# Run the application
#CMD ["flask", "run"]
