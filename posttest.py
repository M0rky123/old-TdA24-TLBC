import requests
import json

url = "http://127.0.0.1:5000/api/lecturers/d0ca045e-f8de-4a17-9231-d8a60e272f00"

# Your JSON data for POST request
post_data = {
    "title_before": "Bc., Mgr., Ing.",
    "first_name": "Vendelína",
    "middle_name": "Kraťoučká",
    "last_name": "Červeňoučká",
    "picture_url": "https://fastly.picsum.photos/id/480/200/200.jpg?hmac=q_kzh_8Ih85_5t_jN3rcD3npeNBLA41oDGtQZVkmmYs",
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
    "price_per_hour": 100,
    "contact": {
        "telephone_numbers": ["+123 456 789 012"],
        "emails": ["alex.smith@example.com", "contact@alexsmith.com"],
    }
}



# Convert the data to JSON
json_post_data = json.dumps(post_data)

# Make the POST request
#response_post = requests.post(url, data=json_post_data, headers={"Content-Type": "application/json"})
print("POST Response:")
print(response_post.status_code)
print(response_post.text)