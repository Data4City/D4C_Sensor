from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

__is_running__ = False

def start():
    if not __is_running__:
        socketio.run(app, host='0.0.0.0')

@app.route("/")
def hello():
        return render_template('Helpers/FlaskHelpers/index.html')

def publish_message(channel, data = {}):
        socketio.emit(channel, data)
