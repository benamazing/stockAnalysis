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

ff.write('代码,上市日期,股票名字,行业,地区,市盈率,总,总资产,每股盈利,涨跌幅超过5%的天数,总天数,开始价,结束价,涨跌幅%,换手率>5%的天数,平均换手率,最近10天换手率>5%,最近10天平均换手率' + '\r\n')
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
    histData = ts.get_hist_data(code, start='2016-08-01')
    if histData is None:
        ff.write(code + ',' + '0\r\n')
    else:
        openPrice = 1
        closePrice = 1
        try:
            openPrice = histData.open[-1]
            openDay = histData.index[-1]
        except Exception as e:
            pass
        try:
            closePrice = histData.close[0]
            closeDay = histData.index[0]
        except Exception as e:
            pass
        count = 0
        bigTurnoverCount = 0
        totalTurnover = 0.0
        avgTurnover = 0.0

        recent10DaysBigTurnoverCount = 0
        recent10DaysTotalTurnover = 0.0
        recent10DaysAvgTurnover = 0.0

        totalDays = len(histData)
        x = 0
        for d in histData.index:
            x += 1
            turnover = histData.ix[d]['turnover']
            totalTurnover += turnover
            if turnover >= 5:
                bigTurnoverCount += 1
            if x < 10:
                recent10DaysTotalTurnover += turnover
                if turnover >=5:
                    recent10DaysBigTurnoverCount += 1
        try:
            avgTurnover = totalTurnover / len(histData.turnover)
        except Exception as e:
            avgTurnover = 0.0

        try:
            if x >= 10:
                x = 10
            recent10DaysAvgTurnover = recent10DaysTotalTurnover / x
        except Exception as e:
            recent10DaysAvgTurnover = 0.0

        for change in histData.p_change:
            if abs(change) >= 5:
                count += 1
        ff.write(code + ',' + str(timeToMarket) + ',' + str(name) + ',' + str(industry) + ',' + str(area) + ',' + str(pe) + ',' + str(totals) + ',' + str(totalAssets) + ',' + str(esp) + ',' + str(count) + ',')
        ff.write(str(totalDays) + ',')
        ff.write(str(openDay) + ',')
        ff.write(str(closeDay) + ',')
        ff.write(str(openPrice) + ',')
        ff.write(str(closePrice) + ',')
        ff.write(str(closePrice/openPrice - 1) + ',')
        ff.write(str(bigTurnoverCount) + ',')
        ff.write(str(avgTurnover) + ',')
        ff.write(str(recent10DaysBigTurnoverCount) + ',')
        ff.write(str(recent10DaysAvgTurnover) + '\r\n')
    ind += 1
    print 'Finished process %d...' % ind

ff.close()
