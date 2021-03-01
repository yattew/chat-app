from main_app import socketio, app
local_net = True
if __name__ == "__main__":
    if local_net:
        socketio.run(app, debug=False,host = '192.168.1.4')
    else:
        socketio.run(app, debug=True)