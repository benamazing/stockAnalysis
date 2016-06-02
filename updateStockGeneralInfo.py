#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8

import MySQLdb as mysql
db = mysql.connect(user="root", passwd="root", db="stock_db", charset="utf8")
db.autocommit(True)
c = db.cursor()

import tushare as ts
import pandas as pd
def downloadStockInfo():
    df = ts.get_stock_basics()
    print 'total stocks: %s ' % len(df)
    df.to_csv('stockList.csv')
    print 'download csv finish'
    return df

df = downloadStockInfo()

if df is None:
    return


sql1 = '''delete from stock_general_info'''
c.execute(sql1)

ind = 0
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
    sql = '''insert into stock_general_info values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (code, name, industry, area, pe, outstanding, totals, totalAssets, liquidAssets, fixedAssets, reserved, reservedPerShare, esp, bvps, pb, timeToMarket)
    c.execute(sql)
print 'Finished update stock general inforamtion'
