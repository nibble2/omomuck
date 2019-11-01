import pymysql

import config
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

host_name = config.DB_CONFIG['stores_host']
port_name = config.DB_CONFIG['stores_port']
user_name = config.DB_CONFIG['stores_user']
pwd = config.DB_CONFIG['stores_passwd']
db_name = config.DB_CONFIG['stores_db']
# database 에 접근
# database 를 사용하기 위한 cursor 를 세팅합니다.

@app.route('/')
def home():
    return render_template('index.html', map_key=config.API_KEY['kakao_map_api'])


@app.route('/list')
def myList():
    return render_template('mylist.html', map_key=config.API_KEY['kakao_map_api'])


@app.route('/search')
def foodSearch():
    return render_template('food-search.html', map_key=config.API_KEY['kakao_map_api'])


@app.route('/map', methods=['POST'])
def saving():
    author_receive = request.form['author_give']
    store_receive = request.form['store_give']  # 가게 명
    address_receive = request.form['address_give']  # 가게 주소
    tel_receive = request.form['tel_give']  # 가게 전화번호
    lat_receive = request.form['lat_give']  # 위도
    lng_receive = request.form['lng_give']  # 경도

    db = pymysql.connect(host=host_name,
                         port=port_name,
                         user=user_name,
                         passwd=pwd,
                         db=db_name,
                         charset='utf8')
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO stores(author, store, address, tel, lat, lng) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (author_receive, store_receive, address_receive, tel_receive, lat_receive, lng_receive))
            db.commit()
    except pymysql.err.IntegrityError:
        return jsonify({'result': 'fail', 'msg': '중복값 체크!'})
    finally:
        db.close()
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/map', methods=['GET'])
def listing():
    db = pymysql.connect(host=host_name,
                         port=port_name,
                         user=user_name,
                         passwd=pwd,
                         db=db_name,
                         charset='utf8')
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            # Create a new record
            sql = "SELECT * FROM stores"
            cursor.execute(sql)
            rows = cursor.fetchall()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
    finally:
        db.close()
        return jsonify({'result': 'success', 'rows': rows})


@app.route('/delete', methods=['POST'])
def deleting():
    store_give = request.args.get('store_give')
    # host ='my aws host ip'
    db = pymysql.connect(host=host_name,
                         port=port_name,
                         user=user_name,
                         passwd=pwd,
                         db=db_name,
                         charset='utf8')
    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM stores WHERE store = %s"
            cursor.execute(sql, store_give)
            db.commit()
        # connection is not autocommit by default. So you must commit to save
        # your changes.
    finally:
        db.close()
        return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
