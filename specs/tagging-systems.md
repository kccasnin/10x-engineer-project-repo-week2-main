Overview and Goals for the Tagging System

Overview: The tagging system in the PromptLab project serves as a mechanism to enhance the organization, categorization, and discovery of prompts. By allowing users to tag prompts with relevant keywords or themes, the system facilitates efficient searching and filtering, improving the overall user experience.

Goals:

1. Enhance Discoverability: Enable users to easily find and access prompts based on specific keywords through tagging.
2. Improve Organization: Allow prompts to be categorized logically using tags, resulting in better structure and navigation within the application.
3. Support Dynamic Interaction: Provide a robust API that supports the creation, retrieval, updating, and deletion of tags, ensuring users can manage their tags effectively.
4. Facilitate Better User Experience: By implementing filtering capabilities based on tags, enhance the usability of the application for users navigating through large sets of prompts.

User Stories with Acceptance Criteria

1. User Story: As a user, I want to create a tag to categorize my prompts.

Acceptance Criteria:
- The system must allow users to create tags with unique names.
- Upon successful creation, a confirmation message must be displayed.

2. User Story: As a user, I want to retrieve a list of all available tags.

Acceptance Criteria:
- An API endpoint must return a list of all tags, including their names and IDs.
- The response must be properly formatted in JSON.

3. User Story: As a user, I want to filter prompts by specific tags.

Acceptance Criteria:
- An API endpoint must exist that accepts one or more tag IDs as input.
- The endpoint should return only prompts that are associated with the specified tag(s).

4. User Story: As a user, I want to delete a tag that is no longer relevant.

Acceptance Criteria:
- The system must allow users to delete tags only if they are not associated with any prompts.
- If a tag is in use, the user must receive an appropriate error message.

Data Model Changes Needed

Tag Model

class Tag(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    created_at: datetime = Field(default_factory=get_current_time)

Prompt-Tag Association Model

class PromptTagAssociation(BaseModel):
    prompt_id: str
    tag_id: str

Individual API Endpoints

1. Create Tag

Endpoint: POST /tags
Request Body:

{
  "name": "Review"
}
Response:

{
  "id": "tag_id",
  "name": "Review",
  "created_at": "2023-10-01T12:00:00Z"
}

2. Retrieve Tags

Endpoint: GET /tags
Response:

[
  {
    "id": "tag_id",
    "name": "Review",
    "created_at": "2023-10-01T12:00:00Z"
  },
  {
    "id": "tag_id_2",
    "name": "Enhancement",
    "created_at": "2023-10-01T12:00:00Z"
  }
]

3. Filter Prompts by Tags

Endpoint: GET /prompts
Query Parameters: tags=[tag_id_1,tag_id_2]
Response:

{
  "prompts": [
    {
      "id": "prompt_id",
      "title": "Sample Prompt",
      "content": "Prompt content.",
      "tags": ["tag_id_1"]
    }
  ],
  "total": 1
}

4. Delete Tag

Endpoint: DELETE /tags/{tag_id}
Response:
204 No Content: Indicates successful deletion.

Error Conditions and Edge Cases

1. Error Condition: Attempting to create a tag with a duplicate name.

Response: 400 Bad Request
Message: "Tag name must be unique."

2. Error Condition: Attempting to delete a tag that is currently associated with prompts.

Response: 409 Conflict
Message: "Cannot delete tag that is in use."

3. Edge Case: Attempting to filter prompts by tags that do not exist.

Response: 404 Not Found
Message: "Tag not found."

4. Edge Case: Attempting to retrieve a list of tags when no tags exist.

Response: 200 OK
Message: [] (an empty list as there are no tags).
