# -*- coding: utf-8 -*-
# get the stock data from 163.com

import json
import re

import requests
from sqlalchemy import *
from sqlalchemy.orm import *


class Stock(object):
    def __init__(self, code, name, start_date='', location=''):
        self.code = code
        self.name = name
        self.start_date = start_date
        self.location = location

    def __str__(self):
        return self.code + "\t" + self.name + "\t" + self.location + "\t" + self.start_date

    def retrieve_start_date(self):
        r = requests.get('http://quotes.money.163.com/trade/lsjysj_' + self.code + '.html')
        pattern = re.compile('起始日期.*?<input.*?value="(.*?)".*?上市日', re.S)

        items = re.findall(pattern, r.text)
        self.start_date = items[0]

    def retrieve_start_date_and_location(self):
        r1 = requests.get('http://quotes.money.163.com/f10/gszl_' + self.code + '.html')
        pattern = re.compile('地域</td>.*?>(.*?)</td>.*?上市日期</td>.*?>(.*?)</td>', re.S)

        items = re.findall(pattern, r1.text)
        if items[0]:
            self.location = items[0][0]
            self.start_date = items[0][1]

    def __repr__(self):
        return '<Stock %s>' % self.code


def main():
    mysql_db = create_engine('mysql://root:123456@192.168.6.1:3306/stock',
                             connect_args={'charset': 'UTF8'},
                             convert_unicode=True,
                             encoding='UTF-8',
                             echo=True)
    metadata = MetaData()
    stock_dict_table = Table('stock_a', metadata,
                             Column('code', VARCHAR(10), unique=True, nullable=False, primary_key=True),
                             Column('name', VARCHAR(50), nullable=False),
                             Column('start_date', VARCHAR(10), nullable=False),
                             Column('location', VARCHAR(20), nullable=False)
                             )
    metadata.create_all(mysql_db)

    mapper(Stock, stock_dict_table)
    Session = sessionmaker(bind=mysql_db)
    session = Session()

    base_url = 'http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquoteds.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=SYMBOL%2CSNAME%2CCODE&sort=SYMBOL&order=asc&count=50000&type=query'
    r = requests.get(base_url)
    data_list = json.loads(r.text)["list"]

    size = len(data_list)
    count = 1
    for stock in data_list:
        stock = Stock(stock['SYMBOL'], stock['SNAME'])
        stock.retrieve_start_date_and_location()
        session.add(stock)
        print(count, "/", size, "->", stock)
        count += 1
    session.commit()

    query = session.query(Stock).filter(Stock.start_date == '--')
    data_list = list(query)
    size = len(data_list)
    count = 1
    for stock in data_list:
        print(stock)
        stock.retrieve_start_date()
        session.merge(stock)
        print(count, "/", size, "->", stock)
        count += 1
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
