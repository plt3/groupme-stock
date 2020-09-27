import os
import requests
import bs4


def getPrice(ticker):  # get current price for given ticker
    url = f'https://finance.yahoo.com/quote/{ticker}'
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    numDiv = soup.find('div', class_='D(ib) Mend(20px)')
    priceSpan = next(numDiv.children)
    rawPrice = priceSpan.getText()
    price = float(rawPrice.replace(',', ''))

    return price


def sendGroupMe(message):
    botId = os.environ.get('STOCK_BOT_ID')

    data = {'bot_id': botId,
            'text': message}

    res = requests.post('https://api.groupme.com/v3/bots/post', data=data)
    res.raise_for_status()

