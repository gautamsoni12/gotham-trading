import requests
from models import NewsArticle
from service import MongoService as ms 
import json
from bson import json_util, ObjectId
import json

def get_daily_news(date: str):
    
    try:
        query = {'time_published': {'$regex': date}}
        result = ms.get_from_mongo(query, 'ticker_news')
        if len(result) > 0:
            
            return json.loads(JSONEncoder().encode(result))
        else:
            url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey=FD84XWAC8MLSCKM4'
            r = requests.get(url)
            data = r.json()
            # data = load_json_file('controller/test_data.json')
            
            for article in data['feed']:
                if ms.check_if_title_exists_in_collection(article['title'], 'ticker_news'):
                    continue
                else:
                    news_article = json.loads(json_util.dumps(article))
                    print(news_article)
                    save_result = ms.save_to_mongo(news_article, 'ticker_news')

            return data
        
    except Exception as e:
        print(e)
        return None
    

def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)