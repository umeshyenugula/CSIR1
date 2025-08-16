import random
import json
import os
import sys
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)
def get_random_truth_question(file_path='truth.json'):
    file_path = resource_path(file_path)  
    try:
        with open(file_path, 'r', encoding='utf-8') as fp:
            questions = json.load(fp)
            if not questions:
                raise ValueError("Empty question file.")
            rand_id = random.randrange(len(questions))
            selected = questions[rand_id]
            # questions.pop(random_id)
    # with open(file_path, 'w', encoding='utf-8') as f:
    #  json.dump(questions, f, indent=4)
            return {
                "id": selected.get("id"),
                "question": selected.get("code"),
                "options": selected.get("options"),
                "answer": selected.get("answer")
            }
    except Exception as e:
        print(f"Error loading question: {e}")
        return None
