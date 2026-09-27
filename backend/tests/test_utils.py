# backend/tests/test_utils.py
import pytest
from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables
)

@pytest.fixture
def sample_prompts():
    """Sample prompt data for testing."""
    return [
        Prompt(id="1", title="Prompt One", content="Content One", created_at="2023-10-01T10:00:00Z"),
        Prompt(id="2", title="Prompt Two", content="Content Two", created_at="2023-10-02T10:00:00Z"),
        Prompt(id="3", title="Prompt Three", content="Content Three", created_at="2023-10-03T10:00:00Z"),
    ]

@pytest.fixture
def sample_prompt_data():
    """Sample prompt for content validation."""
    return "This prompt content is valid and has more than ten characters."

def test_sort_prompts_by_date(sample_prompts):
    """Test sorting prompts by creation date in descending order."""
    sorted_prompts = sort_prompts_by_date(sample_prompts, descending=True)
    assert sorted_prompts[0].id == "3"  # Newest prompt should be first
    assert sorted_prompts[-1].id == "1"  # Oldest prompt should be last

def test_sort_prompts_by_date_ascending(sample_prompts):
    """Test sorting prompts by creation date in ascending order."""
    sorted_prompts = sort_prompts_by_date(sample_prompts, descending=False)
    assert sorted_prompts[0].id == "1"  # Oldest prompt should be first
    assert sorted_prompts[-1].id == "3"  # Newest prompt should be last

def test_filter_prompts_by_collection(sample_prompts):
    """Test filtering prompts by collection ID."""
    # Adding collection_id to prompts
    sample_prompts[0].collection_id = "collection-1"
    sample_prompts[1].collection_id = "collection-2"
    sample_prompts[2].collection_id = "collection-1"

    filtered = filter_prompts_by_collection(sample_prompts, "collection-1")
    assert len(filtered) == 2  # Should return two prompts

def test_search_prompts(sample_prompts):
    """Test searching prompts by title."""
    results = search_prompts(sample_prompts, "One")
    assert len(results) == 1
    assert results[0].title == "Prompt One"

def test_search_prompts_no_results(sample_prompts):
    """Test searching for prompts that do not match."""
    results = search_prompts(sample_prompts, "Non-existent")
    assert len(results) == 0

def test_validate_prompt_content_valid(sample_prompt_data):
    """Test valid prompt content."""
    result = validate_prompt_content(sample_prompt_data)
    assert result is True

def test_validate_prompt_content_too_short():
    """Test invalid prompt content that is too short."""
    result = validate_prompt_content("short")
    assert result is False

def test_validate_prompt_content_empty():
    """Test invalid prompt content that is empty."""
    result = validate_prompt_content("")
    assert result is False

def test_extract_variables():
    """Test extracting variables from prompt content."""
    content = "Here is a variable {{variable_name}} and another {{another_variable}}."
    variables = extract_variables(content)
    assert len(variables) == 2
    assert "variable_name" in variables
    assert "another_variable" in variables

def test_extract_variables_no_variables():
    """Test extracting variables when none exist."""
    content = "No variables here."
    variables = extract_variables(content)
    assert len(variables) == 0
