#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8

import datetime
import MySQLdb as mysql
import tushare as ts
import pandas as pd

db = mysql.connect(user="root", passwd="root", db="stock_db", charset="utf8")
#db.autocommit(True)
c = db.cursor()

def log(msg):
	now = datetime.datetime.now()
	nowString = now.strftime("%Y-%m-%d %H:%M:%S ")
	print nowString + msg


def downloadStockInfo():
    df = ts.get_stock_basics()
    print 'total stocks: %s ' % len(df)
    df.to_csv('stockList.csv')
    log('download csv finish')
    return df

''' Main process '''
log('Process Start...')
df = downloadStockInfo()

if df is None:
    exit()


sql1 = '''delete from stock_general_info'''
c.execute(sql1)

ind = 0
records = []
for i in df.index:
    code = str(i)
    name = df.name[i]
    industry = df.industry[i]
    area = df.area[i]
    pe = df.pe[i]
    outstanding = df.outstanding[i]
    totals = df.totals[i]
    totalAssets = df.totalAssets[i]
    liquidAssets = df.liquidAssets[i]
    fixedAssets = df.fixedAssets[i]
    reserved = df.reserved[i]
    reservedPerShare = df.reservedPerShare[i]
    esp = df.esp[i]
    bvps = df.bvps[i]
    pb = df.pb[i]
    timeToMarket = df.timeToMarket[i]
    record = [code, name, industry, area, pe, outstanding, totals, totalAssets, liquidAssets, fixedAssets, reserved, reservedPerShare, esp, bvps, pb, timeToMarket]
    records.append(record)
c.executemany('insert into stock_general_info values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', records)
db.commit()
log('save to DB finished.')
c.close()
db.close()
log('Process Finished....')
