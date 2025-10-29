import json
import random

import pytest
import requests

ENDPOINT = " https://hacker-news.firebaseio.com/v0/"

# Retrieve top stories, pick a random ID and assert its properties
def test_top_stories():
    # Fetch top stories list
    top_stories_response = requests.get(ENDPOINT + "topstories.json?print=pretty")
    assert top_stories_response.status_code == 200, "Failed to fetch top stories"
    json_data = top_stories_response.json()
    assert len(json_data) > 0, "Top stories list is empty"

    # Pick a random number between 0 - 199 and index that element
    rand_num = random.randint(0, 199)
    rand_story_id = json_data[rand_num]

    # Call a random story ID and save format the response metadata
    top_rand_story_response = requests.get(ENDPOINT + "item/" + str(rand_story_id) + ".json?print=pretty")
    print(top_rand_story_response.text)
    assert top_rand_story_response.status_code == 200, f"Failed to fetch story {rand_story_id}"
    top_rand_story_json_data = top_rand_story_response.json()
    assert isinstance(top_rand_story_json_data, dict), "Story response should be a dict"

    # Assert different return values from the json response
    assert top_rand_story_json_data["id"] == rand_story_id
    assert isinstance(top_rand_story_json_data["score"], int), "'score' should be int"
    assert isinstance(top_rand_story_json_data["title"], str), "'title' should be str"
    assert top_rand_story_json_data["type"] == "story"

    # Edge case: "text" key should not be present in story object
    assert "text" not in top_rand_story_json_data, "The 'text' key should not be present in a Story response."

    # Edge case: Check for unexpected keys
    for key in ["parent", "kids"]:
        # "parent" shouldn't exist in top-level stories, "kids" may or may not
        if key in top_rand_story_json_data and key == "parent":
            pytest.fail(f"Unexpected key '{key}' in story response")

def test_current_top_story(get_top_stories):
    # Initialize the dictionary to store results: {item_id: score}
    item_scores_map = {}
    current_top_story_response = get_top_stories
    assert current_top_story_response.status_code == 200
    print(current_top_story_response.text)

    # Store all story IDs into a list object
    current_top_story_json_data = current_top_story_response.json()
    assert isinstance(current_top_story_json_data, list), "Top stories should be a list"
    assert len(current_top_story_json_data) > 0, "No stories found"

    # Loop through the list of story IDs (est. run time is 6min for 200 items)
    for item in current_top_story_json_data:
        # Construct the full API URL for the current item
        api_url = f"{ENDPOINT+"/item/"}{item}{".json?print=pretty"}"

        try:
            # Make the API call
            response = requests.get(api_url, timeout=10)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                # Edge: Ensure expected keys exist
                assert "score" in data, f"Story {item} lacks 'score' key"
                # Extract the score value
                extracted_score = data["score"]
                # Assert that the extracted score is an integer (or a number type)
                assert isinstance(extracted_score, int), f"Expected 'score' to be an integer, but got {type(extracted_score)}"
                # Extract and store the score in the dictionary
                item_scores_map[item] = extracted_score
            else:
                print(f"Error fetching data for {item}: Status code {response.status_code}")

        # Catch any exceptions during API call
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while calling API for {item}: {e}")

    # Assert that we actually collected some data
    assert item_scores_map, "The dictionary of item scores is empty."

    # Find the HIGHEST score and its corresponding Story ID
    # I use the max() function with the 'key' argument to find the key (item_id)
    # that corresponds to the maximum value (score) in the dictionary.
    highest_score_item_id = max(item_scores_map, key=item_scores_map.get)
    print(f"The current top story (based on highest score) is: {highest_score_item_id}")

def test_first_comment_top_story(get_top_stories, get_item_details):
    # Fetch top stories
    top_story_response = get_top_stories
    assert top_story_response.status_code == 200, "Failed to fetch top stories"
    top_story_json_data = top_story_response.json()
    assert isinstance(top_story_json_data, list), "Top stories should be a list"
    assert len(top_story_json_data) > 0, "No stories found"
    first_story_id = top_story_json_data[0]
    print("Top Story ID: " + str(first_story_id))

    # Fetch details for the first story
    first_story_response = get_item_details(first_story_id)
    assert first_story_response.status_code == 200, f"Failed to fetch story {first_story_id}"
    first_story_json_data = first_story_response.json()
    assert isinstance(first_story_json_data, dict), "Story response should be a dict"
    assert "kids" in first_story_json_data, "No comments on top story"
    assert isinstance(first_story_json_data["kids"], list), "'kids' should be a list"
    assert len(first_story_json_data["kids"]) > 0, "No comments in 'kids' array"
    first_comment_id = first_story_json_data["kids"][0]
    print("First comment ID: " + str(first_comment_id))

    # Get first comment details
    first_comment_response = get_item_details(first_comment_id)
    assert first_comment_response.status_code == 200, f"Failed to fetch comment {first_comment_id}"
    first_comment_json_data = first_comment_response.json()
    assert isinstance(first_comment_json_data, dict), "Comment response should be a dict"

    # Assert the response data
    assert "id" in first_comment_json_data, "'id' key missing in comment"
    assert first_comment_json_data["id"] == first_comment_id

    assert "parent" in first_comment_json_data, "'parent' key missing in comment"
    assert first_comment_json_data["parent"] == first_story_id

    assert "type" in first_comment_json_data, "'type' key missing in comment"
    assert first_comment_json_data["type"] == "comment"

    # Extract text property and print it from the first comment
    assert "text" in first_comment_json_data, "'text' key missing in comment"
    first_comment_response_text = first_comment_json_data["text"]
    print (f"Full first comment from Top story {first_story_id}: " + first_comment_response_text)

# Fixtures
@pytest.fixture
def get_top_stories():
    # Fetches the top stories from Hacker News
    top_stories_response = requests.get(ENDPOINT + "topstories.json?print=pretty")
    return top_stories_response


@pytest.fixture
def get_item_details():
    # Returns a function that fetches details for a given item ID
    def _fetch_item_details(item_id):
        # This is the function that actually makes the API call
        item_details_response = requests.get(ENDPOINT + "item/" + str(item_id) + ".json?print=pretty")
        return item_details_response

    # The fixture returns the inner function
    return _fetch_item_details