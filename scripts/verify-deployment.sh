#!/bin/bash

# Script to verify if all services in docker-compose are healthy
# Usage: ./verify-deployment.sh [timeout_in_seconds]

TIMEOUT=${1:-120}
INTERVAL=5
ELAPSED=0

echo "🔍 Verifying service health..."

while [ $ELAPSED -lt $TIMEOUT ]; do
    UNHEALTHY=$(docker-compose ps --format json | grep -v "healthy" | grep -v "running" | wc -l)
    
    # Note: Depending on docker-compose version, the output format might vary.
    # A more robust way is to check the 'State' or 'Health' field.
    
    ALL_HEALTHY=true
    SERVICES=$(docker-compose ps --services)
    
    for service in $SERVICES; do
        HEALTH=$(docker inspect --format='{{json .State.Health.Status}}' $(docker-compose ps -q $service) 2>/dev/null)
        if [ "$HEALTH" != "\"healthy\"" ] && [ "$HEALTH" != "" ]; then
            echo "⏳ Service $service is $HEALTH..."
            ALL_HEALTHY=false
        fi
    done

    if [ "$ALL_HEALTHY" = true ]; then
        echo "✅ All services are healthy!"
        exit 0
    fi

    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))
done

echo "❌ Timeout reached. Some services are still not healthy."
docker-compose ps
exit 1
