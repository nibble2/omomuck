import config
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('map.html', map_key=config.API_KEY['kakao_map_api'])


@app.route('/map', methods=['POST'])
def saving():
    user_receive = request.form['user_give'] # 이름(pk)
    address_receive = request.form['address_give'] # 가게 주소
    phone_receive = request.form['phone_give'] # 가게 전화번호
    lat_receive = request.form['lat_give'] # 위도
    lng_receive = request.form['lng_give'] # 경도
    name_receive = request.form['name_give'] # 가게 명

    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/map', methods=['GET'])
def listing():
    name_receive = request.args.get('name_give')
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
