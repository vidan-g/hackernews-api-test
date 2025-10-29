import random
import requests

ENDPOINT = " https://hacker-news.firebaseio.com/v0/"

#Retrieve top stories, pick a random ID and assert its properties
def test_top_stories():
    top_stories_response = requests.get(ENDPOINT + "topstories.json?print=pretty")
    assert top_stories_response.status_code == 200
    json_data = top_stories_response.json()

    #Pick a random number between 0 - 199 and index that element
    rand_num = random.randint(0, 199)
    rand_story_id = json_data[rand_num]

    #Call that story and check the "score" and "type"
    top_rand_story_response = requests.get(ENDPOINT + "item/" + str(rand_story_id) + ".json?print=pretty")
    print(top_rand_story_response.text)
    assert top_rand_story_response.status_code == 200
    json_data = top_rand_story_response.json()

    #Assert different return values from the json response
    assert json_data["id"] == rand_story_id
    assert isinstance(json_data["score"], int)
    assert isinstance(json_data["title"], str)
    assert json_data["type"] == "story"