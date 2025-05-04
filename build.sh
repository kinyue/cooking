#!/usr/bin/env bash
# Exit on error
set -e

# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies and build
cd frontend
npm install
npm run build
cd ..

echo "Build completed successfully!"
