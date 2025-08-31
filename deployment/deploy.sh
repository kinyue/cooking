#!/bin/bash
# Deployment script for cooking app

# Exit on error
set -e

# Configuration
SERVER_IP="192.168.50.60"
APP_NAME="cooking-app"
DEPLOY_USER="lance" # Change this to your deploy user
DEPLOY_DIR="/opt/$APP_NAME"
SERVICE_DIR="/etc/systemd/system"
LOG_DIR="/opt/$APP_NAME"/logs
PACKAGE_DIR="$(pwd)" # Assuming we're running from the extracted package directory

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

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   log_error "This script must be run as root"
   exit 1
fi

log_info "Starting deployment of $APP_NAME to $SERVER_IP"

# Create deployment user if not exists
if ! id "$DEPLOY_USER" &>/dev/null; then
    log_info "Creating deployment user: $DEPLOY_USER"
    useradd -m -s /bin/bash $DEPLOY_USER
    log_info "User $DEPLOY_USER created"
else
    log_warn "User $DEPLOY_USER already exists"
fi

# Create directories
log_info "Creating deployment directories"
mkdir -p $DEPLOY_DIR
mkdir -p $LOG_DIR
chown -R $DEPLOY_USER:$DEPLOY_USER $DEPLOY_DIR
chown -R $DEPLOY_USER:$DEPLOY_USER $LOG_DIR
log_info "Directories created"

# Install dependencies
log_info "Checking system dependencies"
apt-get update

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a package is installed
package_installed() {
    dpkg -l | grep -q "^ii  $1 "
}

# Check if Python 3 is installed
if ! command_exists python3; then
    log_info "Installing Python 3"
    apt-get install -y python3
else
    log_info "Python 3 is already installed"
fi

# Check if python3-venv is installed
if ! package_installed python3-venv; then
    log_info "Installing python3-venv"
    apt-get install -y python3-venv
else
    log_info "python3-venv is already installed"
fi

# Check if python3-pip is installed
if ! command_exists pip3; then
    log_info "Installing python3-pip"
    apt-get install -y python3-pip
else
    log_info "python3-pip is already installed"
fi

# Check if nginx is installed
if ! package_installed nginx; then
    log_info "Installing nginx"
    apt-get install -y nginx
    # Ensure nginx is in PATH
    export PATH="$PATH:/usr/sbin:/usr/bin"
else
    log_info "nginx is already installed"
    # Ensure nginx is in PATH
    export PATH="$PATH:/usr/sbin:/usr/bin"
fi

# Check if nodejs is installed
if ! command_exists node; then
    log_info "Installing nodejs"
    apt-get install -y nodejs
else
    log_info "nodejs is already installed"
fi

# Check if npm is installed
if ! command_exists npm; then
    log_info "Installing npm"
    apt-get install -y npm
else
    log_info "npm is already installed"
fi

# Copy application files
log_info "Copying application files"

# Copy and verify backend files
log_info "Copying backend files..."
cp -r backend $DEPLOY_DIR/ || {
    log_error "Failed to copy backend files"
    exit 1
}

# Copy and verify frontend files
log_info "Copying frontend files..."
if [ ! -d "frontend/dist" ]; then
    log_error "Frontend dist directory not found. Package may be corrupted."
    exit 1
fi

mkdir -p $DEPLOY_DIR/frontend
cp -r frontend/dist $DEPLOY_DIR/frontend/ || {
    log_error "Failed to copy frontend dist files"
    exit 1
}

# Copy deployment files
log_info "Copying deployment files..."
cp -r deployment $DEPLOY_DIR/ || {
    log_error "Failed to copy deployment files"
    exit 1
}

# Set proper permissions
log_info "Setting permissions..."
chown -R $DEPLOY_USER:$DEPLOY_USER $DEPLOY_DIR || {
    log_error "Failed to set directory permissions"
    exit 1
}

# Frontend should already be built in the dist directory
log_info "Verifying frontend build"
if [ ! -d "$DEPLOY_DIR/frontend/dist" ]; then
    log_error "Frontend build not found in $DEPLOY_DIR/frontend/dist"
    exit 1
fi
log_info "Frontend build verified successfully"

# Create virtual environment and install Python dependencies
log_info "Creating virtual environment and installing Python dependencies"
cd $DEPLOY_DIR
sudo -u $DEPLOY_USER python3 -m venv venv
log_info "Installing Python dependencies from: $DEPLOY_DIR/backend/requirements.txt"
if [ ! -f "$DEPLOY_DIR/backend/requirements.txt" ]; then
    log_error "Cannot find requirements.txt in $DEPLOY_DIR/backend/"
    exit 1
fi
sudo -u $DEPLOY_USER $DEPLOY_DIR/venv/bin/pip install -r backend/requirements.txt

# Set up PYTHONPATH for Flask commands
export PYTHONPATH="$DEPLOY_DIR/backend:$PYTHONPATH"
log_info "Set PYTHONPATH to: $PYTHONPATH"

# Setup database
log_info "Setting up database"
cd $DEPLOY_DIR/backend
if [ ! -f "instance/database.db" ]; then
    log_info "Database not found, initializing new database"
    cd $DEPLOY_DIR/backend
    log_info "Initializing database..."
    sudo -u $DEPLOY_USER PYTHONPATH=$DEPLOY_DIR/backend $DEPLOY_DIR/venv/bin/python -m flask init-db
    if [ $? -ne 0 ]; then
        log_error "Failed to initialize database"
        exit 1
    fi
    
    log_info "Seeding recipes..."
    sudo -u $DEPLOY_USER PYTHONPATH=$DEPLOY_DIR/backend $DEPLOY_DIR/venv/bin/python -m flask seed-recipes
    if [ $? -ne 0 ]; then
        log_error "Failed to seed recipes"
        exit 1
    fi
    
    log_info "Seeding images..."
    sudo -u $DEPLOY_USER PYTHONPATH=$DEPLOY_DIR/backend $DEPLOY_DIR/venv/bin/python -m flask seed-images
    if [ $? -ne 0 ]; then
        log_error "Failed to seed images"
        exit 1
    fi
else
    log_info "Using existing database"
fi

# Install systemd services
log_info "Installing systemd services"
cp $DEPLOY_DIR/deployment/cooking-app-backend.service $SERVICE_DIR/
cp $DEPLOY_DIR/deployment/cooking-app-frontend.service $SERVICE_DIR/

# Reload systemd
systemctl daemon-reload

# Enable services
log_info "Enabling system services..."
systemctl enable cooking-app-backend.service || {
    log_error "Failed to enable backend service"
    exit 1
}
systemctl enable cooking-app-frontend.service || {
    log_error "Failed to enable frontend service"
    exit 1
}

# Configure nginx
log_info "Configuring nginx"
cp $DEPLOY_DIR/deployment/nginx.conf /etc/nginx/sites-available/$APP_NAME
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/$APP_NAME
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
/usr/sbin/nginx -t

# Restart nginx
systemctl restart nginx

# Start services
log_info "Starting services..."
systemctl start cooking-app-backend.service || {
    log_error "Failed to start backend service"
    systemctl status cooking-app-backend.service --no-pager
    exit 1
}

systemctl start cooking-app-frontend.service || {
    log_error "Failed to start frontend service"
    systemctl status cooking-app-frontend.service --no-pager
    exit 1
}

# Check service status
log_info "Checking service status"
systemctl status cooking-app-backend.service --no-pager
systemctl status cooking-app-frontend.service --no-pager

log_info "Deployment completed successfully!"
log_info "The application should be accessible at http://$SERVER_IP:58080"