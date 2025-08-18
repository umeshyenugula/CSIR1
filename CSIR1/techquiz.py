import json
import random
import sys
import os
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def get_random_question(file_path="QUESTIONS/CURRENT/technical.json"):  
    file_path = resource_path(file_path) 
    with open(file_path, 'r', encoding='utf-8') as fp:
        questions = json.load(fp)
    random_id = random.randrange(len(questions))
    selected_question = questions[random_id]
    code = selected_question['code']
    options = selected_question['options']
    correct_answer = selected_question['answer']
    questions.pop(random_id)
    with open(file_path, 'w', encoding='utf-8') as f:
     json.dump(questions, f, indent=4)
    return {
        'code': code,
        'options': options,
        'answer': correct_answer
    }
