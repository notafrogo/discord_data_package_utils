import json
import emoji

with open('./account/user.json', 'r') as f:
    user = json.load(f)

frecency = user['settings']['frecency']

emojiFrecency = frecency['emojiFrecency']['emojis']

sorted_emojis = sorted(emojiFrecency.items(), key=lambda x: x[1]['score'], reverse=True)

print("Emoji Scoreboard (sorted by score):")
for emoji_name, data in sorted_emojis:
    emoji_character = emoji.emojize(f":{emoji_name}:")
    print(f"{emoji_character} {emoji_name}: {data['score']}")