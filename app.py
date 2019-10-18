from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'this is home'

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)