import os
import json
from pathlib import Path

class DataManip:
    def save_user_data(self, new_data: dict, directory: str, json_file: str) -> None:
        user_data_file = str(Path(directory) / json_file)

        os.makedirs(directory, exist_ok=True)

        if os.path.exists(user_data_file):
            with open(user_data_file, "r") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, dict):
                        data = {}
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        data.update(new_data)

        with open(user_data_file, "r+") as f:
            existing_content = f.read()
            updated_content = json.dumps(data, indent=4)
            if existing_content != updated_content:
                f.seek(0)
                f.write(updated_content)
                f.truncate()

    def load_user_data(
        self, directory: str, json_file: str, create_if_missing: bool = True
    ) -> dict:
        user_data_file = os.path.join(directory, json_file)
        if os.path.isfile(user_data_file):
            try:
                with open(user_data_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(
                    f"Warning: {user_data_file} contains invalid JSON. \
                    Returning empty data."
                )
                return {}
        else:
            if create_if_missing:
                print(
                    f"File {user_data_file} does not exist. \
                Creating a new one..."
                )
                with open(user_data_file, "w") as f:
                    json.dump({}, f, indent=4)
                return {}
        return {}
