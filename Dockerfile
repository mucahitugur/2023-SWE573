
FROM python:3.11

# Set the working directory in the container
RUN mkdir /app

WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Django project code to the working directory
COPY . .

# Expose the port that Django runs on
EXPOSE 8000
RUN chmod +x manage.py

# Define the command to run when the container starts
CMD sh -c 'python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000'


