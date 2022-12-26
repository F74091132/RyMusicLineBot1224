import os
import sys
import json

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message, send_text_message_AI

load_dotenv()

machine = TocMachine(
    states=[
        'initial',
        'input_search',
        'intro',
        'lists',
        'listen',
        'lyrics',
        'chat',
        'chat2',
    ],
    transitions=[
        #music mode
        {'trigger': 'advance', 'source': 'user', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {'trigger': 'advance', 'source': 'initial', 'dest': 'input_search', 'conditions': 'is_going_to_input_search'},
        {'trigger': 'advance', 'source': 'input_search', 'dest': 'intro', 'conditions': 'is_going_to_intro'},
        {'trigger': 'advance', 'source': 'input_search', 'dest': 'lists', 'conditions': 'is_going_to_lists'},
        {'trigger': 'advance', 'source': 'input_search', 'dest': 'listen', 'conditions': 'is_going_to_listen'},
        {'trigger': 'advance', 'source': 'intro', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {'trigger': 'advance', 'source': 'lists', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {'trigger': 'advance', 'source': 'listen', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        #{'trigger': 'advance', 'source': 'end', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        #chat mode
        {'trigger': 'advance', 'source': 'initial', 'dest': 'chat', 'conditions': 'is_going_to_chat'},
        {'trigger': 'advance', 'source': 'chat', 'dest': 'chat2', 'conditions': 'is_going_to_chat2'},
        {'trigger': 'advance', 'source': 'chat2', 'dest': 'chat2', 'conditions': 'is_going_to_chat2'},
        {'trigger': 'advance', 'source': 'chat2', 'dest': 'initial', 'conditions': 'is_going_to_chatEnd'},
        #
        {'trigger': 'advance', 'source': 'intro', 'dest': 'input_search', 'conditions': 'is_going_to_input_search'},
        #lyrics
        {'trigger': 'advance', 'source': 'initial', 'dest': 'lyrics', 'conditions': 'is_going_to_lyrics'},
        {'trigger': 'advance', 'source': 'lyrics', 'dest': 'initial', 'conditions': 'is_going_to_initial'},
        {
            'trigger': 'go_back',
            'source': [
                'initial',
                'input_search',
                'intro',
                'lists',
                'listen',
                'lyrics',
                'chat',
                'chat2',
            ],
            'dest': 'initial'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path='')


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

mode = 0
#mode_of_music = 0

@app.route('/callback', methods=['POST'])
def webhook_handler():
    global mode
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')

        response = machine.advance(event)
        #輸入錯誤的狀況
        if response == False:
            if machine.state != 'user' and event.message.text.lower() == 'restart':
                send_text_message(event.reply_token, '輸入『music』進入音樂模式；\n輸入『lyrics』進入歌詞總覽；\n隨時輸入『chat』跟bot聊天；\n隨時輸入『restart』從頭開始。')
                machine.go_back()
            #選項
            
    return 'OK'

"""
@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')
"""

if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
