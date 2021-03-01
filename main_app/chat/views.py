from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from main_app import socketio, db
from flask_socketio import emit
from main_app.models import User, Texts
from flask import jsonify
import json

chat = Blueprint('chat', __name__)

users = {}

@chat.route('/chat')
@login_required
def chat_view():
    contacts_l=[x.to_username for x in Texts.query.filter_by(from_username = current_user.username).all()]
    a = [x.from_username for x in Texts.query.filter_by(to_username = current_user.username).all()]
    contacts_l+=a
    contacts = list(set(contacts_l))
    return render_template('chat.html',contacts=contacts)


@socketio.on('connect',namespace='/private')
def connect_handle():
    if current_user.is_authenticated:
        emit('check',"connection successfull",room=request.sid)
        users[current_user.username] = request.sid
    else:return False

@chat.route('/username_ajax',methods=['POST'])
def username_ajax():
    username = request.form['username']
    print(username)
    if User.query.filter_by(username=username).first():
        return 'true'
    elif username == current_user.username: return 'false'
    else:
        return 'false'

@chat.route('/messages_ajax',methods=['POST'])
def messages_ajax():
    username = request.form['to_username']
    text_sent = Texts.query.filter_by(to_username = username, from_username=current_user.username).all()
    text_recieved = Texts.query.filter_by(to_username=current_user.username, from_username=username).all()
    text_sent = [(text_sent[i].text, 0, text_sent[i].time) for i in range(len(text_sent))]
    text_recieved = [(text_recieved[i].text, 1, text_recieved[i].time) for i in range(len(text_recieved))]
    texts = text_sent + text_recieved
    texts.sort(key=lambda x: x[2])
    for i in range(len(texts)):
        texts[i] = (texts[i][0],texts[i][1])
    if texts:
        return jsonify(texts=texts)
    else: return "false"

@socketio.on('private_message',namespace='/private')
def private_message(payload):
    message = payload['message']
    try:
        rescipient_session_id = users[payload['username']]
        emit('msg',{'message':message,'username':current_user.username},room=rescipient_session_id,json=True)
    except:
        pass
    finally:
        print(message, payload['username'])
        text = Texts(to_username=payload['username'], from_username=current_user.username, text=message)
        db.session.add(text)
        db.session.commit()
    
    



# @socketio.on('private_message',namespace='/private')
# def private_message()