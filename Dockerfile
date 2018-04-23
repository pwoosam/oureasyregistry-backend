# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /oureasyregistry-backend

# Copy the current directory contents into the container at /outeasyregistry-backend
ADD . /oureasyregistry-backend

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 9001

# Define environment variable
#ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]
