from pytrends.request import TrendReq

def get_trending_topics():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrends.trending_searches()
    return trending_searches_df.head(3).values.flatten().tolist()

top_topics = get_trending_topics()
print(top_topics)

