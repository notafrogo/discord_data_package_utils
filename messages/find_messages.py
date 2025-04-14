import csv
import os
import discord
from discord.ext import commands
from dotenv import dotenv_values

env = dotenv_values()

TOKEN = env['DISCORD_TOKEN']
bot = commands.Bot(command_prefix='!')

if not os.path.exists('dm_messages.csv'):
    with open('messages.csv', mode='r') as infile, open('dm_messages.csv', mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            if row['ChannelType'] in ['GROUP_DM', 'DM']:
                writer.writerow(row)

existing_channels = []
non_existing_channels = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    with open('dm_messages.csv', mode='r') as infile:
        reader = csv.DictReader(infile)

        if not os.path.exists('channels'):
            os.makedirs('channels')

        for row in reader:
            channel_id = row['ChannelID']
            message_id = row["MessageID"]

            channel = None

            if channel_id not in existing_channels and channel_id not in non_existing_channels:
                input(f"Press enter to continue: {channel_id}")
                channel = bot.get_channel(channel_id)

            if channel_id in existing_channels or channel:
                existing_channels.append(channel_id)
                print(f'Found channel {channel_id}.')
                if not os.path.exists(f'channels/{channel_id}.txt'):
                    with open(f'channels/{channel_id}.txt', mode='w') as f:
                        pass
                
                with open(f'channels/{channel_id}.txt', mode='a') as f:
                    f.write(f'https://discord.com/channels/@me/{channel_id}/{message_id}\n')
            
            else:
                non_existing_channels.append(channel_id)
                print(f'Channel {channel_id} not found.')
                continue

    await bot.close()


bot.run(TOKEN)