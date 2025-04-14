import pandas as pd
from wordcloud import WordCloud
from PIL import Image

# Load the CSV file
df = pd.read_csv('messages.csv')

# Extract the 'contents' column
text = ' '.join(df['Contents'].dropna())

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

wordcloud.to_file('word_cloud.png')