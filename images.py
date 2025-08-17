import random
import json
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_random_image():
    file_path = resource_path('QUESTIONS/CURRENT/pictotech.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not data:
            raise ValueError("JSON data is empty.")

        rand_index = random.randrange(len(data))
        question = data.pop(rand_index)  # Remove the selected question from list

        # Save the updated list back to the file without the popped question
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return {
            "id": question.get("id"),
            "image": question.get("image"),
            "options": question.get("options"),
            "answer": question.get("answer")
        }
    except FileNotFoundError:
        print("Error: 'pictotech.json' file not found.")
    except json.JSONDecodeError:
        print("Error: JSON decode failed. Check file format.")
    except Exception as e:
        print(f"Unexpected error: {e}")
