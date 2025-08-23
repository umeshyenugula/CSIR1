import json
import random
import os
import sys

def resource_path(relative_path):
    """
    Returns the correct resource path for development and packaged app modes.
    """
    try:
        base_path = sys._MEIPASS  # This is used when packaged with PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # This is used during development
    return os.path.join(base_path, relative_path)

def get_random_riddle(file_path="QUESTIONS/CURRENT/riddles.json"): 
    file_path = resource_path(file_path)  # Resolve platform-independent file path
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    
    try:
        # Open and load the JSON data
        with open(file_path, 'r', encoding='utf-8') as fp:
            questions = json.load(fp)

        if not questions:
            print(f"Error: The file '{file_path}' contains no riddles.")
            return None

        # Select a random riddle
        random_id = random.randrange(len(questions))
        selected_question = questions[random_id]
        code = selected_question['code']
        options = selected_question['options']
        correct_answer = selected_question['answer']

        # Remove the selected question from the list
        questions.pop(random_id)

        # Write the updated list of questions back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=4)

        return {'code': code, 'options': options, 'answer': correct_answer}

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{file_path}'.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
