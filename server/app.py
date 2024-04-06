from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_login import LoginManager
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = "99fe31bd7778fa2d79edb0e10d7d2644"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)

@socketio.on('message')
def handle_message(h):
    data = {
        'object': 'ball',
        'position': {'x': 100, 'y': 200},
        'velocity': {'x': 5, 'y': -2},
        'acceleration': {'x': 0, 'y': -9.8}
    }
    print(data)
    socketio.emit('message', json.dumps(data))

if __name__ == '__main__':
    socketio.run(app,debug=True,port=5000)