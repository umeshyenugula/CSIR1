import json
import random
import sys
import os

def resource_path(relative_path):
    """
    Returns the correct resource path for both development and packaged modes.
    """
    try:
        base_path = sys._MEIPASS  # This is used when the app is packaged with PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # This is used during development
    return os.path.join(base_path, relative_path)

def get_random_question(file_path="QUESTIONS/CURRENT/technical.json"):  
    """
    Returns a random question from the provided JSON file and removes the selected question.
    """
    file_path = resource_path(file_path)  # Get the full file path
    
    # Check if the file exists before proceeding
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    
    try:
        # Open and load the JSON file
        with open(file_path, 'r', encoding='utf-8') as fp:
            questions = json.load(fp)

        # Check if there are any questions in the file
        if not questions:
            print(f"Error: The file '{file_path}' contains no questions.")
            return None

        # Select a random question
        random_id = random.randrange(len(questions))
        selected_question = questions[random_id]
        code = selected_question['code']
        options = selected_question['options']
        correct_answer = selected_question['answer']

        # Remove the selected question from the list
        questions.pop(random_id)

        # Write the updated questions back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=4)

        return {
            'code': code,
            'options': options,
            'answer': correct_answer
        }

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{file_path}'. Please ensure the file is properly formatted.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
