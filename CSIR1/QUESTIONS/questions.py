import os
import shutil
import json
import random
BASE_DATA_DIR = os.path.dirname(__file__)
CURRENT_QUESTIONS_DIR = os.path.join(os.path.dirname(__file__), 'CURRENT')
def copy_round_files(round_name: str) :
    source_dir = os.path.join(BASE_DATA_DIR, round_name)
    for filename in os.listdir(CURRENT_QUESTIONS_DIR):
        file_path = os.path.join(CURRENT_QUESTIONS_DIR, filename)
        os.unlink(file_path)
    copied_count = 0
    for filename in os.listdir(source_dir):
        if filename.endswith('.json'):
            source_path = os.path.join(source_dir, filename)
            dest_filename = filename
            name_part, ext_part = os.path.splitext(filename)
            dest_filename = name_part[:-4] + ext_part

            dest_path = os.path.join(CURRENT_QUESTIONS_DIR, dest_filename)
            shutil.copy2(source_path, dest_path)
            copied_count += 1
    
        
    
   