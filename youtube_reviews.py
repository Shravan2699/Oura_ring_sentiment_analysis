#Import all the necessary libraries that we will use in this project
#In this code,we visit 3 youtube videos on oura ring and go throught the comments section and see what the responses of individuals are on Oura ring
import googleapiclient.discovery
import pandas as pd
import time
import html
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as plt
from afinn import Afinn
afinn = Afinn()

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyCDFAXEbQRnzoRW_gbjJWK3Rc1J9vtIg9Y"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


#Video1- Chase the summit- link: https://www.youtube.com/watch?v=o_vTIEoRRtI&t=1s&ab_channel=ChasetheSummit
video_id = "o_vTIEoRRtI"
max_results = 100
comments = []

# Initial request
request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=max_results
)
response = request.execute()

# Retrieve comments and nextPageToken
comments += response.get('items', [])
next_page_token = response.get('nextPageToken', None)

# Additional requests for more comments
while next_page_token:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        pageToken=next_page_token
    )
    response = request.execute()
    comments += response.get('items', [])
    next_page_token = response.get('nextPageToken', None)
    time.sleep(1)


# Process comments
comments_data = []
for item in comments:
    comment = item['snippet']['topLevelComment']['snippet']
    comments_data.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['updatedAt'],
        comment['likeCount'],
        comment['textDisplay']
    ])

df = pd.DataFrame(comments_data, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

comment_arr = []
for comment in df['text']:
    comment_arr.append(comment)


#Video2 - Most viewed Youtube video on Oura Ring from Unbox Therapy,link: https://www.youtube.com/watch?v=8hp1TEUqvW4&ab_channel=UnboxTherapy
video_id = "8hp1TEUqvW4"
max_results = 100
comments = []

# Initial request
request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=max_results
)
response = request.execute()

# Retrieve comments and nextPageToken
comments += response.get('items', [])
next_page_token = response.get('nextPageToken', None)

# Additional requests for more comments
while next_page_token:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        pageToken=next_page_token
    )
    response = request.execute()
    comments += response.get('items', [])
    next_page_token = response.get('nextPageToken', None)
    time.sleep(1)

# Process comments
comments_data = []
for item in comments:
    comment = item['snippet']['topLevelComment']['snippet']
    comments_data.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['updatedAt'],
        comment['likeCount'],
        comment['textDisplay']
    ])

df = pd.DataFrame(comments_data, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

for comment in df['text']:
    comment_arr.append(comment)


#Video3 - Jonny&Yusef,link-https://www.youtube.com/watch?app=desktop&v=G1E1GfQAE5o&ab_channel=Jonny%26Yusef-Propanefitness
video_id = "G1E1GfQAE5o"
max_results = 100
comments = []

# Initial request
request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=max_results
)
response = request.execute()

# Retrieve comments and nextPageToken
comments += response.get('items', [])
next_page_token = response.get('nextPageToken', None)

# Additional requests for more comments
while next_page_token:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        pageToken=next_page_token
    )
    response = request.execute()
    comments += response.get('items', [])
    next_page_token = response.get('nextPageToken', None)
    time.sleep(1)

# Process comments
comments_data = []
for item in comments:
    comment = item['snippet']['topLevelComment']['snippet']
    comments_data.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['updatedAt'],
        comment['likeCount'],
        comment['textDisplay']
    ])

df = pd.DataFrame(comments_data, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

# comment_arr = []
for comment in df['text']:
    comment_arr.append(comment)



decoded_comment_array = [html.unescape(text) for text in comment_arr]
comments_df = pd.DataFrame(decoded_comment_array,columns=['comments'])
print(comments_df['comments'][1600])


#Analysis Part
#After collecting some comments from youtube videos,its time to analyze the sentiments and polarity of the comments for primary research
polarity_scores = [TextBlob(comment).sentiment.polarity for comment in decoded_comment_array]
overall_sentiment = sum(polarity_scores) / len(polarity_scores)
print(f"Overall Sentiment: {overall_sentiment}")
# Overall Sentiment: 0.12948694223481125


plt.hist(polarity_scores, bins=[-1, -0.5, 0, 0.5, 1], edgecolor='black',color='violet')
plt.xlabel('Sentiment Polarity')
plt.ylabel('Count')
plt.title('Youtube Comments Sentiment Distribution')
plt.show()


#Checking the most comment positive and negative words in youtube comments

positive_words = []
negative_words = []

for comment in decoded_comment_array:
    words = comment.split()
    #split the review into words
    for word in words:
        score = afinn.score(word)
        #the afinn libary will sort the words into positive and negative for us
        if score > 0:
            positive_words.append(word)
        elif score < 0:
            negative_words.append(word)

print(f'Positive words: {len(positive_words)}')
print(f'Negative words: {len(negative_words)}')

# Results
# Positive words: 2194
# Negative words: 1038

positive_word_counts = Counter(positive_words)
negative_word_counts = Counter(negative_words)


#Checking the top 10 most common positive words in comments
top_positive_words = positive_word_counts.most_common(10)
plt.bar([word[0] for word in top_positive_words], [count[1] for count in top_positive_words], color='blue')
#top_positive_words is a list of tuples,where each tuple contains word and its count,on x-axis would be the word and on y-axis we will have the the count 
plt.xlabel('Positive Word')
plt.ylabel('Count')
plt.title('Top 10 Most Common Positive Words in Youtube Comments')
plt.xticks(rotation=90)
plt.show()


top_negative_words = negative_word_counts.most_common(10)
plt.bar([word[0] for word in top_negative_words], [count[1] for count in top_negative_words], color='grey')
plt.xlabel('Negative Word')
plt.ylabel('Count')
plt.title('Top 10 Most Common Negative Words in Youtube Comments')
plt.xticks(rotation=90)
plt.show()




