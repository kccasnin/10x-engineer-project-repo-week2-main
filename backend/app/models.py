"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generates a unique identifier using UUID4.

    This function creates a new unique identifier in string format 
    using the UUID4 generation method, which guarantees a high degree 
    of uniqueness.

    Returns:
        str: A string representation of a newly generated unique identifier.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Fetches the current UTC time.

    This function returns the current date and time in UTC as a 
    timezone-aware `datetime` object.

    Returns:
        datetime: The current date and time in UTC.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for a prompt.

    This class serves as the base Pydantic model defining the essential 
    attributes of a prompt in the system. It includes fields for the prompt's 
    title, content, description, and an optional collection ID.

    Attributes:
        title (str): The title of the prompt, which must be between 1 and 200 characters.
        content (str): The content of the prompt, which must not be empty.
        description (Optional[str]): A brief description of the prompt, 
        which can be up to 500 characters long. Default is None.
        collection_id (Optional[str]): An optional identifier for the collection 
        to which this prompt belongs. Default is None.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
     """Model for creating a new prompt.

    This class inherits from `PromptBase` and is used to validate 
    the data required for creating a new prompt. It does not add any 
    new fields but ensures that the essential attributes defined in 
    `PromptBase` are present and valid during the creation process.
    """
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing prompt.

    This class inherits from `PromptBase` and is used to validate 
    the data required for updating an existing prompt. It does not 
    introduce any new fields but ensures that the necessary attributes 
    defined in `PromptBase` are valid for the update operation.
    """
    pass


class Prompt(PromptBase):
     """Model representing a prompt with additional metadata.

    This class extends `PromptBase` to include additional attributes
    that are automatically generated when a prompt is created. It 
    holds the unique identifier of the prompt, as well as timestamps 
    for creation and the last update.

    Attributes:
        id (str): A unique identifier for the prompt, generated 
        using the `generate_id` function.
        created_at (datetime): The timestamp when the prompt was 
        created, set to the current time using `get_current_time`.
        updated_at (datetime): The timestamp for the last update, 
        also set to the current time using `get_current_time`.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
         """Pydantic configuration for the Prompt model.

        This configuration class includes settings that modify the 
        default behavior of the Pydantic model. Specifically, 
        it enables the use of attributes directly for model 
        initialization and validation.
        """
        from_attributes = True

class PromptPatch(BaseModel):
"""Model for partial updates to a prompt.

    This class allows for partial updates where each field is optional. 
    Only the fields provided in the request will be updated, while 
    maintaining the existing values for any fields not included. The 
    constraints for these fields match the `PromptBase` model to ensure 
    that provided values adhere to the same standards as those used in 
    the creation or full update of a prompt.

    Attributes:
        title (Optional[str]): The title of the prompt, which must be 
        between 1 and 200 characters if provided.
        content (Optional[str]): The content of the prompt, which must 
        not be empty if provided.
        description (Optional[str]): A brief description of the prompt, 
        which can be up to 500 characters long if provided. Default is None.
        collection_id (Optional[str]): An optional identifier for the 
        collection to which this prompt belongs. Default is None.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None

# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for a collection.

    This class serves as the base Pydantic model defining the essential 
    attributes of a collection in the system. It includes fields for the 
    collection's name and an optional description.

    Attributes:
        name (str): The name of the collection, which must be between 
        1 and 100 characters.
        description (Optional[str]): A brief description of the collection, 
        which can be up to 500 characters long. Default is None.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
     """Model for creating a new collection.

    This class inherits from `CollectionBase` and is used to validate 
    the data required for creating a new collection. It does not add 
    any new fields but ensures that the essential attributes defined 
    in `CollectionBase` are present and valid during the creation process.
    """
    pass


class Collection(CollectionBase):
    """Model representing a collection with additional metadata.

    This class extends `CollectionBase` to include additional attributes
    that are automatically generated when a collection is created. It 
    holds the unique identifier of the collection, as well as a timestamp 
    for when it was created.

    Attributes:
        id (str): A unique identifier for the collection, generated 
        using the `generate_id` function.
        created_at (datetime): The timestamp when the collection was 
        created, set to the current time using `get_current_time`.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        """Pydantic configuration for the Collection model.

        This configuration class modifies the default behavior of the 
        Pydantic model. It enables the use of attributes directly for 
        model initialization and validation, facilitating easier 
        interaction with the class's attributes.
        """
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model representing a list of prompts.

    This class holds a list of prompt objects and the total count of 
    prompts. It is used to structure the response when returning multiple 
    prompts from the API.

    Attributes:
        prompts (List[Prompt]): A list of prompt objects.
        total (int): The total number of prompts in the list.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
     """Model representing a list of collections.

    This class holds a list of collection objects and the total count of 
    collections. It is used to structure the response when returning multiple 
    collections from the API.

    Attributes:
        collections (List[Collection]): A list of collection objects.
        total (int): The total number of collections in the list.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model representing the health status of the API.

    This class is used to structure the response returned by the API 
    when checking its health status. It provides information about 
    the API's operational state and its version.

    Attributes:
        status (str): A string indicating the health status of the API, 
        typically "healthy" or "unhealthy".
        version (str): The current version of the API.
    """
    status: str
    version: str
