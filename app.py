from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/socket')
def socket():
    return render_template('socket.html')

if __name__ == '__main__':
    app.run()
