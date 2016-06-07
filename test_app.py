# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from pymongo import MongoClient


def connect():
    connection = MongoClient("127.0.0.1", 27017)
    handle = connection["test_db"]
    return handle


app = Flask(__name__)
handle = connect()



@app.route('/', methods=['GET'])
def index():
    pipe = [{'$sort':{"pop": -1}}, {'$limit':100}]
    top_pop_cities = [x for x in handle.cities.aggregate(pipeline=pipe)]
    
    lst = []
    cities = []

    for item in top_pop_cities:
        if len(lst) < 20:
            if not cities or item.get('city') not in cities:
                cities.append(item.get('city'))
                lst.append(item)
    top_pop_cities = lst

        

    return render_template('index.html', top_pop_cities=top_pop_cities)



if __name__ == '__main__':
    app.run(debug=True)