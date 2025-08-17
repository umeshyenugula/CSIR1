import os
import shutil
import json
import random

BASE_DATA_DIR = os.path.dirname(__file__)
CURRENT_QUESTIONS_DIR = os.path.join(os.path.dirname(__file__), 'CURRENT')

def copy_round_files(round_name: str) :
    source_dir = os.path.join(BASE_DATA_DIR, round_name)
    print(f"Clearing existing files in {CURRENT_QUESTIONS_DIR}")
    for filename in os.listdir(CURRENT_QUESTIONS_DIR):
        file_path = os.path.join(CURRENT_QUESTIONS_DIR, filename)
        os.unlink(file_path)
    print(f"Copying new JSON files from {source_dir} to {CURRENT_QUESTIONS_DIR}")
    copied_count = 0
    for filename in os.listdir(source_dir):
        if filename.endswith('.json'):
            source_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(CURRENT_QUESTIONS_DIR, filename)
            shutil.copy2(source_path, dest_path)
            print(f"  - Copied: {filename}")
            copied_count += 1
    print(f"Successfully copied {copied_count} JSON files for round '{round_name}'.")

if __name__ == "__main__":
    selected_round = "R12"
    print(f"\n--- Copying Round: {selected_round} ---")
    copy_round_files(selected_round)
        
    
   