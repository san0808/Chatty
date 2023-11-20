import requests
from serpapi import GoogleSearch

def fetch_urls(search_query, engine='google', num_results=10):

    api_key = "f8e859730c3886c08bda00514e0d1776917cd13254c96b2f30fdfe0e977ba515"  

    if engine == 'google':
        params = {
            "engine": engine,
            "q": search_query,
            "api_key": api_key,
            "num": num_results
        }
        search = GoogleSearch(params)
        results = search.get_dict()["organic_results"]

    else:
        params = {
            "engine": engine,
            "q": search_query,
            "api_key": api_key,
            "count": num_results
        }
        response = requests.get("https://serpapi.com/search.json", params=params)
        results = response.json().get("organic_results", [])

    links_profiles = []
    for link in results:
        links_profiles.append({"Title": link.get('title', ''), "URL": link.get('link', '')})

    return links_profiles

if __name__ == "__main__":
    query = "Portugal vs Iceland"
    fetched_urls = fetch_urls(query)
    for item in fetched_urls:
        print(item)
