FROM ubuntu:16.04

ENV ACC_ENV=prod

# Set work directory
WORKDIR /opt/accounting

# Add requirements file
ADD requirements.txt ./requirements.txt

# Perform an update and install packages
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    netcat \
    python3-dev \
    python3-setuptools \
    python3-pip \
    python3-wheel \
    supervisor \
 && pip3 install -r requirements.txt \
 && apt-get remove -y python3-pip \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/* /root/.cache

# Copy code
COPY . /opt/accounting

# Configuration
RUN rm -rf /etc/supervisor/supervisord.conf \
 && cp config/supervisor/supervisord.conf /etc/supervisor/supervisord.conf \
 && cp config/supervisor/accounting.conf /etc/supervisor/conf.d/accounting.conf \
 && python3 manage.py collectstatic --noinput --settings=accounting.settings \
 && chown -R www-data:www-data /opt/accounting \
 && chmod +x config/docker/run.sh

# Gunicorn configuration
# Full settings can be found here: http://docs.gunicorn.org/en/stable/settings.html
ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:80 --workers 8 --error-logfile - --access-logfile - --log-level=debug"

# Expose ports
EXPOSE 80 3333

# Docker container entrypoint
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["/opt/accounting/config/docker/run.sh"]
