import json
import random
import os
import sys
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)
def getreverselet(file_path="questions.json"):  
    file_path = resource_path(file_path)     
    with open(file_path, 'r', encoding='utf-8') as fp:
        questions = json.load(fp)   
    rid = random.randrange(len(questions))
    sq = questions[rid]    
    code = sq.get('question')  
    canswer = sq.get('answer') 
    # questions.pop(random_id)
    # with open(file_path, 'w', encoding='utf-8') as f:
    #  json.dump(questions, f, indent=4)   
    return {
        'code': code,
        'answer': canswer
    }
