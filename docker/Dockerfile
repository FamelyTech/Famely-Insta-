# Start from the builder file to avoid installing deps all the time
FROM registry.digitalocean.com/nano-registry/jalodei:build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Copy the Django application code into the container
COPY jalodei /jalodei
COPY run.sh /jalodei/run.sh

WORKDIR /jalodei
# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port on which Gunicorn will run (change this to your desired port)
EXPOSE 8000

# Start Gunicorn to run the Django application
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_chat.wsgi:application"]
CMD ["bash", "run.sh"]
