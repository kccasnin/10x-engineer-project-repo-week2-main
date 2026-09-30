Step 1: Intentionally Break a Test
Open Your 
test_api.py
 File: Go to the backend/tests/test_api.py file where your test cases are defined.

Choose a Test to Break: Select a valid test and modify it to make it fail. This could involve changing an assertion or returning an incorrect value.

For example, you might adjust the 
test_create_tag
 test like this:


Apply
def test_create_tag(self, client: TestClient):
    """Test creating a new tag with valid data."""
    new_tag_data = {"name": "Sample Tag"}
    
    response = client.post("/tags", json=new_tag_data)
    
    assert response.status_code == 201  # Change 200 to 201 to make it fail
    data = response.json()
    assert data["name"] == "Sample Tag"
    assert "id" in data
    assert "created_at" in data
This change will cause the test for creating a tag to fail, as it expects a 201 Created response but will instead log a 200 OK.

Terminal 

FAILED backend/tests/test_api.py::TestTags::test_create_tag - assert 200 == 201


Revert the Changes
Undo the Changes: To revert the breaking change, modify the test back to its original state:


Apply
def test_create_tag(self, client: TestClient):
    """Test creating a new tag with valid data."""
    new_tag_data = {"name": "Sample Tag"}
    
    response = client.post("/tags", json=new_tag_data)
    
    assert response.status_code == 201  # Revert to the correct status code
    data = response.json()
    assert data["name"] == "Sample Tag"
    assert "id" in data
    assert "created_at" in data

Terminal 

None