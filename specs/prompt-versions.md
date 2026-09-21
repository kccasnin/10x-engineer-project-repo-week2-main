Overview and Goals for Prompt Versioning

Overview: Prompt versioning is a system designed to keep track of changes made to prompts throughout their lifecycle. It allows users and developers to understand how prompts evolve, facilitating better management, rollback capabilities, and historical tracking of modifications.

Goals:

To maintain a structured approach to versioning that adheres to semantic versioning principles (MAJOR.MINOR.PATCH).
To enable users to view the history of prompts, including all changes made over time.
To allow safe rollback to previous versions in case of errors or issues with new versions.
To maintain data integrity and prevent the loss of significant changes across different versions of prompts.

User Stories with Acceptance Criteria

1. User Story: As a user, I want to create a new prompt with an initial version.

Acceptance Criteria:
- When a user creates a new prompt, it should have a version set to 1.0.0.
- The prompt is stored in the system with the correct version associated.

2. User Story: As a user, I want to update a prompt and see the version incremented correctly.

Acceptance Criteria:
- When a prompt is updated, the version should increment according to the changes made:
     - Major changes increase the version to 2.0.0 if the previous version was 1.0.0.
     - Minor changes increase the version to 1.1.0.
     - Patch updates maintain the major and minor version, only incrementing the patch (e.g., 1.0.1).

3. User Story: As a user, I want to retrieve the version history of a prompt.

Acceptance Criteria:
- An API endpoint exists that returns all previous versions of a specific prompt along with timestamps and change descriptions.
- The response includes version numbers and the associated data of each version.

4. User Story: As a user, I want to rollback to a previous version of a prompt.

Acceptance Criteria:
- An API endpoint allows users to restore a prompt to an earlier version.
- The system ensures data integrity after restoration and logs the rollback event.

Data Model Changes Needed

Prompt Model Changes


class Prompt(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    content: str
    description: Optional[str] = None
    collection_id: Optional[str] = None
    version: str = Field(default="1.0.0")  # New field for version tracking

Version History Model


class PromptVersionHistory(BaseModel):
    prompt_id: str
    version: str
    created_at: datetime
    updated_data: str  # Description of changes made

Individual API Endpoints

1. Create Prompt

Endpoint: POST /prompts
Request Body:

{
  "title": "Prompt Title",
  "content": "Prompt content.",
  "description": "Optional description."
}

Response:

{
  "id": "prompt_id",
  "title": "Prompt Title",
  "content": "Prompt content.",
  "description": "Optional description.",
  "version": "1.0.0",
  "created_at": "2023-10-01T12:00:00Z"
}

2. Update Prompt

Endpoint: PUT /prompts/{prompt_id}
Request Body:

{
  "title": "Updated Title",
  "content": "Updated content.",
  "description": "Updated description."
}

Response:

{
  "id": "prompt_id",
  "title": "Updated Title",
  "content": "Updated content.",
  "description": "Updated description.",
  "version": "1.1.0",  // Incremented version
  "created_at": "2023-10-01T12:00:00Z"
}

3. Retrieve Prompt Versions

Endpoint: GET /prompts/{prompt_id}/versions
Response:

[
  {
    "version": "1.0.0",
    "created_at": "2023-10-01T12:00:00Z",
    "updated_data": "Initial creation."
  },
  {
    "version": "1.1.0",
    "created_at": "2023-10-02T14:00:00Z",
    "updated_data": "Updated title and content."
  }
]

4. Rollback to Previous Version

Endpoint: POST /prompts/{prompt_id}/rollback
Request Body:

{
  "version": "1.0.0"
}

Response:

{
  "id": "prompt_id",
  "title": "Prompt Title",
  "content": "Previous content from version 1.0.0",
  "description": "Previous description.",
  "version": "1.0.0",
  "created_at": "2023-10-01T12:00:00Z"
}

Error Conditions and Edge Cases

1. Error Condition: Attempting to update to a version that does not exist.

Response: 404 Not Found
Message: "Prompt version not found."

2. Error Condition: Invalid version format during update or rollback.

Response: 400 Bad Request
Message: "Invalid version format."

3. Edge Case: Restoring to a version that has dependencies or linked entities undergoing change.

Response: 409 Conflict
Message: "Cannot restore to the specified version due to conflicting updates."

4. Edge Case: Attempting to retrieve history for a nonexistent prompt.

Response: 404 Not Found
Message: "Prompt not found."