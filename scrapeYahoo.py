import json
import requests
from tickerNames import TICKER_NAMES, AVERAGE_LENGTHS
from utils import getPrice, sendGroupMe

# NOTE: in the json, 'true' as the value means that the shorter SMA > longer
# SMA. So '30:100': 'true' means that SMA30 > SMA100 for that run during
# the day


def checkBools(ticker, old, new, avgTup, file):
    
    '''
    Send GroupMe message only if greater SMA has changed compared to last time.
    if file=False, don't do anything bc that's only if it is the first run ever
    '''

    if file and old.split()[0] != new.split()[0] and not old.startswith('same'):
        if new.startswith('true'):
            switch = 'bullish'
        else:
            switch = 'bearish'

        message = f'{ticker} became {switch} on {avgTup[0]}, {avgTup[1]} interval.'

        if old.endswith('night'):
            message += ' However, this happened overnight.'

        sendGroupMe(message)


def runAll(fileExists=True):
    
    '''
    Iterate through all tickers and intervals, calculate SMAs and send GroupMe
    message if the greater SMA changes. fileExists=False is if it is the first
    run ever.
    '''

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
                message = (f'{ticker} averages are exactly equal  on '
                            '{avgTup[0]}, {avgTup[1]} interval.')
                sendGroupMe(message)
                boolDict[tickerName][f'{tup[0]}:{tup[1]}'] = 'same'

    with open('smaBools.json', 'w') as f:
        json.dump(boolDict, f, indent=2)


def main():
    runAll()


if __name__ == '__main__':
    main()

