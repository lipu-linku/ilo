import json

PREFERENCES_PATH = "userdata/preferences.json"


def read_preferences():
    with open(PREFERENCES_PATH) as f:
        return json.load(f)


def build_preferences(preferences):
    with open(PREFERENCES_PATH, 'w') as f:
        json.dump(preferences, f, indent=2)


def get_preference(user_id, key, default_value):
    preferences = read_preferences()
    if user_id in preferences:
        if key in preferences[user_id]:
            return preferences[user_id][key]
    return default_value


def set_preference(user_id, key, value):
    preferences = read_preferences()
    # Create user if new
    if user_id not in preferences:
        preferences[user_id] = {}
    # Set value if user wants it set
    preferences[user_id][key] = value
    build_preferences(preferences)


def reset_preferences(user_id):
    preferences = read_preferences()
    # Delete user
    if user_id in preferences:
        preferences.pop(user_id)
    build_preferences(preferences)
