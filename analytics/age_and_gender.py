# 

import json
import os
from collections import defaultdict

def extract_age_and_gender(file_path):
    """
    Reads a JSON file, searches for 'predicted_age' and 'predicted_gender',
    and returns the lines containing those keys in a prettified JSON format.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    results = defaultdict(list)
    
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                if 'predicted_age' in data:
                    results['predicted_age'].append(data)
                if 'predicted_gender' in data:
                    results['predicted_gender'].append(data)
            except json.JSONDecodeError:
                continue

    return json.dumps(results, indent=4)

if __name__ == "__main__":
    file_path = "./activity/analytics/events-2025-00000-of-00001.json"
    try:
        prettified_data = extract_age_and_gender(file_path)
        print(prettified_data)
    except FileNotFoundError as e:
        print(e)