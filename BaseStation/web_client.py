import websocket
from json import dumps, loads
ws = websocket.WebSocket()
ws.connect("ws://192.168.1.128:8765")
msg = {"Header" : "Init",
        "Sender": "Base Station",
        "Recipient": "Robot",
        "Message": "Hello Server from Base"}

ws.send(dumps(msg))
msg["Header"] = "Cannon"
'''msg["Message"] = "Client Started"
ws.send(dumps(msg))'''
msg["Message"] = "Cannon 1"
while True:
    inpt = loads(ws.recv())
    print(inpt["Message"])
    ws.send(dumps(msg))