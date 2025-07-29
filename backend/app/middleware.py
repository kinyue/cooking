# backend/app/middleware.py
# Middleware functions for security and access control

import functools
from flask import request, jsonify, current_app
import socket
import secrets
import os
from datetime import datetime, timedelta

# Dictionary to store valid API tokens with expiration times
# Format: {token: expiration_datetime}
VALID_TOKENS = {}

def get_local_ip_addresses():
    """Get all local IP addresses of the machine."""
    local_ips = set(['127.0.0.1', '::1'])  # Always include localhost
    
    try:
        # Get all network interfaces
        hostname = socket.gethostname()
        local_ips.add(socket.gethostbyname(hostname))
        
        # Try to get all addresses
        for info in socket.getaddrinfo(hostname, None):
            local_ips.add(info[4][0])
    except Exception as e:
        current_app.logger.warning(f"Error getting local IP addresses: {e}")
    
    return local_ips

def local_only(f):
    """Decorator to restrict access to local machine only."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Get client IP
        client_ip = request.remote_addr
        
        # Get all local IPs
        local_ips = get_local_ip_addresses()
        
        # Check if client IP is local
        if client_ip not in local_ips:
            current_app.logger.warning(f"Unauthorized access attempt from {client_ip}")
            return jsonify({
                "error": "Access denied",
                "message": "This API endpoint can only be accessed from the local machine"
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def generate_api_token(expires_in_hours=24):
    """Generate a secure API token that expires after the specified hours."""
    token = secrets.token_urlsafe(32)
    expiration = datetime.now() + timedelta(hours=expires_in_hours)
    VALID_TOKENS[token] = expiration
    return token, expiration

def validate_token(token):
    """Validate if a token exists and has not expired."""
    if token not in VALID_TOKENS:
        return False
    
    expiration = VALID_TOKENS[token]
    if datetime.now() > expiration:
        # Token has expired, remove it
        VALID_TOKENS.pop(token, None)
        return False
    
    return True

def revoke_token(token):
    """Revoke a token by removing it from valid tokens."""
    if token in VALID_TOKENS:
        VALID_TOKENS.pop(token)
        return True
    return False

def token_required(f):
    """Decorator to require a valid API token."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for token in header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "Unauthorized",
                "message": "API token is missing or invalid"
            }), 401
        
        token = auth_header.split(' ')[1]
        
        if not validate_token(token):
            return jsonify({
                "error": "Unauthorized",
                "message": "API token is invalid or has expired"
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

def secure_api_required(f):
    """Combined decorator for both local-only and token authentication."""
    @functools.wraps(f)
    @local_only
    @token_required
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function