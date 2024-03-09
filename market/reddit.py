import praw
import os
import pandas as pd
import datetime as dt
from market import config

class RedditObject:
    def __init__(self, client_id, client_secret, user_agent, sub_reddits_to_query_arr, sub_reddit_search_limit):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        self.sub_reddits_to_query_arr = sub_reddits_to_query_arr
        self.sub_reddit_search_limit = sub_reddit_search_limit
        self.topics_dict = {}

        self.reddit_obj = praw.Reddit(client_id=client_id, client_secret=self.client_secret,
                             user_agent=self.user_agent, username=config.username, password=config.password)

    def query_sub_reddit(self):
        
        result = []
        
        for sub_reddit in self.sub_reddits_to_query_arr:
            subreddit = self.reddit_obj.subreddit(sub_reddit)
            top_subreddit = subreddit.new(limit=self.sub_reddit_search_limit)
            topics_dict = {
                "sub_reddit": sub_reddit,
                "title": [],
                       "score": [],
                       "id": [],
                       "url": [],
                       "comms_num": [],
                       "created": [],
                       "body": []}

            for submission in top_subreddit:
                topics_dict["title"].append(submission.title)
                topics_dict["score"].append(submission.score)
                topics_dict["id"].append(submission.id)
                topics_dict["url"].append(submission.url)
                topics_dict["comms_num"].append(submission.num_comments)
                topics_dict["created"].append(submission.created)
                topics_dict["body"].append(submission.selftext)

            self.topics_dict = pd.DataFrame(topics_dict)
            result.append(topics_dict)
        
        return result


    def search_dict_for_tickers(self):
        ticker_mentions = 0
        for topic in self.topics_dict["title"]:
            if topic.find("Bitcoin") != -1:
                ticker_mentions += 1

        print("ticker mentions {}".format(ticker_mentions))




if __name__ == '__main__':
    reddit_obj = RedditObject(client_id="7Pxd0NY6amn80A", client_secret="mNZkScHDfYmUlxTK7I9bKtcvVtHa1A",
                              user_agent="sas", sub_reddits_to_query_arr=["CryptoCurrency"],
                              sub_reddit_search_limit=500)
    reddit_result = reddit_obj.query_sub_reddit()
    
    print(reddit_result[0]["title"])
    

# print(topics_data["body"][495])