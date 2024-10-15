# Use the official Python 3.8 image from Docker Hub
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . /app/

# Expose the port your application will run on
EXPOSE 8000

# Command to run your application
ENTRYPOINT ["python", "main.py"]

# Default argument (can be overridden)
CMD ["abcd1234"]

# Build
# docker build -t pcs-rasp .

# Run with argument
# docker run -e DEV_MQTT_HOST="191.168.0.171" pcs-rasp abcd1234
# docker run -e DEV_MQTT_HOST="127.0.0.1" pcs-rasp abcd1234

# Run without argument
# docker run -e DEV_MQTT_HOST="191.168.0.171" pcs-rasp


