from datetime import datetime
import json
from flask import Flask, request
import pandas as pd
from pymongo import *

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.ebaydata
ebayCol = db.ebay

months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


@app.post('/data')
def saveData():
    print('SAVING DATA')
    data = request.get_data(as_text=True)
    elementArray = json.loads(data)
    for element in elementArray:
        for key, value in element.items():
            if(key == 'date'):
                month = value[0:3]
                day = value[4:5]
                year = value[7:]
                monthInt = months[month]
                element[key] = datetime(int(year), int(monthInt), int(day))

    for object in elementArray:
        found = ebayCol.find_one(object)
        if(found == None):
            ebayCol.insert_one(object)
    print('DATA SAVED')
    return 'Data saved'

@app.get('/data')
def getData():
    print('GETTING DATA') 
    params = request.args
    print(params)
    query = {}
    for key, value in params.items():
        if(key != 'price' or key != 'date'):
            query.update({key: {'$regex': value}})
            continue
        query.update({key: {'$gte': float(value)}})

    data = ebayCol.find(query)
    objcts: dict = {}
    elements = [{}]
    previousDate = None

    volume = 0
    open = 0
    close = 0
    high = 0
    low = 0

    for element in data:
        element.pop('_id')
        objcts.update({'date': element['date'], 'data': {}})

        currentDate = element['date']
        if (previousDate == None):
            previousDate = currentDate
        elif (previousDate != currentDate):
            objcts.update({'date': previousDate, 'data': {'volume': volume,
             'open': open, 'close': close, 'high': high, 'low': low}})
            previousDate = currentDate
        else:
            volume += 1
            if (element['price'] > high):
                high = element['price']
            if (element['price'] < low):
                low = element['price']
            close = element['price']
            objcts.update({'date': element['date'], 'data': {'volume': volume,
             'open': open, 'close': close, 'high': high, 'low': low}})
    return json.dumps(objcts)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    print('Starting app')
    app.run(debug=True, port=5000)

