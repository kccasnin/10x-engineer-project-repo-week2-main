"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


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
    collection_id: Optional[str] = None,
    search: Optional[str] = None
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
     
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
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
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
    if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,      # preserved — correct
        updated_at=get_current_time()         # FIXED: fresh timestamp on every update
    )
    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)


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
    return None


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
    return None
