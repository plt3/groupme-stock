import requests
import bs4
from tickerNames import TICKER_NAMES


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


with open('29_99_day_sums.txt') as f:
    last29Sum, last99Sum = [float(n) for n in f.read().split('\n')]

if open('bearishBool.txt').read() == '30>100':
    bearishBool = False
else:
    bearishBool = True

nowPrice = getPrice(TICKER_NAME)
sma30 = (last29Sum + nowPrice) / 30
sma100 = (last99Sum + nowPrice) / 100

if sma30 > sma100:
    nowBear = False
elif sma30 < sma100:
    nowBear = True
else:
    nowBear = bearishBool
    print('Placeholder for going apeshit in the Discord')

if nowBear != bearishBool:
    print('Placeholder for going apeshit in the Discord')

with open('bearishBool.txt', 'w') as f:
    if nowBear:
        f.write('30<100')
    else:
        f.write('30>100')

# check that all the logic is right and hit a different conditional if it's
# the first run of the day
# also try to modularize and add support for different date ranges
