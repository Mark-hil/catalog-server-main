# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set the environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]