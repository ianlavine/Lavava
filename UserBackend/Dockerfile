# Use the official Python image from the Docker Hub with the slim variant for smaller size
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app

# Make port 5553 available to the world outside this container
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
