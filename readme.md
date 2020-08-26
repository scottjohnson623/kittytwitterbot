This was created during my time as a Code Chrysalis student.

# Welcome to Kitty Bot

Kitty bot was designed to gain experience with Python and with container services and AWS hosting. Kittybot is currently deployed at https://twitter.com/xxKittybotxx

![alt text](https://i.gyazo.com/24df4a0d62c469595b0cd8316db313d3.png)

## How It Works

Kitty bot waits for mentions on its username, and then if the mention contains one of its keywords listed, it will search for either a random cat picture or a cat picture from a specific category (provided by TheCatAPI) and will reply to the user's message with it.

## Libraries Used

- Requests - for API calls
- Tweepy - for for connecting to Twitter
- Python-dotenv - for storing API keys in .env file

## How to get started

- Get developer keys from Twitter and TheCatApi
- Create .env file in root folder and add keys to .env file as follows:
  - CONSUMER_KEY =
  - CONSUMER_SECRET =
  - ACCESS_TOKEN =
  - ACCESS_TOKEN_SECRET =
  - CAT_API_KEY =
-
