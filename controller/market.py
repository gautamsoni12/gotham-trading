from market.reddit import RedditObject
from service import GPTInsight as gpt
from service import MongoService as ms
import json


async def marketSentiment():
    try:
        # Get text from reddit threads for the day
        reddit_obj = RedditObject(client_id="7Pxd0NY6amn80A", client_secret="mNZkScHDfYmUlxTK7I9bKtcvVtHa1A",
                                  user_agent="sas", sub_reddits_to_query_arr=["stocks"],
                                  sub_reddit_search_limit=10)
        reddit_result = reddit_obj.query_sub_reddit()
        
        # Pass it through GPT-4 to get stock tickers and sentiment
        gpt_4_query = "Below are the title and a post from subreddit. \
            Use the below sections identify stocks mentioned or dicussed. \
            For each stock, return a json object with following keys: sentiment_score, a trade_decision, and summary , of discussion about the stock."
        
        for result in reddit_result:
            for i in range(len(result["title"])):
                try:
                    if not ms.check_if_title_exists_in_collection(result["title"][i], 'reddit_feed'):
                        query = gpt_4_query + "\n" + result["title"][i] + " " + result["body"][i]
                        gpt_response = await gpt.ask(query)
                        
                        reddit_dict = {
                            "sub_reddit": result["sub_reddit"],
                            "title": result["title"][i],
                            "body": result["body"][i],
                            "sentiment": parse_response(gpt_response)
                        }
                        save_result = ms.save_to_mongo(reddit_dict, 'reddit_feed')
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
        
        return "Success"
    except Exception as e:
        print(f"An error occurred: {str(e)}")



def parse_response(response):
    try:
        # Remove '\n', `'`, and ``` characters from the response
        response = response.replace('\n', '').replace('\'', '').replace('`', '')
        # Find the index of the first '{' character
        json_start_index = response.find('{') or response.find('[')
        # Extract the JSON string from the response
        json_string = response[json_start_index:]
        # Parse the JSON string into a dictionary
        parsed_dict = json.loads(json_string)
        return parsed_dict
            
    except Exception as e:
        print(f"An error occurred while parsing the response: {str(e)}")
        return []

if __name__ == "__main__":
    print(marketSentiment())