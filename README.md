# Cooking Project

This project contains a frontend Vue application and a backend Flask API.

## Setup

### Backend

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install dependencies (assuming you have Python and pip installed):
    ```bash
    pip install -r requirements.txt
    ```

### Frontend

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies (assuming you have Node.js and npm installed):
    ```bash
    npm install
    ```

## Running the Application

### Backend

1.  Navigate to the `backend` directory.
2.  Run the Flask development server:
    ```bash
    flask run
    ```
    The backend API will be running at `http://127.0.0.1:5000`.

#### Database Management

1.  Initialize the database (this will clear existing data):
    ```bash
    cd backend && flask init-db
    ```
2.  Seed the database with sample recipe data:
    ```bash
    cd backend && flask seed-recipes
    ```
3.  Seed the database with image data for recipes:
    ```bash
    cd backend && flask seed-images
    ```

### Frontend

1.  Navigate to the `frontend` directory.
2.  Run the Vue development server:
    ```bash
    npm run serve
    ```
    The frontend application will be running at `http://localhost:8080/`.
