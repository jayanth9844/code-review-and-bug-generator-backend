#!/bin/bash
# Start Docker containers

echo "Starting Code Review and Bug Generator API..."
docker-compose up -d

echo ""
echo "✓ Services started successfully!"
echo ""
echo "API available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Redis running on: localhost:6379"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
