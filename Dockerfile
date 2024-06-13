FROM ubuntu:latest

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    apt-get clean

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages in the virtual environment
RUN pip install flask pymongo

# Copy application files
COPY templates /app/templates
COPY app.py /app/app.py

# Expose the port the app runs on
EXPOSE 5000
EXPOSE 27017

# Run the application
CMD ["python3", "/app/app.py"]