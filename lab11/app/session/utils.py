import json

def load_user_data():
    try:
        with open('users.json', 'r') as file:
            user_data = json.load(file)
        return user_data
    except FileNotFoundError:
        return {}