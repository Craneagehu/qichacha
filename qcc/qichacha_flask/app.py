#-*- coding:utf-8 -*-
from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer

from qichacha import qcc


app = Flask(__name__)


@app.route('/api/qichacha',methods=['GET','POST'])
def qichacha():
    if request.method =='GET':
        company = request.args.get('company')
        result = qcc(company)
        data = jsonify(result)
    return data


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    WSGIServer(('0.0.0.0', 5000), app).serve_forever()
