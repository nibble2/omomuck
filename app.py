import pymysql

import config
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# database 에 접근
# database 를 사용하기 위한 cursor 를 세팅합니다.


@app.route('/')
def home():
    return render_template('map.html', map_key=config.API_KEY['kakao_map_api'])


@app.route('/list')
def myList():
    return render_template('mylist.html', map_key=config.API_KEY['kakao_map_api'])


@app.route('/map', methods=['POST'])
def saving():
    author_receive = request.form['author_give']
    store_receive = request.form['store_give']  # 가게 명
    address_receive = request.form['address_give']  # 가게 주소
    tel_receive = request.form['tel_give']  # 가게 전화번호
    lat_receive = request.form['lat_give']  # 위도
    lng_receive = request.form['lng_give']  # 경도
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='1234',
                         db='omomuck',
                         charset='utf8')
    try:
        with db.cursor() as cursor:
            # Create a new record
            sql = "INSERT IGNORE INTO mylist(author, store, address, tel, lat, lng) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (author_receive, store_receive, address_receive, tel_receive, lat_receive, lng_receive))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db.commit()
        print(cursor.lastrowid)
    finally:
        db.close()
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/map', methods=['GET'])
def listing():
    name_give = request.args.get('name_give')
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='1234',
                         db='omomuck',
                         charset='utf8')
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            # Create a new record
            sql = "SELECT * FROM mylist"
            cursor.execute(sql)
            rows = cursor.fetchall()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
    finally:
        db.close()
        return jsonify({'result': 'success', 'rows': rows})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
