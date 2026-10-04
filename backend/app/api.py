"""FastAPI routes for PromptLab"""
import logging

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.models import Tag, TagCreate
from app.storage import storage  # Import the storage for tag manipulation

logger = logging.getLogger(__name__)

from app import __version__
from app.models import (
    Collection,
    CollectionCreate,
    CollectionList,
    HealthResponse,
    Prompt,
    PromptCreate,
    PromptList,
    PromptUpdate,
    PromptVersionHistory,
    RollbackRequest,
    get_current_time,
)
from app.utils import filter_prompts_by_collection, search_prompts, sort_prompts_by_date

app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================== Tag Endpoints ==================

@app.post("/tags", response_model=Tag, status_code=201)
def create_tag(tag_data: TagCreate):
    """Creates a new tag in the system.

    This endpoint allows users to create a tag by providing its name.
    If a tag with the same name already exists, a 400 error will be 
    raised indicating that tag names must be unique.  If the tag name 
    is empty, a 400 Bad Request error will be raised.

    Args:
        tag (TagCreate): The data required to create a new tag, which must 
        include a name.

    Returns:
        Tag: The created Tag object, including its ID and creation timestamp.

    Raises:
        HTTPException: 
        - If a tag with the same name already exists, a 400 Bad Request 
            exception is raised with a detail message.
        - If the provided tag name is empty, a 400 Bad Request exception 
            is raised indicating that the tag name must be provided.
    """
     # New validation for empty tag name
    if not tag_data.name or tag_data.name.strip() == "":  # Checking if the tag name is empty or just whitespace
        raise HTTPException(status_code=400, detail="Tag name must be provided.")
    
    if any(existing_tag.name == tag_data.name for existing_tag in storage.get_all_tags()):
        raise HTTPException(status_code=400, detail="Tag name must be unique.")
    # Create a new Tag instance
    tag = Tag(name=tag_data.name)
    return storage.create_tag(tag)  # Ensure the correct response and status code


@app.get("/tags", response_model=list[Tag])
def retrieve_tags():
    """Retrieves all tags from the system.

    This endpoint returns a list of all tags currently available in the system.

    Returns:
        List[Tag]: A list of tag objects, each containing their unique identifier, name, and creation timestamp.

    Raises:
        None
    """
    return storage.get_all_tags()


@app.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: str):
    """Deletes a tag identified by its unique identifier.

    This endpoint allows a user to delete a tag from the system. 
    If the tag does not exist, a 404 HTTP exception is raised. 
    Additionally, if the tag is currently associated with any prompts, 
    a 409 HTTP exception is raised to prevent orphaned associations.

    Args:
        tag_id (str): The unique identifier of the tag to delete.

    Returns:
        None: A successful deletion results in a 204 No Content response.

    Raises:
        HTTPException: If the specified tag ID does not exist, a 
        404 HTTPException is raised with the detail message 
        "Tag not found."
        HTTPException: If the tag is currently associated with prompts, a 
        409 HTTPException is raised with the detail message 
        "Cannot delete tag that is in use."
    """
    tag = storage.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found.")
    
    # Check if the tag is associated with any prompts
    if storage.get_prompts_by_tag(tag_id):
        raise HTTPException(status_code=409, detail="Cannot delete tag that is in use.")
    
    storage.delete_tag(tag_id)

# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Returns the health status of the API.

    This endpoint checks if the API is up and running. It returns a
    response containing the status and version of the API.

    Returns:
        HealthResponse: An object containing the health status and
        the current version of the API.

    Raises:
        None
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: str | None = None,
    search: str | None = None,
    tags: list[str] | None = Query(default=None)  # noqa: B008
):
    """Retrieves a list of prompts, optionally filtered by collection or searched by content.

    This endpoint returns all prompts in the storage, allowing optional
    filtering by a specific collection ID and searching for prompts that 
    match a given query.

    Args:
        collection_id (Optional[str]): An optional collection ID to filter 
        prompts by. If provided, only prompts belonging to the specified 
        collection will be returned.
        
        search (Optional[str]): An optional search query to filter prompts 
        by their title or description. If provided, only prompts matching 
        the search criteria will be returned.

    Returns:
        PromptList: An object containing a list of prompts and the total 
        number of prompts returned.

    Raises:
        None
    """
    print(f"DEBUG: Received tags -> {tags}")  # Add this line

    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Filter by tags if provided
    if tags:
        # Validate that all provided tag IDs exist
        print("DEBUG: Entering tags validation block")  # Add this line

        for tag_id in tags:
            print(f"DEBUG: Checking tag_id -> {tag_id}")  # Add this line

            if not storage.get_tag(tag_id):
                print(f"DEBUG: Tag {tag_id} not found! Raising 404")  # Add this line
                raise HTTPException(status_code=404, detail="Tag not found.")
        # Filter prompts that contain ANY of the specified tags
        prompts = [p for p in prompts if any(tag_id in p.tags for tag_id in tags)]
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieves a prompt by its unique identifier.

    This endpoint fetches a prompt from storage based on the provided 
    prompt ID. If the prompt does not exist, it raises a 404 HTTP 
    exception.

    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.

    Returns:
        Prompt: The prompt object corresponding to the provided ID.

    Raises:
        HTTPException: If the prompt with the specified ID does not exist, 
        a 404 HTTPException is raised with the detail message "Prompt not found".
    """

    prompt = storage.get_prompt(prompt_id)

    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.get("/prompts/{prompt_id}/versions", response_model=list[PromptVersionHistory])
def get_prompt_versions(prompt_id: str):
    """Retrieves the version history for a specific prompt.

    Args:
        prompt_id (str): The unique identifier of the prompt.

    Returns:
        List[PromptVersionHistory]: A list of version history objects.

    Raises:
        HTTPException: If the prompt is not found, raises a 404 error.
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found.")
    versions = storage.get_prompt_versions(prompt_id)
    if versions is None:
        return []
    return versions


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Creates a new prompt in the system.

    This endpoint allows a user to create a new prompt. It validates 
    that the associated collection exists if a collection ID is provided. 
    If the collection exists, the new prompt is created and stored.

    Args:
        prompt_data (PromptCreate): A Pydantic model containing the details 
        of the prompt to be created, including title, content, 
        description, and an optional collection ID.

    Returns:
        Prompt: The created prompt object, including its generated ID 
        and timestamps.

    Raises:
        HTTPException: If the specified collection ID does not exist, 
        a 400 HTTPException is raised with the detail message 
        "Collection not found".
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


def _validate_collection_exists(collection_id: str | None):
    """Helper to validate that a collection exists if an ID is provided.

    Args:
        collection_id (Optional[str]): The ID of the collection to validate.

    Raises:
        HTTPException: If the specified collection ID does not exist, 
        a 400 HTTPException is raised with the detail message 
        "Collection not found".
    """
    if collection_id:
        collection = storage.get_collection(collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")


def _increment_version(current_version: str, change_type: str | None) -> str:
    """Increments the semantic version based on the change type.
    Args:
        current_version (str): The current version string (e.g., "1.0.0").
        change_type (Optional[str]): The type of change ('major', 'minor', 'patch').
    Returns:
        str: The new incremented version string.
    """
    major, minor, patch = map(int, current_version.split('.'))
    if change_type == "major":
        return f"{major + 1}.0.0"
    elif change_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif change_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        # Default to minor increment
        return f"{major}.{minor + 1}.0"


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Updates an existing prompt in the system.

    This endpoint allows a user to update the details of a prompt identified
    by its unique ID. It checks if the prompt exists and validates that any
    specified collection exists if provided. The updated prompt is returned
    with a new timestamp.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): A Pydantic model containing the updated
        details of the prompt, including title, content, description,
        and an optional collection ID.

    Returns:
        Prompt: The updated prompt object, including its existing ID, 
        and a new timestamp for updated_at.

    Raises:
        HTTPException:
            - If the specified prompt ID does not exist, a 404
            HTTPException is raised with the detail message
        "Prompt not found".
            - If the specified collection ID does not exist, a
            400 HTTPException is raised with the detail message
        "Collection not found".
    """
    existing = storage.get_prompt(prompt_id=prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    _validate_collection_exists(prompt_data.collection_id)

    new_version = _increment_version(existing.version, prompt_data.change_type)

    # Preserve existing tags if not explicitly provided in the update payload
    tags_to_use = prompt_data.tags if prompt_data.tags else existing.tags

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,      # preserved — correct
        updated_at=get_current_time(),        # FIXED: fresh timestamp on every update
        version=new_version,
        tags=tags_to_use
    )
    return storage.update_prompt(prompt_id, updated_prompt)
    

@app.post("/prompts/{prompt_id}/rollback", response_model=Prompt)
def rollback_prompt(prompt_id: str, rollback_data: RollbackRequest):
    """Rolls back a prompt to a previous version.

    Args:
        prompt_id (str): The unique identifier of the prompt.
        rollback_data (RollbackRequest): The version to roll back to.

    Returns:
        Prompt: The restored prompt object.

    Raises:
        HTTPException: If the version format is invalid (400), the prompt is
        not found (404), or the version is not found (404).
    """
    import re
    if not re.match(r'^\d+\.\d+\.\d+$', rollback_data.version):
        raise HTTPException(status_code=400, detail="Invalid version format.")

    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found.")

    restored = storage.rollback_prompt(prompt_id, rollback_data.version)
    if not restored:
        raise HTTPException(status_code=404, detail="Prompt version not found.")
    return restored


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Deletes a prompt identified by its unique identifier.

    This endpoint allows a user to delete a prompt from the system.
    If the prompt with the specified ID does not exist, a 404 HTTP
    exception is raised.

    Args:
        prompt_id (str): The unique identifier of the prompt to delete.

    Returns:
        None: A successful deletion results in a 204 No Content response.

    Raises:
        HTTPException: If the specified prompt ID does not exist, a
        404 HTTPException is raised with the detail message
        "Prompt not found".
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Retrieves a list of all collections in the system.

    This endpoint returns all collections stored in the system, along with 
    the total count of collections.

    Returns:
        CollectionList: An object containing a list of all collections and 
        the total number of collections.

    Raises:
        None
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieves a collection by its unique identifier.

    This endpoint fetches a collection from storage based on the provided
    collection ID. If the collection does not exist, it raises a 404 HTTP
    exception.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection object corresponding to the provided ID.

    Raises:
        HTTPException: If the collection with the specified ID does not exist, 
        a 404 HTTPException is raised with the detail message "Collection not found".
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Creates a new collection in the system.

    This endpoint allows a user to create a new collection. The provided
    collection data is used to instantiate a collection object which is then
    stored in the system.

    Args:
        collection_data (CollectionCreate): A Pydantic model containing the
        details of the collection to be created, including the name and
        an optional description.

    Returns:
        Collection: The created collection object, including its generated 
        ID and timestamps.

    Raises:
        None
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Deletes a collection identified by its unique identifier.

    This endpoint allows a user to delete a collection from the system.
    If the specified collection exists, all prompts associated with the
    collection will be updated to remove their collection ID before the
    collection itself is deleted. If the collection does not exist, a
    404 HTTP exception is raised.

    Args:
        collection_id (str): The unique identifier of the collection to delete.

    Returns:
        None: A successful deletion results in a 204 No Content response.

    Raises:
        HTTPException: If the specified collection ID does not exist, a
        404 HTTPException is raised with the detail message
        "Collection not found".
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    for prompt in storage.get_prompts_by_collection(collection_id):
        unfiled = prompt.model_copy(update={"collection_id": None})
        storage.update_prompt(prompt.id, unfiled)

    storage.delete_collection(collection_id)

