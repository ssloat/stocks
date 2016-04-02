import urllib
import urllib3
import datetime

from mysite import db
from mysite.stocks.models import Stock, StockPrice

URL_BASE = 'https://www.google.com/finance/historical'

if __name__ == '__main__':
    today = datetime.date.today() 
    date = today - datetime.timedelta(days=15)

    http = urllib3.PoolManager()

    stocks = db.session.query(Stock).filter(Stock.ticker.in_(['SNI', 'POM', 'GMCR'])).all()
    for stock in stocks:

        data = {
            'q': stock.ticker,
            'format': 'csv',
            'output': 'csv',
            'startdate': date.strftime('%Y-%m-%d'),
            'enddate': today.strftime('%Y-%m-%d'),
        }

        url = '%s?%s' % (URL_BASE, urllib.urlencode(data))
        print url

        resp = http.urlopen('GET', url)
        lines = resp.data.splitlines()
        if len(lines) < 2:
            continue

        for line in lines[1:]:
            values = line.split(',')
            date = datetime.datetime.strptime(values[0], '%d-%b-%y').date()
            o, h, l, c, v = [None if s=='-' else float(s) for s in values[1:]]

            stock.add_price( date, o, h, l, c, v )

        db.session.commit()
