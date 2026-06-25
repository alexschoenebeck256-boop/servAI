#!/bin/bash

# validation script for ServAI environment variables

# List of required environment variables
REQUIRED_VARS=(
    "DATABASE_URL"
    "REDIS_URL"
    "VECTOR_DB_URL"
    "APP_SECRET_KEY"
    "OPENAI_API_KEY"
    "STRIPE_SECRET_KEY"
    "TWILIO_ACCOUNT_SID"
    "TWILIO_AUTH_TOKEN"
    "NEXTAUTH_SECRET"
)

MISSING=0

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: Environment variable $var is not set."
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -gt 0 ]; then
    echo "🚨 Total missing required variables: $MISSING"
    exit 1
else
    echo "✅ All required environment variables are set."
    exit 0
fi
