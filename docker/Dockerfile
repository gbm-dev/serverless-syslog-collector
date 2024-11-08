# Use the official Fluentd image
FROM fluent/fluentd:edge-debian

# Install necessary plugins
USER root

# Install the Azure Event Hubs plugin
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
