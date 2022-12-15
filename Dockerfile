# Start from a base image with Python installed
FROM python:3-slim

# Copy the Python script that serves the HTTP endpoint
COPY main.py /usr/src/app/

# Install the HTTP server library
RUN pip install nums_from_string

# Run the Python script when the container starts
CMD ["python", "/usr/src/app/main.py"]
