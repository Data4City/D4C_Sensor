from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

__is_running__ = False


def start():
    global __is_running__
    if not __is_running__:
        app.run(host='0.0.0.0', use_reloader=False, debug=False)
        __is_running__ = True


@app.route("/")
def hello():
    return render_template('index.html')


def publish_message(channel, data={}):
    socketio.emit(channel, data)


if __name__ == "__main__":
    start()
