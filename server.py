from flask import Flask, request, jsonify

from main import process1, process2


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome'})


@app.route('/process1', methods = ['POST'])
def proc1():
    temp1 = request.get_json()
    ret1 = process1(temp1)
    res = jsonify(ret1)
    return res


@app.route('/process2', methods = ['POST'])
def proc2():
    temp2 = request.get_json()
    ret2 = process2(temp2)
    res = jsonify(ret2)
    return res

if __name__ == '__main__':
    app.run(port=5000, debug=True)