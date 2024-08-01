FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

EXPOSE 8000

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=todo_app.settings

# Run the Django application using Gunicorn
CMD ["gunicorn", "todo_app.wsgi:application", "--bind", "0.0.0.0:8000"]
