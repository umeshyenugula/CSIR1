import json
import random
import os

def get_random_question(file_path="round1easyquestions.json"):
    
    with open(file_path, 'r', encoding='utf-8') as fp:
        questions = json.load(fp)

    random_id = random.randrange(1,len(questions)+1)
    selected_question = questions[random_id]
    code= selected_question['code']
    options=selected_question['options']
    correct_answer=selected_question['answer']

   
    #questions.pop(random_id)
    # with open(file_path, 'w', encoding='utf-8') as f:
    #     json.dump(questions, f, indent=4)
    print(code)
    print("\n")
    for i in options:
        print(i)
    print()
    answer=input()
    if(answer.strip().lower()==correct_answer.strip().lower()):
        print("You got the correct answer")
    else:
        print("You have choosen the wrong answer")


   
    
if __name__ == "__main__":
    get_random_question()