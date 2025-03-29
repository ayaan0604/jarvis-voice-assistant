api_key="d05867f830a04e69b8a53b0bcc2ef63d"

import requests

class news:
    def __init__(self,title,description,link):
        self.title=title
        self.description=description
        self.link=link
        
def get_news():
    url = (f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={api_key}")

    response = requests.get(url)
    articles=response.json()['articles']
    
    headlines=[]
    
    for news in articles:
        recieved_news=(news["title"],news["description"],news['url'])
        headlines.append(recieved_news)
    return headlines    

