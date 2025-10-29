import pytest
import requests

ENDPOINT = "https://hacker-news.firebaseio.com/v0/"

def test_invalid_story_id():
    # Use a clearly invalid ID
    invalid_id = -1
    response = requests.get(ENDPOINT + f"item/{invalid_id}.json?print=pretty")
    # Expect 200 but empty/null response
    assert response.status_code == 200
    data = response.json()
    assert not data, "Expected empty response for invalid ID"

def test_nonexistent_story_id():
    # Use a very large unlikely ID
    invalid_id = 9999999999
    response = requests.get(ENDPOINT + f"item/{invalid_id}.json?print=pretty")
    assert response.status_code == 200
    data = response.json()
    assert not data, "Expected empty response for non-existent ID"

def test_malformed_endpoint():
    # Call a non-existent endpoint
    response = requests.get(ENDPOINT + "notarealendpoint.json")
    # Should return 404 or similar error code
    assert response.status_code == 401

def test_comment_missing_keys(get_item_details_missing_keys):
    # Use a valid comment id, but simulate missing keys
    class FakeResponse:
        status_code = 200
        def json(self): return {"id": 123456}
    def fake_get_item_details(item_id): return FakeResponse()
    resp = fake_get_item_details(123456)
    data = resp.json()
    # 'parent' and 'type' should be missing
    assert "parent" not in data
    assert "type" not in data

def test_timeout_error():
    # Simulate a timeout for requests.get
    import requests
    from requests.exceptions import Timeout

    def fake_get(*args, **kwargs):
        raise Timeout("Connection timed out.")

    requests.get = fake_get
    with pytest.raises(Timeout):
        requests.get(ENDPOINT + "topstories.json?print=pretty", timeout=0.001)

# Negative fixture: Simulate returning a comment with missing keys
@pytest.fixture
def get_item_details_missing_keys():
    class FakeResponse:
        status_code = 200
        def json(self):
            # Missing 'parent' and 'type'
            return {"id": 123456}
    def _fake_get_item_details(item_id):
        return FakeResponse()
    return _fake_get_item_details