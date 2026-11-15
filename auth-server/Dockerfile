# Use an official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the auth server files
COPY . .

# Auth server runs on port 8001
EXPOSE 8001

# Start the FastAPI auth server
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8001"]