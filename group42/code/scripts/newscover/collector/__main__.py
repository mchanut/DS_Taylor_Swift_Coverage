import json
import os
import argparse
from newscover.newsapi import fetch_latest_news, clean_articles
from datetime import datetime, timedelta

'''
Wanted usage:

python3 -m newscover.collector -k <api_key> -c <count> -i <input_file> -o <output_dir>

'''

def remove_duplicates(articles, key):
    seen = set()
    unique_articles = []
    for article in articles:
        article_key = article[key]
        if article_key not in seen:
            seen.add(article_key)
            unique_articles.append(article)
    return unique_articles

def output_news(name, directory, api_key, keywords, max_articles):

    total_articles = []

    file_path = os.path.join(directory, f"{name}.json")
    with open(file_path, 'r', encoding='utf-8') as f:
        total_articles += json.load(f)

    count = 0

    # Set time range
    # 2023-11-09
    date = datetime.now()

    for _ in range(30):
        articles = fetch_latest_news(api_key, keywords, date.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d"))
        date = date - timedelta(days=1)

        total_articles += articles

        # Remove duplicates based on the article URL (you can use a different key if needed)
        total_articles = remove_duplicates(total_articles, key='description')
        if len(total_articles) >= max_articles:
            break

        #count = len(total_articles)
        
    print(len(total_articles))
    print(date)
    total_articles = total_articles[:max_articles]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(total_articles, f, indent=4, ensure_ascii=False)


def main():

    parser = argparse.ArgumentParser(description="News collector tool.")

    parser.add_argument("-k", "--key", required=True, metavar="<api_key>", help="Your newsapi.org API key")
    parser.add_argument("-c", "--count", required=True, type=int,  metavar="<count>", help="Number of articles to fetch.")
    parser.add_argument("-i", "--input", required=True, metavar="<input_file>", help="Keywords json file")
    parser.add_argument("-o", "--output", required=True, metavar="<output_dir>", help="Directory in which to output your news articles")

    args = parser.parse_args()

    api_key = args.key
    out_directory = args.output
    max_articles = args.count
    
    with open(args.input, 'r') as f:
        keywords = json.load(f)

    # Loop through input file and output fetched articles
    for key, value in keywords.items():
        output_news(key, out_directory, api_key, value, max_articles)


if __name__ == "__main__":
    main()