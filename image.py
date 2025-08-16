import json
import random

def get_random_image():
    with open('image.json','r',encoding='utf-8') as file:
       data=json.load(file)

       rand_id=random.randrange(len(data))
       question=data[rand_id]
       return {
            "id": question.get("id"),
            "image": question.get("image"),
            "options": question.get("options"),
            "answer": question.get("answer")
        }
if __name__ == "__main__":
    print(get_random_image())