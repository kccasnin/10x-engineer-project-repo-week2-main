# backend/tests/test_storage.py

import pytest

from app.models import Collection, Prompt
from app.storage import storage


class TestStorage:
    """Tests for the Storage class functionality."""

    def test_create_prompt(self, sample_prompt_data):
        """Test creating a new prompt."""
        prompt = Prompt(**sample_prompt_data)
        created_prompt = storage.create_prompt(prompt)
        
        assert created_prompt.id == prompt.id
        assert created_prompt.title == prompt.title
        assert created_prompt.content == prompt.content
        assert created_prompt.description == prompt.description

    def test_get_prompt(self, sample_prompt_data):
        """Test retrieving a prompt by ID."""
        prompt = Prompt(**sample_prompt_data)
        storage.create_prompt(prompt)
        
        retrieved_prompt = storage.get_prompt(prompt.id)
        assert retrieved_prompt.id == prompt.id
        assert retrieved_prompt.title == prompt.title

    def test_get_prompt_not_found(self):
        """Test retrieving a non-existent prompt returns None."""
        non_existent_prompt = storage.get_prompt("nonexistent-id")
        assert non_existent_prompt is None

    def test_update_prompt(self, sample_prompt_data):
        """Test updating an existing prompt."""
        prompt = Prompt(**sample_prompt_data)
        storage.create_prompt(prompt)
        
        updated_data = Prompt(id=prompt.id, title="Updated Title", content="Updated Content", description="Updated Description")
        updated_prompt = storage.update_prompt(prompt.id, updated_data)
        
        assert updated_prompt.title == "Updated Title"
        assert updated_prompt.content == "Updated Content"

    def test_delete_prompt(self, sample_prompt_data):
        """Test deleting a prompt."""
        prompt = Prompt(**sample_prompt_data)
        storage.create_prompt(prompt)
        
        assert storage.delete_prompt(prompt.id) is True
        assert storage.get_prompt(prompt.id) is None

    def test_delete_non_existent_prompt(self):
        """Test deleting a non-existent prompt returns False."""
        assert storage.delete_prompt("nonexistent-id") is False

    def test_create_collection(self, sample_collection_data):
        """Test creating a new collection."""
        collection = Collection(**sample_collection_data)
        created_collection = storage.create_collection(collection)

        assert created_collection.id == collection.id
        assert created_collection.name == collection.name
        assert created_collection.description == collection.description

    def test_get_collection(self, sample_collection_data):
        """Test retrieving a collection by ID."""
        collection = Collection(**sample_collection_data)
        storage.create_collection(collection)

        retrieved_collection = storage.get_collection(collection.id)
        assert retrieved_collection.id == collection.id
        assert retrieved_collection.name == collection.name

    def test_get_collection_not_found(self):
        """Test retrieving a non-existent collection returns None."""
        non_existent_collection = storage.get_collection("nonexistent-id")
        assert non_existent_collection is None

    def test_delete_collection(self, sample_collection_data):
        """Test deleting a collection."""
        collection = Collection(**sample_collection_data)
        storage.create_collection(collection)

        assert storage.delete_collection(collection.id) is True
        assert storage.get_collection(collection.id) is None

    def test_delete_non_existent_collection(self):
        """Test deleting a non-existent collection returns False."""
        assert storage.delete_collection("nonexistent-id") is False

    def test_associate_tags_with_prompt(self):
        """Test tag associations with a prompt during create."""
        # Assuming a tagging system where each prompt can be associated with tags
        # This test needs the tagging model to be implemented, thus an example.

    # Edge Cases
    def test_create_prompt_with_empty_title(self):
        """Test creating a prompt with an empty title."""
        with pytest.raises(ValueError):
            storage.create_prompt(Prompt(title="", content="Non-empty content"))

    def test_create_collection_with_empty_name(self):
        """Test creating a collection with an empty name."""
        with pytest.raises(ValueError):
            storage.create_collection(Collection(name="", description="Valid description"))

    def test_get_all_prompts_empty(self):
        """Test retrieving all prompts returns an empty list."""
        assert storage.get_all_prompts() == []

    def test_get_all_collections_empty(self):
        """Test retrieving all collections returns an empty list."""
        assert storage.get_all_collections() == []
