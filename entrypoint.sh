#!/bin/sh
# Extract the container's hostname assigned by Docker
CONTAINER_HOSTNAME=$(hostname)

# Extract the last part of the hostname as a unique identifier
INSTANCE_NUMBER=$(echo "$CONTAINER_HOSTNAME" | grep -oE '[0-9]+$')

# Set the proper hostname inside the container
export HOSTNAME="executor-$INSTANCE_NUMBER"

echo "Running as $HOSTNAME"

exec "$@"