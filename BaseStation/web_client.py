import websocket
from json import dumps
ws = websocket.WebSocket()
ws.connect("ws://192.168.1.128:8765")
msg = {"Header" : "Init",
        "Sender": "Base Station",
        "Message": "Hello Server from Base"}

ws.send(dumps(msg))
#msg["Header"] = "Msg"
#ws.send(msg)
while True:
    print(ws.recv())