import requests
import os

botId = os.environ.get('STOCK_BOT_ID')

data = {'bot_id': botId,
        'text': 'test with environment variable'}

res = requests.post('https://api.groupme.com/v3/bots/post', data=data)
res.raise_for_status()
print(res.status_code)
print(res.text)
