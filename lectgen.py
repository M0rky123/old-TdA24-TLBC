import random, requests, json, time
tags = ["Adventure", "Creativity", "Technology", "Community Service", "Team Building", "Science", "Environmental Sustainability", "Art and Culture", "Health and Wellness", "Leadership", "Innovation", "Critical Thinking", "Global Awareness", "Digital Literacy", "Communication Skills", "Problem Solving", "Culinary Arts", "Fitness", "Mindfulness", "Financial Literacy", "Cybersecurity", "Diversity and Inclusion", "Social Justice", "Time Management", "Public Speaking", "Robotics", "Coding", "Media Literacy", "Entrepreneurship", "Ethics", "Outdoor Exploration", "Philanthropy", "Theater and Performance", "Self-Reflection", "Teamwork", "Virtual Reality", "Astronomy", "Psychology", "Music", "Gaming", "Fashion", "Philosophy", "Animal Welfare", "Sustainable Living", "Historical Exploration", "Futurism", "Magic and Illusion", "Travel", "Graphic Design", "Yoga", "Mental Health Awareness"]
first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Isabella", "Sophia", "Jackson", "Mia", "Lucas", "Oliver", "Amelia", "Evelyn", "Benjamin", "Harper", "Elijah", "Aiden", "Aria", "Caden", "Zoe", "Charlotte", "Mason", "Ella", "Carter", "Lily", "Grace", "Ethan", "Alexander", "Sebastian", "Mila", "Layla", "Nora", "Scarlett", "Zachary", "Chloe", "Liam", "Madison", "Henry", "Avery", "Jackson", "Ella", "Abigail", "Caleb", "Victoria", "Eli", "Penelope", "Hudson", "Stella", "Lillian"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hill", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins"]
titles_before_names = ["Mr.", "Ms.", "Dr.", "Mrs.", "Miss", "Prof.", "Rev.", "Sir", "Madam", "Lord", "Lady", "Mx.", "Capt.", "Hon.", "Col.", "Sgt.", "Cmdr.", "Fr.", "Engr.", "Amb."]
titles_after_names = ["Sr.", "Jr.", "PhD", "Esq.", "CPA", "DDS", "MD", "DVM", "CFA", "MBA", "RN", "FAIA", "PE", "MPH", "OBE", "FRAeS", "FSA", "FCA", "FIMechE", "FRSA"]
city_names = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose","Austin", "Jacksonville", "San Francisco", "Indianapolis", "Columbus", "Fort Worth", "Charlotte", "Seattle", "Denver", "El Paso","Detroit", "Washington", "Boston", "Nashville", "Memphis", "Portland", "Oklahoma City", "Las Vegas", "Louisville", "Baltimore","Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Mesa", "Kansas City", "Atlanta", "Long Beach", "Omaha", "Raleigh","Miami", "Virginia Beach", "Minneapolis", "Oakland", "Tulsa", "Arlington", "Wichita", "New Orleans", "Bakersfield"]
claims = ["Aktivní student", "Předsedkyně spolku", "Projektová manažerka", "Kreativní dobrovolník", "Inovativní vůdce", "Průkopnický badatel", "Social Media Guru", "Humanitární aktivista", "Technologický vizionář", "Ekologický bojovník", "Umělecký inspirátor"]
bios = ["✨ Adventure seeker | Coffee lover ☕ | Making memories around the world 🌍","🌈 Creative soul | Art enthusiast 🎨 | Spreading positivity and good vibes ✌️","📚 Lifelong learner | Bookworm 📖 | Passionate about knowledge and growth","🎵 Music lover | Concert-goer 🎤 | Dancing through life one song at a time","🍜 Foodie at heart | Culinary explorer 🍣 | Trying new recipes and flavors","🧘‍♀️ Mindfulness advocate | Yoga enthusiast 🧘 | Finding balance in chaos","💻 Tech geek | Coding ninja 🖥️ | Building the future, one line of code at a time","🌱 Eco-warrior | Sustainable living 🌍 | Nurturing the planet for future generations","👩‍💻 Digital nomad | Remote work enthusiast 💼 | Exploring the world while working","🎭 Theater lover | Drama queen/king 👑 | Bringing stories to life on and off the stage"]
picture_url = "https://picsum.photos/1920/1080/?random"

def generate_random_person():
    randomized_data = {
            "title_before": random.choice(titles_before_names),
            "first_name": random.choice(first_names),
            "middle_name": random.choice(first_names) if random.choice([True, False]) else None,
            "last_name": random.choice(last_names),
            "title_after": random.choice(titles_after_names),
            "picture_url": picture_url,
            "location": random.choice(city_names),
            "claim": random.choice(claims),
            "bio": random.choice(bios),
            "tags": [
                {
                    "name": random.choice(tags)
                } for i in range(random.randint(1, 10))
            ],
            "price_per_hour": random.uniform(800, 1500),
            "contact": {
                "telephone_numbers": [f"+420 {random.randint(100, 999)} {random.randint(100, 999)} {random.randint(100, 999)}" for _ in range(random.randint(1, 3))],
                "emails": [f"{random.choice(first_names)}.{random.choice(last_names)}@gmail.com" for _ in range(random.randint(1, 3))]
            }
        }
    return randomized_data

url = "http://127.0.0.1:5000/api/lecturers"

for i in range(20):
    random_person = generate_random_person()

    # Make the POST request
    response_post = requests.post(url, json=random_person, headers={"Content-Type": "application/json"})
    print(response_post.status_code)
    # Make it wait for 2 seconds
    time.sleep(2)

print("Done!")