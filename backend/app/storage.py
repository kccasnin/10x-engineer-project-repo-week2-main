"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""


from app.models import Collection, Prompt, PromptVersionHistory, Tag  # Ensure Tag is imported


class Storage:
    """In-memory storage for prompts and collections.

    This class provides a simple in-memory storage solution for managing 
    prompts and collections within the application. It utilizes dictionaries 
    to store prompts and collections, allowing for efficient retrieval, 
    creation, update, and deletion operations.

    Attributes:
        _prompts (Dict[str, Prompt]): A dictionary mapping prompt IDs to 
        their corresponding Prompt objects.
        _collections (Dict[str, Collection]): A dictionary mapping collection 
        IDs to their corresponding Collection objects.
        _tags (Dict[str, Tag]): A dictionary mapping tag IDs to
        their corresponding Tag objects.
        _prompt_versions (Dict[str, List[PromptVersionHistory]]): A dictionary
        mapping prompt IDs to their version history.
    """
    def __init__(self):
        """Initializes the Storage instance.

        This constructor creates an empty in-memory storage for prompts 
        and collections by initializing three dictionaries:
        - `_prompts`: to store Prompt objects mapped by their unique IDs.
        - `_collections`: to store Collection objects mapped by their 
          unique IDs.
        - `_tags`: to store Tag objects mapped by their unique IDs.
        - `_prompt_versions`: to store version histories for prompts
          mapped by their unique IDs.
        """
        self._prompts: dict[str, Prompt] = {}
        self._collections: dict[str, Collection] = {}
        self._tags: dict[str, Tag] = {}  # Initialize a new dictionary for tags
        self._prompt_versions: dict[str, list[PromptVersionHistory]] = {}  # Initialize for version tracking
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Adds a new prompt to the storage.

        This method stores a given Prompt object in the in-memory storage 
        using its unique identifier as the key. If a prompt with the same 
        ID already exists, it will be overwritten.

        Args:
            prompt (Prompt): The Prompt object to be added to the storage.

        Returns:
            Prompt: The stored Prompt object, which includes its ID 
            and any associated metadata.
        """
        self._prompts[prompt.id] = prompt
        self._record_version(prompt, "Initial creation.")
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Prompt | None:
        """Retrieves a prompt by its unique identifier.

        This method fetches a Prompt object from the in-memory storage 
        using the provided prompt ID. If no prompt with the specified ID 
        exists, it returns None.

        Args:
            prompt_id (str): The unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The Prompt object associated with the given 
            ID if it exists; otherwise, None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> list[Prompt]:
        """Retrieves all prompts stored in memory.

        This method returns a list of all Prompt objects within the 
        in-memory storage.

        Returns:
            List[Prompt]: A list containing all the Prompt objects stored 
            in the storage. This will be empty if no prompts have been created.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Prompt | None:
        """Updates an existing prompt in storage.

        This method updates the details of an existing Prompt object 
        identified by its unique ID. If the prompt with the specified ID 
        does not exist, it returns None.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The updated Prompt object containing new data.

        Returns:
            Optional[Prompt]: The updated Prompt object if the update was 
            successful; otherwise, None if the prompt with the given ID 
            was not found.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        self._record_version(prompt, "Updated prompt.")
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt identified by its unique identifier.

        This method removes a Prompt object from the in-memory storage 
        based on the provided prompt ID. If the prompt with the specified 
        ID exists and is successfully deleted, the method returns True; 
        otherwise, it returns False.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was successfully deleted; otherwise, False.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Adds a new collection to the storage.

        This method stores a given Collection object in the in-memory storage 
        using its unique identifier as the key. If a collection with the same 
        ID already exists, it will be overwritten.

        Args:
            collection (Collection): The Collection object to be added to the storage.

        Returns:
            Collection: The stored Collection object, which includes its ID 
            and any associated metadata.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Collection | None:
        """Retrieves a collection by its unique identifier.

        This method fetches a Collection object from the in-memory storage 
        using the provided collection ID. If no collection with the specified ID 
        exists, it returns None.

        Args:
            collection_id (str): The unique identifier of the collection to retrieve.

        Returns:
            Optional[Collection]: The Collection object associated with the given 
            ID if it exists; otherwise, None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> list[Collection]:
        """Retrieves all collections stored in memory.

        This method returns a list of all Collection objects within the 
        in-memory storage.

        Returns:
            List[Collection]: A list containing all the Collection objects stored 
            in the storage. This will be empty if no collections have been created.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection identified by its unique identifier.

        This method removes a Collection object from the in-memory storage 
        based on the provided collection ID. If the collection with the specified 
        ID exists and is successfully deleted, the method returns True; 
        otherwise, it returns False.

        Args:
            collection_id (str): The unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was successfully deleted; otherwise, False.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> list[Prompt]:
        """Retrieves all prompts belonging to a specific collection.

        This method returns a list of Prompt objects that are associated 
        with the provided collection ID. It checks each prompt in the 
        in-memory storage to find those whose `collection_id` matches the 
        given ID.

        Args:
            collection_id (str): The unique identifier of the collection for which 
            prompts should be retrieved.

        Returns:
            List[Prompt]: A list of Prompt objects that belong to the specified 
            collection. This will be empty if no prompts are associated with the 
            given collection ID.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Tag Operations ==============
    
    def create_tag(self, tag: Tag) -> Tag:
        """Adds a new tag to the storage.

        This method stores a given Tag object in the in-memory storage
        using its unique identifier as the key. If a tag with the same
        ID already exists, it will be overwritten.

        Args:
            tag (Tag): The Tag object to be added to the storage.
        Returns:
            Tag: The stored Tag object, which includes its ID
            and any associated metadata.
        """
        self._tags[tag.id] = tag  # Add self._tags to store tags
        return tag
    
    def get_tag(self, tag_id: str) -> Tag | None:
        """Retrieves a tag from the storage by its ID.

        This method returns the Tag object associated with the given
        unique identifier, or None if the tag does not exist in the
        in-memory storage.

        Args:
            tag_id (str): The unique identifier of the tag to be retrieved.

        Returns:
            Optional[Tag]: The Tag object if found, otherwise None.
        """
        return self._tags.get(tag_id)

    def get_all_tags(self) -> list[Tag]:
        """Retrieves all tags stored in memory.

        This method returns a list of all Tag objects within the
        in-memory storage.

        Returns:
            List[Tag]: A list containing all the Tag objects stored
            in the storage. This will be empty if no tags have been created.
        """
        return list(self._tags.values())  # Ensure this initializes _tags in __init__

    def delete_tag(self, tag_id: str) -> bool:
        """Deletes a tag from the storage by its ID.

        This method removes a Tag object from the in-memory storage based on its
        unique identifier. It returns True if the tag was successfully deleted,
        and False if the tag did not exist in the storage.

        Args:
            tag_id (str): The unique identifier of the tag to be deleted.

        Returns:
            bool: True if the tag was deleted, False if it did not exist.
        """
        if tag_id in self._tags:
            del self._tags[tag_id]
            return True
        return False

    def get_prompts_by_tag(self, tag_id: str) -> list[Prompt]:
        """Retrieves all prompts associated with a specific tag ID.

        This method returns a list of Prompt objects that have the given
        tag ID in their tags attribute.

        Args:
            tag_id (str): The unique identifier of the tag to filter prompts by.

        Returns:
            List[Prompt]: A list of Prompt objects associated with the specified tag ID.
        """    
        return [p for p in self._prompts.values() if tag_id in p.tags]
    
    def _record_version(self, prompt: Prompt, updated_data: str) -> None:
        """Records a snapshot of the prompt's version in its history.

        Args:
            prompt (Prompt): The prompt being versioned.
            updated_data (str): A description of the changes made.
        """
        if prompt.id not in self._prompt_versions:
            self._prompt_versions[prompt.id] = []

        version_history = PromptVersionHistory(
            prompt_id=prompt.id,
            version=prompt.version,
            created_at=prompt.updated_at or prompt.created_at,
            updated_data=updated_data
        )
        self._prompt_versions[prompt.id].append(version_history)

    def get_prompt_versions(self, prompt_id: str) -> list[PromptVersionHistory] | None:
        """Retrieves the version history for a specific prompt.

        Args:
            prompt_id (str): The unique identifier of the prompt.

        Returns:
            Optional[List[PromptVersionHistory]]: A list of version history
            objects if the prompt exists, otherwise None.
        """
        if prompt_id not in self._prompts:
            return None
        return self._prompt_versions.get(prompt_id, [])

    # ============== Utility ==============

    def clear(self):
        """Clears all prompts and collections from storage.

        This method removes all Prompt and Collection objects from the
        in-memory storage, effectively resetting the storage. After
        invoking this method, both prompts and collections will be empty.

        Returns:
            None
        """
        self._prompts.clear()
        self._collections.clear()
        self._tags.clear()  # Clear tags as well
        self._prompt_versions.clear()  # Clear version history as well


# Global storage instance
storage = Storage()

