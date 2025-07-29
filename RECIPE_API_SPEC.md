# Recipe API Specification

This document provides a comprehensive API specification for the recipe management endpoints in the cooking application.

## Base URLs

- **Regular Endpoints**: `http://localhost:5000/api/recipes`
- **Secure Endpoints**: `http://localhost:5000/api/secure/recipes`

## Authentication

### Secure Endpoints
Secure endpoints require:
1. **Local Machine Access**: Requests must originate from localhost/127.0.0.1
2. **API Token**: Valid token in the `Authorization` header as `Bearer <token>`

### Token Management

#### Generate API Token
```http
POST /api/secure/token
Content-Type: application/json
Host: localhost (required)

{
  "expires_in_hours": 24  // Optional, default: 24, max: 720 (30 days)
}
```

**Response (201 Created):**
```json
{
  "message": "API token generated successfully",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires_at": "2025-07-30T09:45:10.427Z",
  "expires_in_hours": 24
}
```

#### Revoke API Token
```http
POST /api/secure/token/revoke
Content-Type: application/json
Host: localhost (required)

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Recipe Data Structure

### Recipe Object
```json
{
  "id": 1,
  "name": "Scrambled Eggs",
  "description": "Simple and delicious scrambled eggs",
  "ingredients": [
    {
      "name": "eggs",
      "quantity": "3 large"
    },
    {
      "name": "butter",
      "quantity": "1 tbsp"
    }
  ],
  "instructions": [
    "Crack eggs into a bowl and whisk",
    "Heat butter in a pan over medium heat",
    "Add eggs and stir gently until set"
  ],
  "image_url": null,
  "tags": ["breakfast", "quick", "easy"],
  "difficulty": "Easy",
  "cuisine": "American",
  "prep_time_minutes": 5,
  "cook_time_minutes": 5,
  "servings": 2,
  "created_at": "2025-07-29T09:45:10.427Z",
  "updated_at": "2025-07-29T09:45:10.427Z"
}
```

### Request Payload Structure
All create and update requests must wrap the recipe data in a `recipeData` object:

```json
{
  "recipeData": {
    "name": "Recipe Name",
    "description": "Recipe description",
    "ingredients": [...],
    "instructions": [...],
    // ... other fields
  }
}
```

## Create Recipe

### Regular Endpoint
```http
POST /api/recipes/
Content-Type: application/json

{
  "recipeData": {
    "name": "Scrambled Eggs",
    "description": "Simple and delicious scrambled eggs",
    "ingredients": [
      {
        "name": "eggs",
        "quantity": "3 large"
      },
      {
        "name": "butter", 
        "quantity": "1 tbsp"
      }
    ],
    "instructions": [
      "Crack eggs into a bowl and whisk",
      "Heat butter in a pan over medium heat",
      "Add eggs and stir gently until set"
    ],
    "tags": ["breakfast", "quick", "easy"],
    "difficulty": "Easy",
    "cuisine": "American",
    "prep_time_minutes": 5,
    "cook_time_minutes": 5,
    "servings": 2
  }
}
```

### Secure Endpoint
```http
POST /api/secure/recipes
Content-Type: application/json
Authorization: Bearer <token>
Host: localhost (required)

{
  "recipeData": {
    // Same structure as regular endpoint
  }
}
```

### Required Fields
- `name` (string): Recipe name, cannot be empty
- `ingredients` (array): Non-empty array of ingredient objects
  - Each ingredient must have a `name` field (string, required)
  - `quantity` field is optional (string)
- `instructions` (array): Non-empty array of instruction strings

### Optional Fields
- `description` (string): Recipe description
- `image_url` (string): External image URL
- `tags` (array): Array of tag strings
- `difficulty` (string): Difficulty level
- `cuisine` (string): Cuisine type
- `prep_time_minutes` (number): Preparation time, must be >= 0
- `cook_time_minutes` (number): Cooking time, must be >= 0
- `servings` (number): Number of servings, must be >= 0

### Success Response (201 Created)
```json
{
  "message": "Recipe created successfully",
  "data": {
    "id": 1,
    "name": "Scrambled Eggs",
    "description": "Simple and delicious scrambled eggs",
    "ingredients": [...],
    "instructions": [...],
    "image_url": null,
    "tags": ["breakfast", "quick", "easy"],
    "difficulty": "Easy",
    "cuisine": "American",
    "prep_time_minutes": 5,
    "cook_time_minutes": 5,
    "servings": 2,
    "created_at": "2025-07-29T09:45:10.427Z",
    "updated_at": "2025-07-29T09:45:10.427Z"
  }
}
```

### Error Responses

#### Validation Error (400 Bad Request)
```json
{
  "message": "Validation failed within 'recipeData'",
  "errors": {
    "name": "Missing required field: name",
    "ingredients": [
      {
        "index": 0,
        "errors": {
          "name": "Ingredient 1: Name is required and cannot be empty."
        }
      }
    ],
    "instructions": [
      {
        "index": 1,
        "error": "Instruction must be a non-empty string."
      }
    ],
    "prep_time_minutes": "Prep Time Minutes must be a valid number if provided."
  }
}
```

#### Missing Content Type (415 Unsupported Media Type)
```json
{
  "message": "Request must be application/json."
}
```

#### Empty Request Body (400 Bad Request)
```json
{
  "message": "Request body cannot be empty."
}
```

#### Missing recipeData Field (400 Bad Request)
```json
{
  "message": "Missing or invalid 'recipeData' field in request body."
}
```

#### Server Error (500 Internal Server Error)
```json
{
  "message": "Internal server error creating recipe.",
  "error": "Database connection failed"
}
```

## Update Recipe

### Regular Endpoint
```http
PUT /api/recipes/{id}
Content-Type: application/json

{
  "recipeData": {
    "name": "Updated Recipe Name",
    "description": "Updated description",
    "prep_time_minutes": 10
    // Only include fields you want to update
  }
}
```

### Secure Endpoint
```http
PUT /api/secure/recipes/{id}
Content-Type: application/json
Authorization: Bearer <token>
Host: localhost (required)

{
  "recipeData": {
    // Same structure as regular endpoint
  }
}
```

### Path Parameters
- `id` (integer): Recipe ID to update

### Request Body
- All fields are optional for updates
- Only include fields you want to modify
- Same validation rules apply as create endpoint
- Cannot update `name` to empty string
- Cannot update `ingredients` or `instructions` to empty arrays

### Success Response (200 OK)
```json
{
  "message": "Recipe updated successfully",
  "data": {
    "id": 1,
    "name": "Updated Recipe Name",
    "description": "Updated description",
    // ... complete updated recipe object
    "updated_at": "2025-07-29T10:30:15.123Z"
  }
}
```

### Error Responses

#### Recipe Not Found (404 Not Found)
```json
{
  "message": "Recipe with id 123 not found."
}
```

#### No Update Data (400 Bad Request)
```json
{
  "message": "No data provided for update."
}
```

#### Validation Error (400 Bad Request)
```json
{
  "message": "Validation failed within 'recipeData'",
  "errors": {
    "name": "Name cannot be empty.",
    "ingredients": "Ingredients list cannot be empty if provided for update."
  }
}
```

#### No Changes Made (200 OK)
```json
{
  "message": "Recipe update operation completed, but may not have changed the record (data might be identical or another issue occurred).",
  "data": {
    // Current recipe data
  }
}
```

## Delete Recipe

### Regular Endpoint
```http
DELETE /api/recipes/{id}
```

### Secure Endpoint
```http
DELETE /api/secure/recipes/{id}
Authorization: Bearer <token>
Host: localhost (required)
```

### Path Parameters
- `id` (integer): Recipe ID to delete

### Success Response (200 OK)
```json
{
  "message": "Recipe deleted successfully",
  "data": {
    "id": 123
  }
}
```

### Error Responses

#### Recipe Not Found (404 Not Found)
```json
{
  "message": "Recipe with id 123 not found."
}
```

#### Server Error (500 Internal Server Error)
```json
{
  "message": "Failed to delete recipe due to an unknown database issue."
}
```

## Image Upload

### Regular Endpoint
```http
POST /api/recipes/{id}/image
Content-Type: multipart/form-data

Form Data:
- image: [binary file data]
```

### Secure Endpoint
```http
POST /api/secure/recipes/{id}/image
Content-Type: multipart/form-data
Authorization: Bearer <token>
Host: localhost (required)

Form Data:
- image: [binary file data]
```

### Path Parameters
- `id` (integer): Recipe ID to upload image for

### Form Data
- `image` (file): Image file (PNG, JPG, JPEG, GIF)

### Success Response (201 Created)
```json
{
  "message": "Image uploaded successfully",
  "data": {
    "recipe_id": 123,
    "image_id": 456
  }
}
```

### Error Responses

#### No Image File (400 Bad Request)
```json
{
  "message": "No image file part in the request."
}
```

#### No File Selected (400 Bad Request)
```json
{
  "message": "No selected file."
}
```

#### Invalid File Type (400 Bad Request)
```json
{
  "message": "Invalid file type. Allowed types: png, jpg, jpeg, gif."
}
```

#### Empty File (400 Bad Request)
```json
{
  "message": "Uploaded file is empty."
}
```

## Security Considerations

### Secure Endpoints
- All secure endpoints require requests from localhost/127.0.0.1
- Valid JWT token required in Authorization header
- Tokens have configurable expiration (default 24 hours, max 30 days)
- Tokens can be revoked before expiration

### Regular Endpoints
- No authentication required
- Accessible from any origin
- Suitable for public recipe browsing and creation

### Data Validation
- Comprehensive input validation on all endpoints
- SQL injection protection through parameterized queries
- File type validation for image uploads
- Size limits and empty file checks for uploads

## Rate Limiting
Currently no rate limiting is implemented. Consider adding rate limiting for production use.

## CORS
CORS configuration should be set up appropriately for your frontend domain in production.

## Database Transactions
- Image uploads use database transactions for consistency
- Failed operations are properly rolled back
- Comprehensive error logging for debugging