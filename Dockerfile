FROM ubuntu:18.04
LABEL maintainer "Sebastian Schmid"

# Install dependencies
RUN  apt-get update && apt-get install -y \
                    curl \
                    cron \
                    nano \
                    python3-pip

# Copy scripts
COPY scripts /scripts

# Install python packages
RUN pip3 install -r /scripts/requirements.txt

# Create temp folder for downloaded files
RUN mkdir temp
RUN mkdir data

# Copy cronjob
COPY scripts/cronjob /etc/cron.d/container_cronjob

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/container_cronjob

# Apply cron job
RUN crontab /etc/cron.d/container_cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD ["cron", "-f"]