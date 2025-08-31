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
    The frontend application will be running at `http://localhost:58080/`.

## Secure API Endpoints

The application provides secure API endpoints for recipe management that are restricted to local machine access only. These endpoints require both local machine access and a valid API token for authentication.

### Security Features

1. **Local Machine Access Control**: All secure endpoints can only be accessed from the local machine (localhost or local IP addresses).
2. **Token-based Authentication**: A valid API token must be provided in the Authorization header.
3. **Token Expiration**: Tokens automatically expire after a configurable time period (default: 24 hours).

### Token Management

#### Generating a Token

To generate a new API token (only accessible from the local machine):

**Linux/macOS (Bash):**
```bash
curl -X POST http://127.0.0.1:5000/api/secure/token \
  -H "Content-Type: application/json" \
  -d '{"expires_in_hours": 24}'
```

**Windows (PowerShell):**
```powershell
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    "expires_in_hours" = 24
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/secure/token" -Headers $headers -Body $body
```

**Windows (CMD):**
```cmd
curl -X POST http://127.0.0.1:5000/api/secure/token -H "Content-Type: application/json" -d "{\"expires_in_hours\": 24}"
```

The response will include your token and expiration information:
```json
{
  "message": "API token generated successfully",
  "token": "your_generated_token",
  "expires_at": "2025-07-28T02:15:00.000Z",
  "expires_in_hours": 24
}
```

#### Revoking a Token

To revoke an existing token (only accessible from the local machine):

**Linux/macOS (Bash):**
```bash
curl -X POST http://127.0.0.1:5000/api/secure/token/revoke \
  -H "Content-Type: application/json" \
  -d '{"token": "your_token_to_revoke"}'
```

**Windows (PowerShell):**
```powershell
$headers = @{
    "Content-Type" = "application/json"
}
$body = @{
    "token" = "your_token_to_revoke"
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/secure/token/revoke" -Headers $headers -Body $body
```

**Windows (CMD):**
```cmd
curl -X POST http://127.0.0.1:5000/api/secure/token/revoke -H "Content-Type: application/json" -d "{\"token\": \"your_token_to_revoke\"}"
```

### Recipe Management Endpoints

All secure recipe endpoints require:
1. Access from the local machine
2. A valid API token in the Authorization header

#### Create a Recipe

**Linux/macOS (Bash):**
```bash
curl -X POST http://127.0.0.1:5000/api/secure/recipes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_token" \
  -d '{
    "recipeData": {
      "name": "Pasta Carbonara",
      "description": "Classic Italian pasta dish",
      "ingredients": [
        {"name": "Spaghetti", "quantity": "200g"},
        {"name": "Eggs", "quantity": "2"},
        {"name": "Pancetta", "quantity": "100g"},
        {"name": "Parmesan cheese", "quantity": "50g"},
        {"name": "Black pepper", "quantity": "to taste"}
      ],
      "instructions": [
        "Cook pasta according to package instructions",
        "Fry pancetta until crispy",
        "Beat eggs with grated cheese",
        "Mix everything together off the heat"
      ],
      "tags": ["Italian", "Pasta", "Quick"],
      "difficulty": "Medium",
      "prep_time_minutes": 10,
      "cook_time_minutes": 15,
      "servings": 2
    }
  }'
```

**Windows (PowerShell):**
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer your_api_token"
}
$body = @{
    recipeData = @{
        name = "Pasta Carbonara"
        description = "Classic Italian pasta dish"
        ingredients = @(
            @{name = "Spaghetti"; quantity = "200g"},
            @{name = "Eggs"; quantity = "2"},
            @{name = "Pancetta"; quantity = "100g"},
            @{name = "Parmesan cheese"; quantity = "50g"},
            @{name = "Black pepper"; quantity = "to taste"}
        )
        instructions = @(
            "Cook pasta according to package instructions",
            "Fry pancetta until crispy",
            "Beat eggs with grated cheese",
            "Mix everything together off the heat"
        )
        tags = @("Italian", "Pasta", "Quick")
        difficulty = "Medium"
        prep_time_minutes = 10
        cook_time_minutes = 15
        servings = 2
    }
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/secure/recipes" -Headers $headers -Body $body
```

**Windows (CMD):**
```cmd
curl -X POST http://127.0.0.1:5000/api/secure/recipes -H "Content-Type: application/json" -H "Authorization: Bearer your_api_token" -d "{\"recipeData\": {\"name\": \"Pasta Carbonara\", \"description\": \"Classic Italian pasta dish\", \"ingredients\": [{\"name\": \"Spaghetti\", \"quantity\": \"200g\"}, {\"name\": \"Eggs\", \"quantity\": \"2\"}, {\"name\": \"Pancetta\", \"quantity\": \"100g\"}, {\"name\": \"Parmesan cheese\", \"quantity\": \"50g\"}, {\"name\": \"Black pepper\", \"quantity\": \"to taste\"}], \"instructions\": [\"Cook pasta according to package instructions\", \"Fry pancetta until crispy\", \"Beat eggs with grated cheese\", \"Mix everything together off the heat\"], \"tags\": [\"Italian\", \"Pasta\", \"Quick\"], \"difficulty\": \"Medium\", \"prep_time_minutes\": 10, \"cook_time_minutes\": 15, \"servings\": 2}}"
```

#### Update a Recipe

**Linux/macOS (Bash):**
```bash
curl -X PUT http://127.0.0.1:5000/api/secure/recipes/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_token" \
  -d '{
    "recipeData": {
      "name": "Updated Pasta Carbonara",
      "servings": 4
    }
  }'
```

**Windows (PowerShell):**
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer your_api_token"
}
$body = @{
    recipeData = @{
        name = "Updated Pasta Carbonara"
        servings = 4
    }
} | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri "http://127.0.0.1:5000/api/secure/recipes/1" -Headers $headers -Body $body
```

**Windows (CMD):**
```cmd
curl -X PUT http://127.0.0.1:5000/api/secure/recipes/1 -H "Content-Type: application/json" -H "Authorization: Bearer your_api_token" -d "{\"recipeData\": {\"name\": \"Updated Pasta Carbonara\", \"servings\": 4}}"
```

#### Delete a Recipe

**Linux/macOS (Bash):**
```bash
curl -X DELETE http://127.0.0.1:5000/api/secure/recipes/1 \
  -H "Authorization: Bearer your_api_token"
```

**Windows (PowerShell):**
```powershell
$headers = @{
    "Authorization" = "Bearer your_api_token"
}
Invoke-RestMethod -Method Delete -Uri "http://127.0.0.1:5000/api/secure/recipes/1" -Headers $headers
```

**Windows (CMD):**
```cmd
curl -X DELETE http://127.0.0.1:5000/api/secure/recipes/1 -H "Authorization: Bearer your_api_token"
```

#### Upload a Recipe Image

**Linux/macOS (Bash):**
```bash
curl -X POST http://127.0.0.1:5000/api/secure/recipes/1/image \
  -H "Authorization: Bearer your_api_token" \
  -F "image=@/path/to/your/image.jpg"
```

**Windows (PowerShell):**
```powershell
$headers = @{
    "Authorization" = "Bearer your_api_token"
}
$filePath = "C:\path\to\your\image.jpg"
$fileBytes = [System.IO.File]::ReadAllBytes($filePath)
$fileEnc = [System.Text.Encoding]::GetEncoding('ISO-8859-1').GetString($fileBytes)
$boundary = [System.Guid]::NewGuid().ToString()
$LF = "`r`n"

$bodyLines = (
    "--$boundary",
    "Content-Disposition: form-data; name=`"image`"; filename=`"$(Split-Path $filePath -Leaf)`"",
    "Content-Type: application/octet-stream$LF",
    $fileEnc,
    "--$boundary--$LF"
) -join $LF

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/secure/recipes/1/image" -Method Post -Headers $headers -ContentType "multipart/form-data; boundary=`"$boundary`"" -Body $bodyLines
```

**Windows (CMD):**
```cmd
curl -X POST http://127.0.0.1:5000/api/secure/recipes/1/image -H "Authorization: Bearer your_api_token" -F "image=@C:\path\to\your\image.jpg"
```

### HTTP Status Codes

The API uses standard HTTP status codes to indicate the success or failure of requests:

- **200 OK**: The request was successful
- **201 Created**: A new resource was successfully created
- **400 Bad Request**: The request was malformed or contained invalid data
- **401 Unauthorized**: Authentication failed (missing or invalid token)
- **403 Forbidden**: The client does not have permission to access the resource (non-local access)
- **404 Not Found**: The requested resource was not found
- **415 Unsupported Media Type**: The content type of the request is not supported
- **500 Internal Server Error**: An error occurred on the server

### Security Best Practices

1. **Token Management**: Store tokens securely and revoke them when no longer needed.
2. **Regular Token Rotation**: Generate new tokens periodically for enhanced security.
3. **Secure Communication**: Consider using HTTPS even for local communication.
4. **Minimal Permissions**: Use the secure API only when necessary for administrative tasks.
