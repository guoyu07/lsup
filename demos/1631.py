# -*- coding: utf-8 -*-

import csv
from io import StringIO

import requests

url = 'http://quotes.money.163.com/service/chddata.html?code=1000001&start=19910102&end=20160705&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
r = requests.get(url)
dataFile = StringIO(r.text)
csvReader = csv.reader(dataFile)
# 日期,股票代码,名称,收盘价,最高价,最低价,开盘价,前收盘,涨跌额,涨跌幅,换手率,成交量,成交金额,总市值,流通市值
# 2016-07-05,'000001,平安银行,8.81,8.83,8.77,8.8,8.81,0.0,0.0,0.2885,42203729,371422814.75,1.51271324134e+11,1.28900854151e+11
# TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
for date, code, name, close, high, low, open, lclose, chg, pchg, turnover, voturnover, vaturnover, tcap, mcap in csvReader:
    print(date)
    print(code)
    print(tcap)
