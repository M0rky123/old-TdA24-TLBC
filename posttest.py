import requests
import json

url = "http://127.0.0.1:5000/api/lecturers/b108f9e7-42ca-467b-b17a-f3be68f89b37"
#url = "http://f7b5d5a152c395f1.app.tourdeapp.cz/api/lecturers/999a8b5f-8dda-4ba8-8a15-21df6110f573"
#Need to force commit lol

# Your JSON data for POST request
post_data = {
    "title_before": "111",
    "first_name": "2222",
    "middle_name": "333",
    "last_name": "Červ44eňoučká",
    "picture_url": "https://fastly.picsum.photos/id/480/200/200.jpg?hmac=q_kzh_8Ih85_5t_jN3rcD3npeNBLA41oDGtQZVkmmYs",
    "location": "Cityville",
    "claim": "Passionate researcher / Community leader / Tech enthusiast",
    "bio": "I thrive on exploring new ideas and pushing the boundaries of technology. Whether it's conducting research in cutting-edge fields, leading community initiatives, or diving into the world of tech, I am always eager to contribute and learn. My journey has involved everything from developing innovative software solutions to collaborating on open-source projects. Currently pursuing a PhD in Computer Science at Tech University.",
    "tags": [
        {"name": "BUNF OF NONSENCE"},

    ],
    "price_per_hour": 100,
    "contact": {
        "telephone_numbers": ["+123 456 789 012", "+420 233 444 555"],
        "emails": ["alex.smith@example.com", "contact@alexsmith.com"],
    }
}



# Convert the data to JSON
json_post_data = json.dumps(post_data)

# Make the POST request
response_post = requests.put(url, json=post_data, headers={"Content-Type": "application/json"})
print("POST Response:")
print(response_post.status_code)
print(type(response_post.text))
print(response_post.text)