# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable (replace 'yourproject' with the actual project name)
ENV DJANGO_SETTINGS_MODULE=core.settings

RUN echo "import warnings\nfrom cryptography.utils import CryptographyDeprecationWarning\nwarnings.filterwarnings('ignore', category=CryptographyDeprecationWarning)" >> /usr/local/lib/python3.9/site-packages/paramiko/pkey.py

# Run migrations, collect static files, and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py createsuperuser && python manage.py runserver 0.0.0.0:8000"]
