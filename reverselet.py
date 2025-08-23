import json
import random
import os
import sys

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundles.
    """
    if hasattr(sys, '_MEIPASS'):  # When bundled by PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)

def getreverselet(file_path="QUESTIONS/CURRENT/reverselet.json"):  
    # Ensure cross-platform file path resolution
    file_path = resource_path(file_path)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None

    try:
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as fp:
            questions = json.load(fp)   

        if not questions:  # Ensure there are questions to pick
            print(f"Error: The file '{file_path}' contains no questions.")
            return None
        
        # Select a random question
        rid = random.randrange(len(questions))
        sq = questions[rid]    
        code = sq.get('question')  
        canswer = sq.get('answer') 
        
        # Remove the selected question
        questions.pop(rid)  

        # Save the updated list back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(questions, file, indent=4, ensure_ascii=False) 

        return {
            'code': code,
            'answer': canswer
        }

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in '{file_path}'.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
