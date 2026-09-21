"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
     """Sorts a list of prompts by their creation date.

    This function sorts the provided list of Prompt objects based on 
    their creation timestamps. The sorting order can be specified to 
    be either ascending or descending.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be sorted.
        descending (bool): If True, sorts prompts from newest to oldest;
        if False, sorts from oldest to newest. Defaults to True.

    Returns:
        List[Prompt]: A sorted list of Prompt objects based on their 
        creation date.
    """

    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filters a list of prompts by their associated collection ID.

    This function returns a list of Prompt objects that belong to a 
    specific collection, identified by the provided collection ID.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be filtered.
        collection_id (str): The unique identifier of the collection by 
        which prompts should be filtered.

    Returns:
        List[Prompt]: A list of Prompt objects that are associated with 
        the specified collection ID. This will be empty if no prompts 
        belong to the given collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Searches for prompts that match a given query.

    This function filters a list of Prompt objects to return only those 
    that contain the specified search query in either their title or 
    description. The search is case-insensitive.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be searched.
        query (str): The search query; prompts will be matched against 
        this string in a case-insensitive manner.

    Returns:
        List[Prompt]: A list of Prompt objects that contain the search 
        query in their title or description. This may be empty if no 
        matches are found.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Checks the validity of prompt content.

    A valid prompt must meet the following criteria:
    - It should not be empty.
    - It should not consist solely of whitespace.
    - It must contain at least 10 characters.

    Args:
        content (str): The content of the prompt to validate.

    Returns:
        bool: True if the prompt content is valid; otherwise, False.
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
"""Extracts template variables from prompt content.

    This function identifies and extracts variables embedded within 
    the prompt content that follows the template format {{variable_name}}. 
    It uses regular expressions to find all occurrences of the variables.

    Args:
        content (str): The prompt content containing template variables.

    Returns:
        List[str]: A list of variable names extracted from the content. 
        If no variables are found, an empty list is returned.
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
