# backend/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.api import app  # Ensure the API is correctly imported
from app.models import Tag

# Create a test client fixture for FastAPI
@pytest.fixture
def client() -> TestClient:
    """Create a test client for the API."""
    return TestClient(app)

class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        print(response.json())  # Debug: Print the response JSON for inspection
        assert response.status_code == 200

       # Update the assertion to reflect expected response structure
        data = response.json()
        #assert isinstance(data, dict)  # Ensure it's a dictionary
        #assert "prompts" in data  # Ensure the 'prompts' key exists in the response
        assert data["prompts"] == []  # Check that the prompts list is empty
        assert data["total"] == 0  # Check that the total number of prompts is zero
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204

        get_response = client.get(f"/prompts/{prompt_id}")
        assert get_response.status_code == 404

    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        updated_data = {
            "title": "Updated Sample Prompt",
            "content": "Updated content.",
            "description": "Updated description."
        }
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Sample Prompt"

    def test_validation_error_create_prompt(self, client: TestClient):
        # Missing required fields
        response = client.post("/prompts", json={})
        assert response.status_code == 422  # Unprocessable Entity

    def test_special_characters_in_title(self, client: TestClient, sample_prompt_data):
        """Test creating a prompt with special characters in the title."""
        # Modifying the sample data to include special characters
        sample_prompt_data["title"] = "Title! @ # $ % ^ & *"

        response = client.post("/prompts", json=sample_prompt_data)

        # You can check for a successful creation if required
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]  # Ensure title was stored correctly


class TestCollections:
    """Tests for collection endpoints."""
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts."""
        
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]

        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_data)

       # Delete collection
        client.delete(f"/collections/{collection_id}")

        # Verify that the prompt still exists but is no longer associated with the collection
        prompts_response = client.get("/prompts")
        assert prompts_response.status_code == 200
        prompts = prompts_response.json()["prompts"]
        
        assert len(prompts) == 1  # Ensure one prompt exists
        assert prompts[0]["collection_id"] is None  # Check that the collection_id for the prompt is None or empty


class TestTags:
    """Tests for tag endpoints."""

    def test_create_tag(self, client: TestClient):
        """Test creating a new tag with valid data."""

        # Arrange: Define the request body for creating a new tag.
        new_tag_data = {"name": "Sample Tag"}

        # Act: Make the POST request to the create_tag endpoint.
        response = client.post("/tags", json=new_tag_data)
        # Assert: Check the response status code and body.
        assert response.status_code == 200  # Expecting a 200 Created response
        data = response.json()
        assert data["name"] == "Sample Tag"  # The name should match
        assert "id" in data  # Ensure that an ID is returned
        assert "created_at" in data  # Ensure a created_at timestamp is present
    
    def test_create_duplicate_tag(self, client: TestClient):
        """Test creating a tag with a duplicate name."""
        # First, create the tag
        
        new_tag_data = {"name": "Duplicate Tag"}
        client.post("/tags", json=new_tag_data)

        # Act: Attempt to create the same tag again
        response = client.post("/tags", json=new_tag_data)

        # Assert: Check for a 400 Bad Request due to duplication
        assert response.status_code == 400  # Expecting a 400 Bad Request
        assert response.json() == {"detail": "Tag name must be unique."}  # Error message expected

    def test_create_tag_empty_name(self, client: TestClient):
        """Test creating a tag with an empty name."""
        # Act: Attempt to create a tag with an empty name
        response = client.post("/tags", json={"name": ""})

        # Assert: Expect a 400 Bad Request for empty name
        assert response.status_code == 400  # Expecting a 400 Bad Request
        assert response.json() == {"detail": "Tag name must be provided."}  # Expected error message
    
    def test_get_tags(self, client: TestClient):
        """Test retrieving all tags after creation."""
        # Create a new tag
        client.post("/tags", json={"name": "Tag 1"})
        client.post("/tags", json={"name": "Tag 2"})

        # Act: Retrieve all tags
        response = client.get("/tags")

        # Assert: Check response contains the created tags
        assert response.status_code == 200  # Expecting a 200 OK response
        data = response.json()
        assert len(data) == 2  # Expecting two tags
        assert any(tag["name"] == "Tag 1" for tag in data)  # Check for Tag 1
        assert any(tag["name"] == "Tag 2" for tag in data)  # Check for Tag 2

    def test_filter_prompts_by_tags(self, client: TestClient):
        """Test filtering prompts by tags."""
        # Create a tag first
        tag_response = client.post("/tags", json={"name": "Sample Tag"})
        tag_id = tag_response.json()["id"]

        # Create a prompt associated with the tag
        prompt_data = {
           "title": "Prompt with Tag",
            "content": "This is a prompt associated with the tag.",
            "description": "Valid description.",
            "collection_id": None  # Assuming no collection association for this test
        }
        client.post("/prompts", json=prompt_data)  # Add prompt

        # Act: Retrieve prompts filtered by the created tag
        response = client.get(f"/prompts?tags={tag_id}")

        # Assert: Check if the prompt is returned
        assert response.status_code == 201
        data = response.json()
        assert "prompts" in data  # Ensure prompt list is present
        assert isinstance(data["prompts"], list)  # Check that prompts is a list
        assert len(data["prompts"]) == 1  # Expect one prompt
        assert data["prompts"][0]["title"] == "Prompt with Tag"  # Verify correct prompt title


class TestTags:
    """Tests for tag endpoints based on tagging-systems.md specifications."""

    def test_create_tag_all_info(self, client: TestClient):
        """Test creating a new tag with all valid info provided."""
        new_tag_data = {"name": "Review"}
        response = client.post("/tags", json=new_tag_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Review"
        assert "id" in data
        assert "created_at" in data

    def test_create_tag_missing_info(self, client: TestClient):
        """Test creating a tag with missing name (partial/missing info)."""
        response = client.post("/tags", json={})
        
        # Should fail validation (422 Unprocessable Entity)
        assert response.status_code == 422

    def test_create_tag_empty_name(self, client: TestClient):
        """Test creating a tag with an empty string as name."""
        response = client.post("/tags", json={"name": ""})
        
        # Depending on implementation, Pydantic might catch this (422) 
        # or custom validation in the endpoint (400)
        assert response.status_code in [400, 422]

    def test_create_duplicate_tag(self, client: TestClient):
        """Test creating a tag with a duplicate name."""
        client.post("/tags", json={"name": "Duplicate Tag"})
        response = client.post("/tags", json={"name": "Duplicate Tag"})
        
        assert response.status_code == 400
        assert response.json() == {"detail": "Tag name must be unique."}

    def test_retrieve_tags_empty(self, client: TestClient):
        """Test retrieving tags when none exist (edge case)."""
        response = client.get("/tags")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_retrieve_tags_with_data(self, client: TestClient):
        """Test retrieving all tags after creation."""
        client.post("/tags", json={"name": "Tag 1"})
        client.post("/tags", json={"name": "Tag 2"})
        
        response = client.get("/tags")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(tag["name"] == "Tag 1" for tag in data)
        assert any(tag["name"] == "Tag 2" for tag in data)

    def test_filter_prompts_by_tags(self, client: TestClient):
        """Test filtering prompts by specific tags."""
        # Create a tag
        tag_response = client.post("/tags", json={"name": "Sample Tag"})
        tag_id = tag_response.json()["id"]

        # Create a prompt (assuming prompt creation supports tags or we mock it)
        # Note: If your PromptCreate model doesn't support tags yet, this might need adjustment
        # in your models/api to accept a list of tag IDs.
        prompt_data = {
            "title": "Prompt with Tag",
            "content": "This is a prompt associated with the tag.",
            "description": "Valid description.",
            "tags": [tag_id]
        }
        client.post("/prompts", json=prompt_data)

        # Act: Retrieve prompts filtered by the created tag
        response = client.get(f"/prompts?tags={tag_id}")

        # Assert: Check if the prompt is returned
        assert response.status_code == 200
        data = response.json()
        assert "prompts" in data
        assert isinstance(data["prompts"], list)
        assert len(data["prompts"]) == 1
        assert data["prompts"][0]["title"] == "Prompt with Tag"

    def test_filter_prompts_by_nonexistent_tag(self, client: TestClient):
        """Test filtering prompts by a tag that does not exist (edge case)."""
        response = client.get("/prompts?tags=nonexistent-tag-id")
        
        assert response.status_code == 404
        assert response.json() == {"detail": "Tag not found."}

    def test_delete_tag_success(self, client: TestClient):
        """Test deleting a tag that is not associated with any prompts."""
        create_response = client.post("/tags", json={"name": "Unused Tag"})
        tag_id = create_response.json()["id"]
        
        response = client.delete(f"/tags/{tag_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get("/tags")
        assert len(get_response.json()) == 0

    def test_delete_tag_in_use(self, client: TestClient):
        """Test deleting a tag that is currently associated with prompts."""
        tag_response = client.post("/tags", json={"name": "In Use Tag"})
        tag_id = tag_response.json()["id"]
        
        # Create a prompt associated with the tag
        prompt_data = {
            "title": "Prompt with Tag",
            "content": "This is a prompt associated with the tag.",
            "description": "Valid description.",
            "tags": [tag_id]
        }
        client.post("/prompts", json=prompt_data)

        # Attempt to delete the tag
        response = client.delete(f"/tags/{tag_id}")
        
        assert response.status_code == 409
        assert response.json() == {"detail": "Cannot delete tag that is in use."}
