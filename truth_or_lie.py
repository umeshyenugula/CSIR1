import random
import os
import json

def get_question(file_path):
    with open(file_path, 'r', encoding='utf-8') as fp:
         questions=json.load(fp)
    random_id=random.randrange(len(questions))
    selected_question=questions[random_id]
    code=selected_question['code']
    options=selected_question['options']
    answer=selected_question['answer']
   
    # questions.pop(random_id)
    # with open(file_path, 'w', encoding='utf-8') as f:
    #  json.dump(questions, f, indent=4)
    option_letters=['a','b','c']
    option_map={}
    
    for i,option_text in enumerate(options):
        letter=option_letters[i]
        print(f"{letter.upper()}. {option_text}")
        option_map[letter]=option_text



    user_choice=input("Choose one of the option:   ")

    selected_option=option_map[user_choice.strip().lower()]
    if selected_option.lower()==answer.lower():
        print("Yay You guessed the correct answer")
    else:
        print("Sorry you are wrong ")
if __name__=="__main__":
    get_question("truth.json")
    
