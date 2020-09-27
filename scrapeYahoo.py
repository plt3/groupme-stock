import json
import requests
import bs4
from tickerNames import TICKER_NAMES, AVERAGE_LENGTHS

# NOTE: in the json, 'true' as the value means that the shorter sma > longer
# sma. So '30:100': 'true day' means that sma30 > sma100 for that run during
# the day


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


def checkBools(ticker, old, new, avgTup, file):
    if file and old.split()[0] != new.split()[0] and not old.startswith('same'):
        if new.startswith('true'):
            switch = 'bullish'
        else:
            switch = 'bearish'

        message = f'{ticker} became {switch} on {avgTup[0]}, {avgTup[1]} interval.'

        if old.endswith('night'):
            message += ' However, this happened overnight.'

        print(message)  # make it actually send to the groupme here


def runAll(fileExists=True):
    with open('tickerSums.json') as f:
        sumData = json.load(f)

    if fileExists:
        with open('smaBools.json') as f:
            boolDict = json.load(f)
    else:
        boolDict = {}

    for tickerName in TICKER_NAMES:
        price = getPrice(tickerName)
        if not fileExists:
            boolDict[tickerName] = {}

        for tup in AVERAGE_LENGTHS:
            if fileExists:
                oldVal = boolDict[tickerName][f'{tup[0]}:{tup[1]}']
            else:
                oldVal = ''

            shortSMA = round((sumData[tickerName][str(tup[0])] + price) / tup[0], 2)
            longSMA = round((sumData[tickerName][str(tup[1])] + price) / tup[1], 2)

            if shortSMA > longSMA:
                checkBools(tickerName, oldVal, 'true', tup, fileExists)
                boolDict[tickerName][f'{tup[0]}:{tup[1]}'] = 'true'
            elif shortSMA < longSMA:
                checkBools(tickerName, oldVal, 'false', tup, fileExists)
                boolDict[tickerName][f'{tup[0]}:{tup[1]}'] = 'false'
            else:
                print('wow the two are exactly the same')  # also text groupme here
                boolDict[tickerName][f'{tup[0]}:{tup[1]}'] = 'same'

    with open('smaBools.json', 'w') as f:
        json.dump(boolDict, f, indent=2)


def main():
    runAll()

if __name__ == '__main__':
    main()

