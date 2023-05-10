This repo contains source code for my pet project. Further updates may be commited here in the future.

FEATURES:
-User authentication using Telegram bot API capacities
-Scheduled notifications and checking if the user has taken a pill
-Users are able to unsubscribe from the notifications if they want so.

TECHSTACK:
-Python 3.11 (with strong use of asyncio adn threading)
-sqlite3.
-PyTelegramBotAPI

CONFIGURATION.
-For local testing store your API key inside .env file in the root of the project. Var: TOKEN=YOUR_API_KEY
-To change the frequency of notifications tweak the time_logic function. Note that "sender" coroutine also changes and updates other parameters of the object (see Girlclass), so you better initiate takepill_checker instead.
-Messages are written in russian, so you would need to change noticiations to your language. 

DEPLOYMENT SUGGESTIONS:
The bot can be easily deployed with Docker.
NOTE:
1. Before CMD python main.py, run 

python dblogic.py

This command will create a file containing database and create a table with all necessary fiels.

2. Declare your API key as an env variable inside your docker file or while running a Docker container.
3. 
