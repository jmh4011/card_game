import base64
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_login import LoginManager
import json
from module import Database
db = Database()


app = Flask(__name__)
app.config['SECRET_KEY'] = "99fe31bd7778fa2d79edb0e10d7d2644"
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)

@socketio.on('message')
def handle_message(data):
    print(data)
    socketio.emit('message', "hello")

@socketio.on('login')
def handle_message(data):
    print(data)
    socketio.emit('login', db.login(userid= data['userid'], password= data['password']))

@socketio.on('create_account')
def handle_message(data):
    print(data)
    socketio.emit('create_account', db.create_account(userid= data['userid'], password=data['password']))
    
@socketio.on('card')
def handle_request_card(id):
    card = db.card_info(id)
    image_path = f'./data/images/{card['image']}'
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            card['image'] = encoded_string
            socketio.emit('card', json.dumps(card))
    except FileNotFoundError:
        socketio.emit('card', 'error')
    
    

if __name__ == '__main__':
    socketio.run(app,debug=True,port=5000)