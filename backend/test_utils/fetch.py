import json
from pytrends.request import TrendReq

# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

def get_top_three_trends():
    trends = pytrends.trending_searches(pn='india').head(3)
    return trends[0].tolist()

def get_interest_data(keyword):
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='IN', gprop='')
    interest_over_time = pytrends.interest_over_time()
    interest_over_time.index = interest_over_time.index.strftime('%Y-%m-%d')  # Format the dates
    interest_by_region = pytrends.interest_by_region()
    return interest_over_time.to_dict(), interest_by_region.to_dict()


def main():
    top_trends = get_top_three_trends()
    trends_data = {}

    for trend in top_trends:
        over_time, by_region = get_interest_data(trend)
        trends_data[trend] = {
            "interest_over_time": over_time,
            "interest_by_region": by_region
        }

    # Store data in JSON
    with open('trends_data.json', 'w') as json_file:
        json.dump(trends_data, json_file, indent=4)

if __name__ == "__main__":
    main()




