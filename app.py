from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('map.html')


@app.route('/map', methods=['POST'])
def saving():
    user_receive = request.form['user_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']
    lat_receive = request.form['lat_give']
    lng_receive = request.form['lng_give']
    name_receive = request.form['name_give']

    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/map', methods=['GET'])
def listing():
    name_receive = request.args.get('name_give')
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
