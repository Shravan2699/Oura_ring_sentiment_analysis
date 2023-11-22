import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as plt
from afinn import Afinn

#1.TRUSTPILOT
# URL of the product reviews page on trustpilot
base_url = 'https://ca.trustpilot.com/review/ouraring.com?page={}'
num_pages = 42
rating_arr = []
review_arr = []
afinn = Afinn()

for page_number in range(1, num_pages + 1):
    # Construct the URL for the current page
    url = base_url.format(page_number)

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the script tag containing JSON data
    script_tag = soup.find('script', {'type': 'application/json'})


    if script_tag:
        json_data = json.loads(script_tag.contents[0])


        reviews = json_data['props']['pageProps']['reviews']
        ratings = json_data['props']['pageProps']
        review_dict = {}
        total_reviews = json_data['props']['pageProps']['reviews'][0].keys()
        # print(total_reviews)
        review_dict = {}
        for idx in range(len(reviews)):
            # print(idx)
            review_text = json_data['props']['pageProps']['reviews'][idx]['text']
            rating = json_data['props']['pageProps']['reviews'][idx]['rating']
            review_dict[rating] = review_text
            # print(rating)
            rating_arr.append(rating)
            review_arr.append(review_text)

print(len(review_arr))
data = {'rating' : rating_arr,'review': review_arr}
df = pd.DataFrame(data)
#Creating pandas dataframe with 'rating' and 'review' as the features

print(df['review'].values[0])

#Plotting the ratings count
rating_counts = df['rating'].value_counts().sort_index()
plt.bar(rating_counts.index, rating_counts.values)
plt.xlabel('rating')
plt.ylabel('Count')
plt.title('Rating Distribution')
plt.show()

#Checking the polarity of reviews
polarity_scores = [TextBlob(review).sentiment.polarity for review in review_arr]
overall_sentiment = sum(polarity_scores) / len(polarity_scores)
print(f"Overall Sentiment: {overall_sentiment}")
# plt.show()

plt.hist(polarity_scores, bins=[-1, -0.5, 0, 0.5, 1], edgecolor='black')
plt.xlabel('Sentiment Polarity')
plt.ylabel('Count')
plt.title('Sentiment Distribution')
plt.show()

all_text = ' '.join(review_arr)
words = all_text.split()
word_counts = Counter(words)
print("Most Common Words:")
for word, count in word_counts.most_common(10):
    print(f"{word}: {count}")

positive_words = []
negative_words = []

for review in review_arr:
    words = review.split()
    #split the review into words
    for word in words:
        score = afinn.score(word)
        #the afinn libary will sort the words into positive and negative for us
        if score > 0:
            positive_words.append(word)
        elif score < 0:
            negative_words.append(word)


positive_word_counts = Counter(positive_words)
negative_word_counts = Counter(negative_words)


#Plotting the top positive words
top_positive_words = positive_word_counts.most_common(10)
plt.bar([word[0] for word in top_positive_words], [count[1] for count in top_positive_words], color='green')
#top_positive_words is a list of tuples,where each tuple contains word and its count,on x-axis would be the word and on y-axis we will have the the count 
plt.xlabel('Positive Word')
plt.ylabel('Count')
plt.title('Top 10 Most Common Positive Words')
plt.xticks(rotation=90)
plt.show()

#Plotting the top negative words
top_negative_words = negative_word_counts.most_common(10)
plt.bar([word[0] for word in top_negative_words], [count[1] for count in top_negative_words], color='red')
plt.xlabel('Negative Word')
plt.ylabel('Count')
plt.title('Top 10 Most Common Negative Words')
plt.xticks(rotation=90)
plt.show()
