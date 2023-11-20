from turtle import pd
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
import string
# import tweepy
from pytrends.request import TrendReq
from apscheduler.schedulers.background import BackgroundScheduler
import json

# Twitter API keys (replace with your actual keys)
# CONSUMER_KEY = 'your_consumer_key'
# CONSUMER_SECRET = 'your_consumer_secret'
# ACCESS_TOKEN = 'your_access_token'
# ACCESS_SECRET = 'your_access_secret'

# News sources
NEWS_SOURCES = {
    "The Hindu": "https://www.thehindu.com/news/rss",
    "NDTV": "https://www.ndtv.com/rss",
    "Indian Express": "https://indianexpress.com/rss",
}

# Database file
DB_FILE = 'news_data.json'

def fetch_news():
    all_news = {}
    for source, url in NEWS_SOURCES.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, features="xml")
                headlines = soup.findAll('item')[:5]  # Fetch top 5 for analysis
                all_news[source] = [{'title': item.title.text, 'link': item.link.text} for item in headlines]
            else:
                print(f"Error fetching from {source}: HTTP Status Code {response.status_code}")
        except requests.RequestException as e:
            print(f"Request error fetching from {source}: {e}")
        except Exception as e:
            print(f"General error fetching from {source}: {e}")
    return all_news


def extract_keywords(text):
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    keywords = [word.lower() for word in tokens if word.lower() not in stop_words]
    return keywords

# def get_twitter_trends():
#     auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#     auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
#     twitter_api = tweepy.API(auth)

#     trends = twitter_api.trends_place(1)  # 1 for worldwide
#     trending_topics = [trend['name'] for trend in trends[0]['trends']]
#     return trending_topics

def get_google_trends(keywords):
    pytrends = TrendReq()
    try:
        pytrends.build_payload(kw_list=keywords)
        trends_data = pytrends.interest_over_time()
        return trends_data
    except Exception as e:
        print(f"Error fetching Google Trends data: {e}")
        return pd.DataFrame()  # Returning an empty DataFrame as a fallback


def analyze_top_news(news_data):
    keyword_frequency = Counter()
    for source, articles in news_data.items():
        for article in articles:
            keywords = extract_keywords(article['title'])
            keyword_frequency.update(keywords)

    top_keywords = keyword_frequency.most_common(10)
    top_keywords = [keyword for keyword, _ in top_keywords]

    # Integrate Twitter and Google Trends data
    # twitter_trends = get_twitter_trends()
    google_trends = get_google_trends(top_keywords).sum().sort_values(ascending=False).index.tolist()

    # Adjust relevance based on Twitter and Google Trends
    # Implement your logic here

    # Select top 3 topics
    top_news_topics = select_top_news_topics(news_data, top_keywords, google_trends)
    return top_news_topics

def select_top_news_topics(news_data, top_keywords,google_trends):
    # Scoring weights (can be adjusted)
    base_weight = 1
    twitter_weight = 2
    google_weight = 3

    scores = {}
    for keyword in top_keywords:
        scores[keyword] = base_weight * (news_data[keyword] if keyword in news_data else 0)

        # # Increase score if keyword is in Twitter trends
        # if keyword in twitter_trends:
        #     scores[keyword] += twitter_weight

        # Further increase score if keyword is high in Google Trends
        if keyword in google_trends:
            scores[keyword] += google_weight

    # Sort topics by their scores
    sorted_topics = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    # Select top 3 unique topics
    top_news_topics = []
    for topic, score in sorted_topics:
        if len(top_news_topics) >= 3:
            break
        if all(topic not in article['title'] for article in top_news_topics):
            top_news_topics.append(next(article for article in news_data if topic in article['title']))

    return top_news_topics


def update_top_news():
    try:
        news_data = fetch_news()
        top_news = analyze_top_news(news_data)
        
        with open(DB_FILE, 'w') as file:
            json.dump(top_news, file)
    except Exception as e:
        print(f"Error during news update: {e}")

def get_top_news():
    try:
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("News data file not found. Please check if the update process has run at least once.")
        return []
    except json.JSONDecodeError:
        print("Error decoding the news data file. The file might be corrupted.")
        return []
    except Exception as e:
        print(f"General error accessing the news data file: {e}")
        return []


if __name__ == '__main__':
    update_top_news()
    print(get_top_news())
