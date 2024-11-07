# Use the official Fluentd image
FROM fluent/fluentd:latest

# Install necessary plugins
USER root

# Install Azure plugins (choose the one you need)
# For Azure Blob Storage
RUN fluent-gem install fluent-plugin-azure-storage-append-blob

# For Azure Event Hubs
RUN fluent-gem install fluent-plugin-azure-eventhubs

# Clean up
RUN gem sources --clear-all && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/* /var/tmp/*

# Copy Fluentd configuration file
COPY fluent.conf /fluentd/etc/fluent.conf

# Expose syslog port (UDP and/or TCP)
EXPOSE 514/udp

# Set the default command to run Fluentd
CMD ["fluentd", "-c", "/fluentd/etc/fluent.conf"]
