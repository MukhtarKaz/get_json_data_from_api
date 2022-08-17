import requests
import json
from urllib.parse import urlparse


class APIGateway:

    @staticmethod
    def get_articles_as_json(url: str, api_key: str) -> str:
        result = []
        # the URL structures can be passed separately as parameters if necessary. But for the sake of simplicity,
        # it was divided into 2 parts

        response_api = requests.get(url + api_key)
        data = response_api.text
        parse_json = json.loads(data)
        articles = parse_json['articles']

        if len(articles) > 0:
            for article in articles:
                parsed_url = urlparse(article['url'])
                cleaned_content = str(article['content']).replace("\r\n", " ")
                template = {
                    "source": article['source']['name'],
                    "author": article['author'],
                    "title": article['title'],
                    "description": article['description'],
                    "url": parsed_url.path,
                    "image_url": article['urlToImage'],
                    "published_at": article['publishedAt'],
                    "content": cleaned_content
                }
                result.append(template)
        else:
            raise Exception("Article list is empty")

        ready_json = json.dumps(result, indent=2)
        return ready_json


articles_data_url = "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey="
api_key = "af92652e76b745a6bde8dd2fc5739bfd"
ready_json_data = APIGateway.get_articles_as_json(articles_data_url, api_key)

print(ready_json_data)

# To write json data into file
with open("api_articles.json", "w") as file:
    json.dump(ready_json_data, file)
