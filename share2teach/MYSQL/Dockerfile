# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application (update with the actual entry command if different)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM mysql:8

ENV MYSQL_ROOT_PASSWORD @AnbuBlackOps2024
COPY ./data.sql /docker-entrypoint-initdb.d/data.sql