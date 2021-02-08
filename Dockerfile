# Python 3.7.9 as base image
FROM python:3.7.9

# Expose port 5000
EXPOSE 5000

# Don't generate .pyc in container
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY . /pci-prototype-backend
WORKDIR /pci-prototype-backend

# Install pip requirements in root directory
RUN python -m pip install -r requirements.txt

# Switch to non-root piwatcher user
RUN useradd piwatcher && chown -R piwatcher /pci-prototype-backend
USER piwatcher

# Start Gunicorn server
CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info