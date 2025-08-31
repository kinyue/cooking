#!/bin/bash
# Startup script for cooking app

# Exit on error
set -e

# Configuration
APP_NAME="cooking-app"
DEPLOY_DIR="/opt/$APP_NAME"
LOG_DIR="/opt/$APP_NAME"/logs
BACKEND_PORT=5000
FRONTEND_PORT=58080

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

# Check if running as the correct user
if [[ $(whoami) != "lance" ]]; then
   log_error "This script must be run as user 'lance'"
   exit 1
fi

# Create log directory if it doesn't exist
mkdir -p $LOG_DIR

# Function to start backend
start_backend() {
    log_info "Starting backend on port $BACKEND_PORT"
    
    # Check if backend is already running
    log_info "Checking for existing backend process..."
    if pgrep -f "gunicorn.*:$BACKEND_PORT" > /dev/null; then
        log_warn "Backend is already running"
        return 0
    fi
    
    # Navigate to backend directory
    cd $DEPLOY_DIR/backend
    
    # Start backend with logging
    nohup $DEPLOY_DIR/venv/bin/gunicorn --bind 0.0.0.0:$BACKEND_PORT --workers 3 --timeout 120 app:create_app() > $LOG_DIR/backend.log 2> $LOG_DIR/backend-error.log &
    
    # Check if backend started successfully
    sleep 3
    log_info "Checking if backend started on port $BACKEND_PORT..."
    if pgrep -f "gunicorn.*:$BACKEND_PORT" > /dev/null; then
        log_info "Backend started successfully"
    else
        log_error "Failed to start backend"
        cat $LOG_DIR/backend-error.log
        exit 1
    fi
}

# Function to start frontend
start_frontend() {
    log_info "Starting frontend on port $FRONTEND_PORT"
    
    # Check if frontend is already running
    log_info "Checking for existing frontend process..."
    if pgrep -f "python3.*http.server.*$FRONTEND_PORT" > /dev/null; then
        log_warn "Frontend is already running"
        return 0
    fi
    
    # Navigate to frontend directory
    cd $DEPLOY_DIR/frontend
    
    # Start frontend with logging
    nohup python3 -m http.server $FRONTEND_PORT --directory $DEPLOY_DIR/frontend/dist --bind 0.0.0.0 > $LOG_DIR/frontend.log 2> $LOG_DIR/frontend-error.log &
    
    # Check if frontend started successfully
    sleep 5
    log_info "Checking if frontend started on port $FRONTEND_PORT..."
    if pgrep -f "python3.*http.server.*$FRONTEND_PORT" > /dev/null; then
        log_info "Frontend started successfully"
    else
        log_error "Failed to start frontend"
        cat $LOG_DIR/frontend-error.log
        exit 1
    fi
}

# Function to stop services
stop_services() {
    log_info "Stopping services"
    
    # Stop backend
    if pgrep -f "gunicorn.*:$BACKEND_PORT" > /dev/null; then
        pkill -f "gunicorn.*:$BACKEND_PORT"
        log_info "Backend stopped"
    else
        log_warn "Backend is not running"
    fi
    
    # Stop frontend
    if pgrep -f "python3.*http.server.*$FRONTEND_PORT" > /dev/null; then
        pkill -f "python3.*http.server.*$FRONTEND_PORT"
        log_info "Frontend stopped"
    else
        log_warn "Frontend is not running"
    fi
}

# Function to check status
check_status() {
    log_info "Checking service status"
    
    # Check backend
    if pgrep -f "gunicorn.*:$BACKEND_PORT" > /dev/null; then
        log_info "Backend is running on port $BACKEND_PORT"
    else
        log_warn "Backend is not running"
    fi
    
    # Check frontend
    if pgrep -f "python3.*http.server.*$FRONTEND_PORT" > /dev/null; then
        log_info "Frontend is running on port $FRONTEND_PORT"
    else
        log_warn "Frontend is not running"
    fi
}

# Main script logic
case "$1" in
    start)
        start_backend
        start_frontend
        log_info "All services started successfully"
        log_info "Frontend is accessible at http://$(hostname -I | awk '{print $1}')"
        ;;
    stop)
        stop_services
        log_info "All services stopped"
        ;;
    restart)
        stop_services
        sleep 2
        start_backend
        start_frontend
        log_info "All services restarted successfully"
        ;;
    status)
        check_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0