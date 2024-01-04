import requests
import json

url = "http://127.0.0.1:5000/api/lecturers"

# Your JSON data for POST request
post_data = {
    "UUID": "8a2b5f91-1c4e-4d7a-9d86-12ab3cde5f12",
    "title_before": "Dr.",
    "first_name": "John",
    "last_name": "Carson",
    "picture_url": "https://example.com/profile_picture.png",
    "location": "Cityville",
    "claim": "Passionate researcher / Community leader / Tech enthusiast",
    "bio": "I thrive on exploring new ideas and pushing the boundaries of technology. Whether it's conducting research in cutting-edge fields, leading community initiatives, or diving into the world of tech, I am always eager to contribute and learn. My journey has involved everything from developing innovative software solutions to collaborating on open-source projects. Currently pursuing a PhD in Computer Science at Tech University.",
    "tags": [
        {"name": "Research"},
        {"name": "Community Engagement"},
        {"name": "Technology Enthusiast"},
        {"name": "Innovation"},
        {"name": "Open Source"},
        {"name": "Programming Languages"},
        {"name": "Artificial Intelligence"},
        {"name": "Data Science"},
    ],
    "price_per_hour": 1500,
    "contact": {
        "telephone_numbers": ["+123 456 7890"],
        "emails": ["alex.smith@example.com", "contact@alexsmith.com"],
    }
}

# Convert the data to JSON
json_post_data = json.dumps(post_data)

# Make the POST request
response_post = requests.post(url, data=json_post_data, headers={"Content-Type": "application/json"})
print("POST Response:")
print(response_post.status_code)
print(response_post.text)
