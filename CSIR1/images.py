import random
import json
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)
def get_random_image():
    file_path = resource_path('image.json') 
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if not data:
                raise ValueError("JSON data is empty.")

            rand_id = random.randrange(len(data))
            question = data[rand_id]
            # questions.pop(random_id)
            # with open(file_path, 'w', encoding='utf-8') as f:
            #  json.dump(questions, f, indent=4)
            return {
                "id": question.get("id"),
                "image": question.get("image"),
                "options": question.get("options"),
                "answer": question.get("answer")
            }
    except FileNotFoundError:
        print("Error: 'image.json' file not found.")
    except json.JSONDecodeError:
        print("Error: JSON decode failed. Check file format.")
    except Exception as e:
        print(f"Unexpected error: {e}")
