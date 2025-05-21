# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in docker
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 8000

# Install any pineeded packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#CMD ["fastapi", "run", "main.py"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]