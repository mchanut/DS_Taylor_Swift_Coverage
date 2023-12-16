import json
import re
import requests

QUERY_URL_TEMPLATE = ('https://newsapi.org/v2/everything?'
                      'language=en&'
                      'q={}&'
                      'searchIn=title,description&'
                      'from={}&'
                      'to={}'
                      'sortBy=popularity&'
                      'apiKey={}')


def fetch_latest_news(api_key, news_keywords, start_date, end_date):
    
    # Check if there are keywords passed
    if not news_keywords :
        raise ValueError("No keywords were provided.")
    
    # Check if the API key contains an invalid character
    if re.search(r"[^A-z0-9]", api_key):
        raise ValueError("API key contains non-alphanumeric characters.")

    # Transform variables to appropriate URL format
    keyword_list = []
    for key in news_keywords:
        keyword_list.append('("' + key + '")')
    formatted_keywords = 'OR'.join(keyword_list)
    print(formatted_keywords)

    # Format the query URL
    url = QUERY_URL_TEMPLATE.format(formatted_keywords, start_date, end_date, api_key)

    # Send request to the API
    response = requests.get(url)

    # If response was unsuccessful, return error
    if response.status_code != 200:
        raise Exception(f"Unable to fetch the latest news containing {news_keywords} from {start_date} to {end_date}.")
    
    # Otherwise load the response json file
    data = response.json()

    # Get the articles
    articles = data["articles"]
    
    undesirables = ["BBC News", "The Indian Express", "Quartz India", "Sky.com", "ABC News (AU)"]
    
    filtered_articles = []
    for article in articles:
        if article["title"] != "[Removed]" and article["description"] != "[Removed]":
            if article["source"]["name"] not in undesirables:
                filtered_articles.append(article)

    return filtered_articles

# If we want only the TITLE and DESCRIPTION
def clean_articles(articles):
    
    cleaned_articles = []
    
    for article in articles:
        info = {
            "title" : article["title"],
            "description" : article["description"]
        }
        cleaned_articles.append(info)
        
    return cleaned_articles