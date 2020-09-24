import pytz
import json
import yfinance as yf
from datetime import datetime, timedelta
from tickerNames import TICKER_NAMES, AVERAGE_LENGTHS


def getTwoSums(ticker, averages):

    ''' 
    return dictionary where each key is a number from averages variable and
    value is the sum of the ticker's close prices for the last number - 1 days
    '''

    timezone = pytz.timezone('US/Eastern')
    today = datetime.now(tz=timezone)
    longestAvg = max([max(tup) for tup in averages])
    getAtLeastNDays = 1.7  # since stock market is only open Monday-Friday
    longStart = today - timedelta(days=longestAvg * getAtLeastNDays)

    tickerObj = yf.Ticker(ticker)
    df = tickerObj.history(start=longStart.strftime('%Y-%m-%d'),
                           end=today.strftime('%Y-%m-%d'), actions=False)

    sumDict = {}

    for shortAvg, longAvg in averages:
        shortSum = round(df.tail(shortAvg - 1)['Close'].sum(), 2)
        longSum = round(df.tail(longAvg - 1)['Close'].sum(), 2)

        sumDict[shortAvg] = shortSum
        sumDict[longAvg] = longSum

    return sumDict


def main():
    tickerSumDict = {name: getTwoSums(name, AVERAGE_LENGTHS) for name in
                     TICKER_NAMES}

    with open('tickerSums.json', 'w') as f:
        json.dump(tickerSumDict, f, indent=2)


if __name__ == '__main__':
    main()
