import urllib
import urllib3
import datetime
import sys
import re

from mysite import db
from mysite.stocks.models import Stock, StockPrice

URL_BASE = 'http://real-chart.finance.yahoo.com/table.csv'

if __name__ == '__main__':

    stock = Stock(sys.argv[1], sys.argv[1], '', sys.argv[1], sys.argv[2], sys.argv[3])
    db.session.add(stock)
    db.session.commit()

    end = datetime.date.today() 
    start = datetime.date(1980, 1, 1)

    http = urllib3.PoolManager()

    args = [
        's=%s' % (stock.ticker),
        'a=%d' % (start.month-1), 'b=%d' % (start.day), 'c=%d' % (start.year),
        'd=%d' % (end.month-1), 'e=%d' % (end.day), 'f=%d' % (end.year),
    ]

    url = '%s?%s' % (URL_BASE, '&'.join(args))
    print url
    lines = urllib.urlopen(url).read().splitlines()
 
    if [x for x in lines if re.search('404 Not Found', x)]:
        print "Not found: %s: %s - %s" % (asset.ticker, start, end)
    else:

        if stock.ticker == 'LMBMX':
            lines.append('2016-05-19,11.43,11.43,11.43,11.43,')

        for line in lines[1:]:
            data = line.split(',')
            date = datetime.date(*map(int, data[0].split('-')))
            o, h, l, c, v, adj_close = [None if s=='-' else float(s) for s in data[1:]]

            stock.add_price( date, o, h, l, c, v )

    args.append('g=v')
    url = '%s?%s' % (URL_BASE, '&'.join(args))
    print url
    lines = urllib.urlopen(url).read().splitlines()
 
    if [x for x in lines if re.search('404 Not Found', x)]:
        print "Not found: %s: %s - %s" % (asset.ticker, start, end)

    else:
        for line in lines[1:]:
            data = line.split(',')
            date = datetime.date(*map(int, data[0].split('-')))
            dividend = float(data[1])

            stock.add_dividend('Income', dividend, date, date, date, date)

    db.session.commit()
