import os
import json
import csv

# Path to your root messages directory
root_dir = 'messages'
output_csv = 'messages.csv'

# Prepare the CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        'MessageID', 'Timestamp', 'Contents', 'Attachments',
        'ChannelID', 'ChannelType'
    ])
    writer.writeheader()

    # Traverse through all channel folders
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        # Load channel metadata
        channel_path = os.path.join(folder_path, 'channel.json')
        messages_path = os.path.join(folder_path, 'messages.json')
        
        if not os.path.exists(channel_path) or not os.path.exists(messages_path):
            continue

        with open(channel_path, 'r', encoding='utf-8') as ch_file:
            channel_data = json.load(ch_file)
            channel_id = channel_data.get('id', 'unknown')
            channel_type = channel_data.get('type', 'unknown')

        # Load messages
        with open(messages_path, 'r', encoding='utf-8') as msg_file:
            messages = json.load(msg_file)
            for msg in messages:
                writer.writerow({
                    'MessageID': msg.get('ID', ''),
                    'Timestamp': msg.get('Timestamp', ''),
                    'Contents': msg.get('Contents', ''),
                    'Attachments': msg.get('Attachments', ''),
                    'ChannelID': channel_id,
                    'ChannelType': channel_type
                })

print(f"✅ Done! Output saved to '{output_csv}'")
