import requests
import json

url = "http://127.0.0.1:5000/api/lecturers"

# Your JSON data
data = {
    "UUID": "67fda282-2bca-41ef-9caf-039cc5c8dd69",
    "title_before": "Mgr.",
    "first_name": "Petra",
    "middle_name": "Swil",
    "last_name": "Plachá",
    "title_after": "MBA",
    "picture_url": "https://tourdeapp.cz/storage/images/2023_02_25/412ff296a291f021bbb6de10e8d0b94863fa89308843b/big.png.webp",
    "location": "Brno",
    "claim": "Aktivní studentka / Předsedkyně spolku / Projektová manažerka",
    "bio": "Baví mě organizovat věci. Ať už to bylo vyvíjení mobilních aplikací ve Futured, pořádání konferencí, spolupráce na soutěžích Prezentiáda, pIšQworky, Tour de App a Středoškolák roku, nebo třeba dobrovolnictví, vždycky jsem skončila u projektového managementu, rozvíjení soft-skills a vzdělávání. U studentských projektů a akcí jsem si vyzkoušela snad všechno od marketingu po logistiku a moc ráda to předám dál. Momentálně studuji Pdf MUNI a FF MUNI v Brně.",
    "tags": [
        {"name": "Dobrovolnictví"},
        {"name": "Studentské spolky"},
        {"name": "Efektivní učení"},
        {"name": "Prezentační dovednosti"},
        {"name": "Marketing pro neziskové studentské projekty"},
        {"name": "Mimoškolní aktivity"},
        {"name": "Projektový management, event management"},
        {"name": "Fundraising pro neziskové studentské projekty"},
    ],
    "price_per_hour": 1200,
    "contact": {
        "telephone_numbers": ["+420 722 482 974"],
        "emails": ["placha@scg.cz", "predseda@scg.cz"],
    }
}

# Convert the data to JSON
json_data = json.dumps(data)

# Make the POST request
response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})

# Print the response
print(response.status_code)
print(response.text)
