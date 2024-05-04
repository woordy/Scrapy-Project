# Use an official Python 3.12 runtime as a base image running on Debian bookworm OS
FROM python:3.12-bookworm

# Set the working directory in the container to /HHViz
WORKDIR /Scrappy

# Update the package lists and upgrade the system
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /Scrappy/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt 

# Copy the rest of the application
COPY . /Scrappy

# Make port 5000 available to the world outside this container
EXPOSE 5000
EXPOSE 8050

# Set the command to run when the container starts.
# Here, we use 'tail -f /dev/null' to keep the container running indefinitely without consuming CPU resources.
CMD ["tail", "-f", "/dev/null"]
