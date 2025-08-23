import random
import json
import os
import sys

def resource_path(relative_path):
    """
    Returns the absolute path of the resource, works in both dev and packaged modes.
    """
    try:
        base_path = sys._MEIPASS  # When running from a packaged app (PyInstaller)
    except AttributeError:
        base_path = os.path.abspath(".")  # When running in development mode
    return os.path.join(base_path, relative_path)

def get_random_truth_question(file_path='QUESTIONS/CURRENT/truthlie.json'):
    file_path = resource_path(file_path)  # Resolve the file path
    
    # Check if the file exists before proceeding
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    
    try:
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as fp:
            questions = json.load(fp)
        
        # Ensure the file is not empty
        if not questions:
            print(f"Error: The file '{file_path}' contains no questions.")
            return None
        
        # Select a random question
        rand_id = random.randrange(len(questions))
        selected = questions[rand_id]
        
        # Remove the selected question from the list
        questions.pop(rand_id)
        
        # Save the updated list back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=4)
        
        # Return the selected question
        return {
            "id": selected.get("id"),
            "question": selected.get("code"),
            "options": selected.get("options"),
            "answer": selected.get("answer")
        }
    
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{file_path}'. Please ensure the file is properly formatted.")
        return None
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
