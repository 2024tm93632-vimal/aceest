# Use official Python image (already has python + pip)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Run tests (optional but good for CI)
RUN python -m pytest || true

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]