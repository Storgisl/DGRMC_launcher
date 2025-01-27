import json
import os


def load_user_data(directory: str, json_file: str, create_if_missing: bool = True) -> dict:
    user_data_file = os.path.join(directory, json_file)

    if os.path.isfile(user_data_file):
        try:
            with open(user_data_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {user_data_file} contains invalid JSON. \
                Returning empty data.")
            return {}
    else:
        if create_if_missing:
            print(f"File {user_data_file} does not exist. \
            Creating a new one...")
            with open(user_data_file, "w") as f:
                json.dump({}, f, indent=4)
            return {}

    return {}
