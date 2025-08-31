#!/bin/bash
# Packaging script for cooking app

# Exit on error
set -e

# Configuration
APP_NAME="cooking-app"
PACKAGE_DIR="dist"
VERSION=$(date +%Y%m%d-%H%M%S)
PACKAGE_NAME="${APP_NAME}-${VERSION}.tar.gz"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Clean previous builds
log_info "Cleaning previous builds"
rm -rf $PACKAGE_DIR
mkdir -p $PACKAGE_DIR

# Install backend dependencies
log_info "Installing backend dependencies"
log_info "Current directory: $(pwd)"
if [ ! -f "../backend/requirements.txt" ]; then
    log_error "Cannot find backend/requirements.txt. Please run this script from the deployment directory."
    exit 1
fi
pip install -r ../backend/requirements.txt --target $PACKAGE_DIR/backend_deps

# Copy backend code
log_info "Copying backend code"
mkdir -p $PACKAGE_DIR/backend
cp -r ../backend/app $PACKAGE_DIR/backend/
cp -r ../backend/data $PACKAGE_DIR/backend/
cp ../backend/requirements.txt $PACKAGE_DIR/backend/

# Copy database if it exists
if [ -f "../backend/instance/database.db" ]; then
    log_info "Copying existing database"
    mkdir -p $PACKAGE_DIR/backend/instance
    cp ../backend/instance/database.db $PACKAGE_DIR/backend/instance/
else
    log_warn "Database not found. A new one will be created during deployment."
fi

# Install frontend dependencies and build
log_info "Building frontend"
if [ ! -d "../frontend" ]; then
    log_error "Cannot find frontend directory. Please run this script from the deployment directory."
    exit 1
fi

# Store the original directory
SCRIPT_DIR=$(pwd)

# Build frontend
cd ../frontend
log_info "Installing frontend dependencies in: $(pwd)"
npm install || {
    log_error "Failed to install frontend dependencies"
    cd "$SCRIPT_DIR"
    exit 1
}

cp ../deployment/.env.production .env || {
    log_error "Failed to copy .env.production file"
    cd "$SCRIPT_DIR"
    exit 1
}

log_info "Building frontend application..."
npm run build || {
    log_error "Failed to build frontend application"
    cd "$SCRIPT_DIR"
    exit 1
}

# Return to original directory
cd "$SCRIPT_DIR"

# Verify dist directory exists
if [ ! -d "../frontend/dist" ]; then
    log_error "Frontend build failed: dist directory not found"
    exit 1
fi

# Copy frontend build
log_info "Copying frontend build"
mkdir -p $PACKAGE_DIR/frontend
cp -r ../frontend/dist $PACKAGE_DIR/frontend/ || {
    log_error "Failed to copy frontend build files"
    exit 1
}

# Copy deployment files
log_info "Copying deployment files"
mkdir -p $PACKAGE_DIR/deployment
cp ../deployment/deploy.sh $PACKAGE_DIR/deployment/
cp ../deployment/cooking-app-backend.service $PACKAGE_DIR/deployment/
cp ../deployment/cooking-app-frontend.service $PACKAGE_DIR/deployment/
cp ../deployment/nginx.conf $PACKAGE_DIR/deployment/
cp ../deployment/start-app.sh $PACKAGE_DIR/deployment/
cp ../deployment/.env.production $PACKAGE_DIR/deployment/

# Create version file
echo "$VERSION" > $PACKAGE_DIR/VERSION

# Create package
log_info "Creating package: $PACKAGE_NAME"
tar -czf $PACKAGE_NAME -C $PACKAGE_DIR .

# Calculate checksum
log_info "Calculating checksum"
sha256sum $PACKAGE_NAME > $PACKAGE_NAME.sha256

log_info "Package created successfully: $PACKAGE_NAME"
log_info "Checksum: $(cat $PACKAGE_NAME.sha256)"
log_info ""
log_info "To deploy:"
log_info "1. Upload $PACKAGE_NAME and $PACKAGE_NAME.sha256 to your server"
log_info "2. On the server, run: tar -xzf $PACKAGE_NAME && cd dist && sudo ./deployment/deploy.sh"