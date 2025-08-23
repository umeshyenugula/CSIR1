import random
import json
import os
import sys

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundles.
    """
    if hasattr(sys, "_MEIPASS"):  # When bundled by PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)

def get_random_image():
    file_path = resource_path(os.path.join("QUESTIONS", "CURRENT", "pictotech.json"))
    
    # Check if file exists, and handle errors
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not data:
            print("Error: JSON data is empty.")
            return None

        rand_index = random.randrange(len(data))
        question = data.pop(rand_index)  # Remove selected question

        # Save updated JSON
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return {
            "id": question.get("id"),
            "image": question.get("image"),
            "options": question.get("options"),
            "answer": question.get("answer"),
        }
    except json.JSONDecodeError:
        print("Error: JSON decoding failed. Check the file format.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
