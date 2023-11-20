import requests
from bs4 import BeautifulSoup

def fetch_top_news():
    URL = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"  # Example RSS Feed
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, features="xml")
    headlines = soup.findAll('item')
    
    top_news = []
    for news in headlines[:3]:  # Fetching top 3 news
        title = news.title.text
        link = news.link.text
        top_news.append({'title': title, 'link': link})
    return top_news

print(fetch_top_news())
