# PromptLab - AI Prompt Engineering Platform

## Project Overview
PromptLab is an AI Prompt Engineering platform that allows users to create, manage, and utilize prompts for AI models. The application provides an API for interacting with prompts and collections, facilitating a user-friendly experience for developers and AI enthusiasts alike.

## Features
- Create, read, update, and delete prompts and collections.
- Health check endpoint to monitor API status.
- Support for filtering and searching prompts by collection or by content.
- In-memory storage for easy testing and deployment.
- Comprehensive testing setup using pytest.

## Prerequisites
- Python 3.7 or higher
- `pip` for Python package management

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/promptlab.git
   cd promptlab
   ```
2. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn pytest
   ```

## Quick Start Guide
To start the API server, run the following command:
```bash
python backend/main.py
```
The server will be running at `http://0.0.0.0:8000`.

## API Endpoint Summary
### Health Check
- **Endpoint:** `GET /health`
- **Description:** Check the health status of the API.
- **Response:**
  ```json
  {
    "status": "healthy",
    "version": "0.1.0"
  }
  ```

### Prompts
- **Create Prompt**
  - **Endpoint:** `POST /prompts`
  - **Request Body:**
    ```json
    {
      "title": "Prompt Title",
      "content": "Prompt content goes here.",
      "description": "A brief description."
    }
    ```
  - **Response:** `201 Created` with the created prompt details.

- **List Prompts**
  - **Endpoint:** `GET /prompts`
  - **Response:**
    ```json
    {
      "prompts": [],
      "total": 0
    }
    ```

- **Get Prompt by ID**
  - **Endpoint:** `GET /prompts/{prompt_id}`
  - **Response:** `200 OK` with prompt details.

- **Update Prompt**
  - **Endpoint:** `PUT /prompts/{prompt_id}`
  - **Request Body:** Similar to Create Prompt
  - **Response:** Updated prompt details.

- **Delete Prompt**
  - **Endpoint:** `DELETE /prompts/{prompt_id}`
  - **Response:** `204 No Content` upon successful deletion.

### Collections
- **Create Collection**
  - **Endpoint:** `POST /collections`
  - **Request Body:**
    ```json
    {
      "name": "Collection Name",
      "description": "Description of the collection."
    }
    ```
  - **Response:** `201 Created` with the created collection details.

- **List Collections**
  - **Endpoint:** `GET /collections`
  - **Response:** Similar to List Prompts.

- **Get Collection by ID**
  - **Endpoint:** `GET /collections/{collection_id}`
  - **Response:** Details of the collection.

- **Delete Collection**
  - **Endpoint:** `DELETE /collections/{collection_id}`
  - **Response:** `204 No Content` upon successful deletion.

## Development Setup
1. Ensure you have Python and pip installed.
2. Use a virtual environment for isolating dependencies (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies as per the installation section.
4. Run tests using pytest:
   ```bash
   pytest backend/tests
   ```

## Contributing Guidelines
We welcome contributions! Please adhere to the following guidelines:
- Fork the repository and create a new branch for each feature or bugfix.
- Make sure your code passes all tests.
- Include tests for new features.
- Submit a pull request with a descriptive title and a summary of changes.

For extensive contributions, please refer to our [Code of Conduct](CODE_OF_CONDUCT.md) and [Contribution Guidelines](CONTRIBUTING.md).

