import csv
from datetime import datetime

input_csv = 'all_messages.csv'
output_csv = 'all_messages_sorted.csv'

# Read and sort the CSV rows
with open(input_csv, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    messages = list(reader)

# Convert timestamps and sort
messages.sort(key=lambda x: datetime.strptime(x['Timestamp'], '%Y-%m-%d %H:%M:%S'))

# Write to a new sorted CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(messages)

print(f"✅ Sorted messages saved to '{output_csv}'")
