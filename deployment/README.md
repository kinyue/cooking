# Cooking App Deployment Guide

This guide explains how to deploy the Cooking App to a Debian Linux server with IP address 192.168.50.60.

## Prerequisites

- Debian Linux server with IP 192.168.50.60
- Root access to the server
- Existing SQLite database file (database.db) in the backend/instance directory

## Deployment Options

### Option 1: Package and Deploy (Recommended)

This option allows you to package the application locally and then deploy only the package to the server.

#### 1. Package the Application

1. Make sure your existing SQLite database file is in the `backend/instance` directory
2. Run the packaging script:
   ```bash
   chmod +x deployment/package.sh
   ./deployment/package.sh
   ```

3. This will create a tar.gz package file (e.g., `cooking-app-20230810-143000.tar.gz`) and a checksum file.

#### 2. Deploy to Server

1. Upload the package and checksum to the server:
   ```bash
   scp cooking-app-*.tar.gz cooking-app-*.sha256 lance@192.168.50.60:/home/lance/
   ```

2. SSH into the server:
   ```bash
   ssh lance@192.168.50.60
   ```

3. Verify the package integrity:
   ```bash
   sha256sum -c cooking-app-*.sha256
   ```

4. Extract the package:
   ```bash
   tar -xzf cooking-app-*.tar.gz
   cd dist
   ```

5. Run the deployment script (requires root privileges):
   ```bash
   sudo chmod +x deployment/deploy.sh
   sudo ./deployment/deploy.sh
   ```

### Option 2: Direct Deployment

This option copies the entire project directory to the server and builds it there.

#### 1. Prepare the Application

1. Make sure your existing SQLite database file is in the `backend/instance` directory
2. Build the application locally:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```

#### 2. Deploy to Server

1. Copy the entire project directory to the server:
   ```bash
   scp -r cooking-app/ lance@192.168.50.60:/home/lance/
   ```

2. SSH into the server:
   ```bash
   ssh lance@192.168.50.60
   ```

3. Navigate to the project directory:
   ```bash
   cd /home/lance/cooking-app
   ```

4. Run the deployment script (requires root privileges):
   ```bash
   sudo chmod +x deployment/deploy.sh
   sudo ./deployment/deploy.sh
   ```

The deployment script will:
- Create necessary directories
- Check and install missing system dependencies (Python, Node.js, npm, nginx)
- Create a Python virtual environment
- Install Python dependencies in the virtual environment
- Build the frontend with production configuration
- Set up the database (using existing database.db if found)
- Configure and start nginx
- Set up systemd services for auto-start on boot

### 3. Manual Service Management

If you need to manually start, stop, or check the status of the services:

#### Using Systemd Services

```bash
# Start services
sudo systemctl start cooking-app-backend.service
sudo systemctl start cooking-app-frontend.service

# Stop services
sudo systemctl stop cooking-app-backend.service
sudo systemctl stop cooking-app-frontend.service

# Check service status
sudo systemctl status cooking-app-backend.service
sudo systemctl status cooking-app-frontend.service

# Enable/disable auto-start on boot
sudo systemctl enable cooking-app-backend.service
sudo systemctl enable cooking-app-frontend.service
sudo systemctl disable cooking-app-backend.service
sudo systemctl disable cooking-app-frontend.service
```

#### Using the Custom Startup Script

```bash
# Make the script executable
chmod +x deployment/start-app.sh

# Start both services
./deployment/start-app.sh start

# Stop both services
./deployment/start-app.sh stop

# Restart both services
./deployment/start-app.sh restart

# Check service status
./deployment/start-app.sh status
```

### 4. Access the Application

After deployment, the application will be accessible at:
- Frontend: http://192.168.50.60
- Backend API: http://192.168.50.60/api

### 5. Log Files

Log files are located in `/var/log/cooking-app/`:
- Backend log: `/var/log/cooking-app/backend.log`
- Backend error log: `/var/log/cooking-app/backend-error.log`
- Frontend log: `/var/log/cooking-app/frontend.log`
- Frontend error log: `/var/log/cooking-app/frontend-error.log`
- Nginx access log: `/var/log/cooking-app/nginx-access.log`
- Nginx error log: `/var/log/cooking-app/nginx-error.log`

## Troubleshooting

### Common Issues

1. **Services not starting**: Check the log files in `/var/log/cooking-app/` for error messages
2. **Port conflicts**: Make sure ports 5000 (backend) and 58080 (frontend) are not in use
3. **Permission issues**: Ensure the lance user has proper permissions to the application directories

### Database Issues

If you need to recreate the database:

```bash
cd /opt/cooking-app/backend
sudo -u lance /opt/cooking-app/venv/bin/python -m flask init-db
sudo -u lance /opt/cooking-app/venv/bin/python -m flask seed-recipes
sudo -u lance /opt/cooking-app/venv/bin/python -m flask seed-images
```

### Nginx Issues

If you need to reload nginx configuration:

```bash
sudo nginx -t  # Test configuration
sudo systemctl reload nginx  # Reload configuration
```

## Updating the Application

### Using Package and Deploy Method (Recommended)

1. Make your changes to the code
2. Create a new package:
   ```bash
   chmod +x deployment/package.sh
   ./deployment/package.sh
   ```
3. Upload the new package to the server:
   ```bash
   scp cooking-app-*.tar.gz lance@192.168.50.60:/home/lance/
   ```
4. SSH into the server and deploy:
   ```bash
   ssh lance@192.168.50.60
   tar -xzf cooking-app-*.tar.gz
   cd dist
   sudo ./deployment/deploy.sh
   ```

### Using Direct Update Method

1. Make your changes to the code
2. Rebuild the frontend if needed:
   ```bash
   cd /opt/cooking-app/frontend
   sudo -u lance npm run build
   ```
3. Restart the services:
   ```bash
   sudo systemctl restart cooking-app-backend.service
   sudo systemctl restart cooking-app-frontend.service
   ```

## Security Notes

- The deployment script sets up basic security headers in nginx
- Consider setting up a firewall (ufw) to restrict access to necessary ports only
- Change the default SECRET_KEY in the backend configuration for production
- Regularly update system packages and dependencies