"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


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
    """
    def __init__(self):
        """Initializes the Storage instance.

        This constructor creates an empty in-memory storage for prompts 
        and collections by initializing two dictionaries:
        - `_prompts`: to store Prompt objects mapped by their unique IDs.
        - `_collections`: to store Collection objects mapped by their 
          unique IDs.
        """
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
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
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
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
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieves all prompts stored in memory.

        This method returns a list of all Prompt objects within the 
        in-memory storage.

        Returns:
            List[Prompt]: A list containing all the Prompt objects stored 
            in the storage. This will be empty if no prompts have been created.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
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
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
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
    
    def get_all_collections(self) -> List[Collection]:
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
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
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


# Global storage instance
storage = Storage()
