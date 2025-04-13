import json

def search_in_large_json(file_path, search_text):
    buffer_size = 1024 * 1024
    result = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        while chunk := file.read(buffer_size):
            start_index = chunk.find(search_text)
            if start_index != -1:
                start_context = max(0, start_index - 300)
                end_context = start_index + len(search_text) + 300
                result.append(chunk[start_context:end_context])
    
    return result

file_path = "activity/analytics/events-2025-00000-of-00001.json"
search_text = "predicted_age"
matches = search_in_large_json(file_path, search_text)

for match in matches:
    print(match)
    print("=" * 80)
