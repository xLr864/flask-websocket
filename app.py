from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import emit
import json


app = Flask(__name__)
socketio = SocketIO(app)
# socketio.init_app(app, cors_allowed_origins="*")

@socketio.on("connect")
def ws_connect():
    try:
        f = open("data.txt",'r')
        data = f.read()
        _ = int(json.loads(data).get('counter'))+1
        temp = {"counter":_}
        f.close()
        emit('user',temp,broadcast=True)

        f = open("data.txt","w")
        f.write(json.dumps(temp))
        f.close()
        emit('user',temp,broadcast=True)

    except:
        f = open("data.txt","w")
        f.write(json.dumps({"counter":0}))
        f.close()
        emit('user',{"counter":0},broadcast=True)



@socketio.on("disconnect")
def ws_disconnect():
    try:
        f = open("data.txt",'r')
        data = f.read()
        _ = int(json.loads(data).get('counter'))-1
        temp = {"counter":_}
        f.close()
        emit('user',temp,broadcast=True)

        f = open("data.txt","w")
        f.write(json.dumps(temp))
        f.close()
        emit('user',temp,broadcast=True)

    except:
        f = open("data.txt","w")
        f.write(json.dumps({"counter":0}))
        f.close()
        emit('user',{"counter":0},broadcast=True)


@app.route('/',methods=["GET","POST"])
def hello_world():
    f = open('data.txt','r')
    data = f.read()
    data = {"counter":int(json.loads(data).get('counter'))}
    return render_template("index.html",data=data)

if __name__=="__main__":
    socketio.run(app,debug=True)