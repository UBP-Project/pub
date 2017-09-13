# Use an official Python runtime as a parent image
FROM python:3.5

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_CONFIG development

# Run app.py when the container launches
#CMD ["python", "manage.py", "shell"]
#CMD ["db.drop_all()"]
#CMD ["db.create_all()"]
#CMD ["seed()"]
#CMD ["quit()"]
CMD ["python", "manage.py", "runserver"]