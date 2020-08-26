import tweepy
import logging
from config import create_api
import time
import requests 
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Nya! Retrieving mentions")
    new_since_id = since_id
    ## Getting new tweets
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
    ## checking its not a reply
        if tweet.in_reply_to_status_id is not None:
            continue
    ## if it contains a keyword specified in the function, reply, and follow the user if needed
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()
            if "hat" in tweet.text.lower():
                url = "https://api.thecatapi.com/v1/images/search?category_ids=1"
            elif "clothes" in tweet.text.lower():
                url = "https://api.thecatapi.com/v1/images/search?category_ids=15"
            elif "box" in tweet.text.lower():
                url = "https://api.thecatapi.com/v1/images/search?category_ids=5"
            elif "sink" in tweet.text.lower():
                url = "https://api.thecatapi.com/v1/images/search?category_ids=14"
            elif "space" in tweet.text.lower():
                url = "https://api.thecatapi.com/v1/images/search?category_ids=2"
            elif "sunglasses" in tweet.text.lower():
                url = "https://api.thecatapi.com/v1/images/search?category_ids=4"
            else:
                url = "https://api.thecatapi.com/v1/images/search?category_ids=7"
            
            message = "Nya! Enjoy :3"
            filename = 'temp.jpg'
            headers = { 'x-api-key' : os.environ.get("CAT_API_KEY") }
            request1 = requests.get(url, headers = headers, stream=True)
            request1 = request1.json()
            request1image = request1[0]["url"]
            request2 = requests.get(request1image)
            if request2.status_code == 200:

                with open(filename, 'wb') as image:
                    for chunk in request2:
                        image.write(chunk)

                api.update_with_media(filename, status=message, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                os.remove(filename)
           
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["cat", "please", "kitty", "kat"], since_id)
        logger.info("Waiting...")
        ##wait 1 minute before checking mentions again
        time.sleep(60)
##calling it again if it's executed from the main file  
if __name__ == "__main__":
    main()
