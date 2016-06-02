#!/usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8

import MySQLdb as mysql
import json
from flask import Flask, request, render_template
app = Flask(__name__)
db = mysql.connect(user="root", passwd="root", db="stock_db", charset="utf8")
db.autocommit(True)
c = db.cursor()


@app.route("/", methods=["GET"])
def home():
    return render_template("stocklist.html")

@app.route("/stocklist", methods=["GET"])
def getProducts():
    c.execute("select * from stock_general_info order by code")
    ones = []
    for i in c.fetchall():
      stock = {}
      stock['code'] = i[0]
      stock['name'] = i[1]
      stock['industry'] = i[2]
      stock['area'] = i[3]
      ones.append(stock)
    data = {}
    data['data'] = ones
    return json.dumps(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
