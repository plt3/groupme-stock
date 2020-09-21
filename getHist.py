import yfinance as yf
import pytz
from datetime import datetime, timedelta

TICKER_NAME = 'SPY'

timezone = pytz.timezone('US/Eastern')
today = datetime.now(tz=timezone)
startFor100 = today - timedelta(days=170)

ticker = yf.Ticker(TICKER_NAME)
df = ticker.history(start=startFor100.strftime('%Y-%m-%d'),
                    end=today.strftime('%Y-%m-%d'), actions=False)

last29Sum = str(round(df.tail(29)['Close'].sum(), 2))
last99Sum = str(round(df.tail(99)['Close'].sum(), 2))

with open('29_99_day_sums.txt', 'w') as f:
    f.write(f'{last29Sum}\n{last99Sum}')

