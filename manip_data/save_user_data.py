import os
import json 


def save_user_data(new_data: dict, directory: str, json_file: str) -> None:
    user_data_file = os.path.join(directory, json_file)

    if not os.path.exists(user_data_file):
        with open(user_data_file, "w") as f:
            json.dump({}, f, indent=4)

    with open(user_data_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    data.update(new_data)

    with open(user_data_file, "w") as f:
        json.dump(data, f, indent=4)
