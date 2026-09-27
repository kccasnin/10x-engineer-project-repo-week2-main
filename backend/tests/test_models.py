# backend/tests/test_models.py

import pytest
from datetime import datetime
from app.models import Prompt, Collection, PromptCreate, PromptUpdate

# Test Data
valid_prompt_data = {
    "title": "Valid Prompt",
    "content": "This is a valid prompt content.",
    "description": "A valid description."
}

valid_collection_data = {
    "name": "Valid Collection",
    "description": "A collection for prompts."
}

invalid_prompt_data_short_title = {
    "title": "",
    "content": "This is a valid prompt content.",
    "description": "A valid description."
}

invalid_prompt_data_empty_content = {
    "title": "Valid Prompt",
    "content": "",
    "description": "A valid description."
}

invalid_collection_data_empty_name = {
    "name": "",
    "description": "A valid description."
}

class TestPromptModel:
    """Tests for the Prompt model."""

    def test_prompt_creation(self):
        """Test that a valid prompt can be created."""
        prompt = Prompt(**valid_prompt_data)
        assert prompt.title == valid_prompt_data["title"]
        assert prompt.content == valid_prompt_data["content"]
        assert prompt.description == valid_prompt_data["description"]
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)

    def test_default_id_generation(self):
        """Test that the prompt's ID is generated automatically."""
        prompt = Prompt(**valid_prompt_data)
        assert prompt.id is not None  # Check that ID is assigned

    def test_prompt_validation_empty_title(self):
        """Test that creating a prompt with an empty title raises a validation error."""
        with pytest.raises(ValueError):
            Prompt(**invalid_prompt_data_short_title)

    def test_prompt_validation_empty_content(self):
        """Test that creating a prompt with empty content raises a validation error."""
        with pytest.raises(ValueError):
            Prompt(**invalid_prompt_data_empty_content)

    def test_prompt_serialization(self):
        """Test that the prompt serializes correctly."""
        prompt = Prompt(**valid_prompt_data)
        serialized = prompt.dict()  # Convert to dictionary
        assert serialized["title"] == prompt.title
        assert serialized["content"] == prompt.content
        assert serialized["description"] == prompt.description
        assert "id" in serialized
        assert "created_at" in serialized
        assert "updated_at" in serialized

class TestCollectionModel:
    """Tests for the Collection model."""

    def test_collection_creation(self):
        """Test that a valid collection can be created."""
        collection = Collection(**valid_collection_data)
        assert collection.name == valid_collection_data["name"]
        assert collection.description == valid_collection_data["description"]
        assert isinstance(collection.created_at, datetime)

    def test_default_id_generation(self):
        """Test that the collection's ID is generated automatically."""
        collection = Collection(**valid_collection_data)
        assert collection.id is not None  # Check that ID is assigned

    def test_collection_validation_empty_name(self):
        """Test that creating a collection with an empty name raises a validation error."""
        with pytest.raises(ValueError):
            Collection(**invalid_collection_data_empty_name)

    def test_collection_serialization(self):
        """Test that the collection serializes correctly."""
        collection = Collection(**valid_collection_data)
        serialized = collection.dict()  # Convert to dictionary
        assert serialized["name"] == collection.name
        assert serialized["description"] == collection.description
        assert "id" in serialized
        assert "created_at" in serialized
