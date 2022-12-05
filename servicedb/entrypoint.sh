#!/bin/sh

echo "Waiting for rabbitmq..."

while ! nc -z rabbitmq 5672; do
  sleep 1
done

echo "RabbitMQ started"

exec "$@"