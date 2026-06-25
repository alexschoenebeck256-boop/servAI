#!/bin/bash
set -e

echo "🚀 Setting up ServAI local development environment..."

# 1. Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env from .env.example..."
    cp infra/.env.example .env
    echo "⚠️  Please update .env with your actual API keys!"
fi

# 2. Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# 3. Pull images and build
echo "📦 Building Docker images..."
make build

# 4. Start services
echo "✨ Starting services..."
make dev
