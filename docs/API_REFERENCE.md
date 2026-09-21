API Reference for PromptLab
Overview
This document provides detailed information about the API endpoints available in the PromptLab application, including request formats, example responses, error handling, and authentication notes.

Endpoints
1. Health Check
GET /health
Description
Check the health status of the API.

Request Example
Run
curl -X GET http://localhost:8000/health
Sample Response

Apply
{
  "status": "healthy",
  "version": "0.1.0"
}
Error Codes
None
Authentication
None

2. Create Prompt
POST /prompts
Description
Create a new prompt.

Request Example
Run
curl -X POST http://localhost:8000/prompts \
-H "Content-Type: application/json" \
-d '{
  "title": "Sample Prompt",
  "content": "This is a sample prompt content.",
  "description": "A brief description of the prompt."
}'
Sample Response

Apply
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Sample Prompt",
  "content": "This is a sample prompt content.",
  "description": "A brief description of the prompt.",
  "collection_id": null,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T12:00:00Z"
}
Error Codes
400 Bad Request: Invalid collection ID (if provided).
Authentication
None

3. List Prompts
GET /prompts
Description
Retrieve a list of all prompts.

Request Example
Run
curl -X GET http://localhost:8000/prompts
Sample Response

Apply
{
  "prompts": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Sample Prompt",
      "content": "This is a sample prompt content.",
      "description": "A brief description of the prompt.",
      "collection_id": null,
      "created_at": "2023-10-01T12:00:00Z",
      "updated_at": "2023-10-01T12:00:00Z"
    }
  ],
  "total": 1
}
Error Codes
None
Authentication
None

4. Get Prompt by ID
GET /prompts/{prompt_id}
Description
Retrieve a specific prompt by its ID.

Request Example
Run
curl -X GET http://localhost:8000/prompts/123e4567-e89b-12d3-a456-426614174000
Sample Response

Apply
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Sample Prompt",
  "content": "This is a sample prompt content.",
  "description": "A brief description of the prompt.",
  "collection_id": null,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T12:00:00Z"
}
Error Codes
404 Not Found: Prompt not found.
Authentication
None

5. Update Prompt
PUT /prompts/{prompt_id}
Description
Update an existing prompt.

Request Example
Run
curl -X PUT http://localhost:8000/prompts/123e4567-e89b-12d3-a456-426614174000 \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Sample Prompt",
  "content": "Updated content for the prompt.",
  "description": "Updated description."
}'
Sample Response

Apply
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated Sample Prompt",
  "content": "Updated content for the prompt.",
  "description": "Updated description.",
  "collection_id": null,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T12:05:00Z"
}
Error Codes
404 Not Found: Prompt not found.
400 Bad Request: Invalid collection ID (if provided).
Authentication
None

6. Delete Prompt
DELETE /prompts/{prompt_id}
Description
Delete a prompt by its ID.

Request Example
Run
curl -X DELETE http://localhost:8000/prompts/123e4567-e89b-12d3-a456-426614174000
Sample Response
204 No Content: Successful deletion with no response body.
Error Codes
404 Not Found: Prompt not found.
Authentication
None

7. Create Collection
POST /collections
Description
Create a new collection.

Request Example
Run
curl -X POST http://localhost:8000/collections \
-H "Content-Type: application/json" \
-d '{
  "name": "Sample Collection",
  "description": "A collection for prompt examples."
}'
Sample Response

Apply
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Sample Collection",
  "description": "A collection for prompt examples.",
  "created_at": "2023-10-01T12:00:00Z"
}
Error Codes
400 Bad Request: Invalid data provided.
Authentication
None

8. List Collections
GET /collections
Description
Retrieve a list of all collections.

Request Example
Run
curl -X GET http://localhost:8000/collections
Sample Response

Apply
{
  "collections": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Sample Collection",
      "description": "A collection for prompt examples.",
      "created_at": "2023-10-01T12:00:00Z"
    }
  ],
  "total": 1
}
Error Codes
None
Authentication
None

9. Get Collection by ID
GET /collections/{collection_id}
Description
Retrieve a specific collection by its ID.

Request Example
Run
curl -X GET http://localhost:8000/collections/123e4567-e89b-12d3-a456-426614174000
Sample Response

Apply
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Sample Collection",
  "description": "A collection for prompt examples.",
  "created_at": "2023-10-01T12:00:00Z"
}
Error Codes
404 Not Found: Collection not found.
Authentication
None

10. Delete Collection
DELETE /collections/{collection_id}
Description
Delete a collection by its ID.

Request Example
Run
curl -X DELETE http://localhost:8000/collections/123e4567-e89b-12d3-a456-426614174000
Sample Response
204 No Content: Successful deletion with no response body.
Error Codes
404 Not Found: Collection not found.
Authentication
None

