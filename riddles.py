import json
import random

def get_random_question(file_path= r"C:\Users\Mallikarjun\Desktop\opencv_project\csiround1\riddles.json"):
    
    with open(file_path, 'r', encoding='utf-8') as fp:
        questions = json.load(fp)

    random_id = random.randrange(len(questions))
    selected_question = questions[random_id]
    code = selected_question['code']
    options = selected_question['options']
    correct_answer = selected_question['answer']

    print(code)
    print("\n")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    print()
    
    answer = input("Enter option number or text: ").strip()

    # If they entered a number, map it to the option
    if answer.isdigit():
        idx = int(answer)
        if 1 <= idx <= len(options):
            answer = options[idx - 1]  # map number → option text
        else:
            print("Invalid option number.")
            return

    if answer.strip().lower() == correct_answer.strip().lower():
        print("You got the correct answer ✅")
    else:
        print(f"You have chosen the wrong answer ❌\nCorrect answer: {correct_answer}")


if __name__ == "__main__":
    get_random_question()
