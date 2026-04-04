# Use lightweight Python image
FROM python:3.10.14-slim-bookworm

RUN apt-get update && \
    apt-get install -y\
    python3-dev

    
# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run app
CMD ["python", "main.py"]