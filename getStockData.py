#!/usr/bin/env python
# -*- coding:utf-8 -*-
#encoding=utf-8

import tushare as ts
import pandas as pd
def downloadStockInfo():
    df = ts.get_stock_basics()
    print 'total stocks: %s ' % len(df)
    print 'Choose csv'
    df.to_csv('stockList.csv')
    print 'download csv finish'
    return df

df = downloadStockInfo()

ff = open('result2.csv', 'w')

ff.write('代码,timeToMarket,StockName,行业,地区,市盈率,总,总资产,每股盈利,涨跌幅超过5%的天数,开始价,结束价,涨跌幅%,换手率>5%,平均换手率' + '\r\n')
ind = 0
for i in df.index:
    code = str(i)
    name = df.ix[i]['name']
    industry = df.ix[i]['industry']
    area = df.ix[i]['area']
    pe = df.ix[i]['pe']
    totals = df.ix[i]['totals']
    totalAssets = df.ix[i]['totalAssets']
    esp = df.ix[i]['esp']
    timeToMarket = df.ix[i]['timeToMarket']
    histData = ts.get_hist_data(code, start='2016-06-01')
    if histData is None:
        ff.write(code + ',' + '0\r\n')
    else:
        openPrice = 1
        closePrice = 1
        try:
            openPrice = histData.open[-1]
        except Exception as e:
            pass
        try:
            closePrice = histData.close[0]
        except Exception as e:
            pass
        count = 0
        bigTurnoverCount = 0
        totalTurnover = 0.0
        avgTurnover = 0.0
        for turnover in histData.turnover:
            totalTurnover += turnover
            if turnover >= 5:
                bigTurnoverCount += 1
        try:
            avgTurnover = totalTurnover / len(histData.turnover)
        except Exception as e:
            avgTurnover = 0.0
        for change in histData.p_change:
            if abs(change) >= 5:
                count += 1
        ff.write(code + ',' + str(timeToMarket) + ',' + str(name) + ',' + str(industry) + ',' + str(area) + ',' + str(pe) + ',' + str(totals) + ',' + str(totalAssets) + ',' + str(esp) + ',' + str(count) + ',')
        ff.write(str(openPrice) + ',')
        ff.write(str(closePrice) + ',')
        ff.write(str(closePrice/openPrice - 1) + ',')
        ff.write(str(bigTurnoverCount) + ',')
        ff.write(str(avgTurnover) + '\r\n')
    ind += 1
    print 'Finished process %d...' % ind

ff.close()