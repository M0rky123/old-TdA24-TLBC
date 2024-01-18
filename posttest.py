import requests
import json

url = "http://127.0.0.1:5000/api/lecturers/filter"
url_get_all = "http://127.0.0.1:5000/api/lecturers"
#url = "http://f7b5d5a152c395f1.app.tourdeapp.cz/api/lecturers/999a8b5f-8dda-4ba8-8a15-21df6110f573"
#Need to force commit lol

# Your JSON data for POST request
post_data = {
    "tag": "Fitness",
    "loc": "Tvoje máma"
}



# Convert the data to JSON
json_post_data = json.dumps(post_data)

# Make the POST request
reponse = requests.get(url_get_all)
print(reponse)
response_post = requests.get(url, json=post_data, headers={"Content-Type": "application/json"})
print("POST Response:")
print(response_post.status_code)
print(type(response_post.text))
print(response_post.text)