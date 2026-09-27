# backend/tests/test_api.py
import pytest
from fastapi.testclient import TestClient


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
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
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

    def test_special_characters_in_title(self, client: TestClient):
        # Create a prompt with special characters
        sample_prompt_data["title"] = "Title! @ # $ % ^ & *"
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201


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
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_data)
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204
        
        prompts = client.get("/prompts").json()["prompts"]
        assert len(prompts) == 1  # The prompt still exists but is orphaned


class TestTags:
    """Tests for tag endpoints."""

    def test_create_tag(self, client: TestClient):
        response = client.post("/tags", json={"name": "Sample Tag"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Sample Tag"
        assert "id" in data

    def test_create_duplicate_tag(self, client: TestClient):
        client.post("/tags", json={"name": "Duplicate Tag"})
        response = client.post("/tags", json={"name": "Duplicate Tag"})
        assert response.status_code == 400  # Bad Request

    def test_get_tags(self, client: TestClient):
        client.post("/tags", json={"name": "Sample Tag"})
        response = client.get("/tags")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_delete_tag_used(self, client: TestClient):
        client.post("/tags", json={"name": "Tag In Use"})
        # Assuming you have logic to associate this tag with prompts
        response = client.delete("/tags/tag_id_in_use")
        assert response.status_code == 409  # Cannot delete tag that is in use

