import os
import json
from transitions.extensions import GraphMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
from bs4 import BeautifulSoup
import requests
from linebot.models import *
import pandas as pd
from linebot import LineBotApi, WebhookParser, WebhookHandler
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
# global variable
age = 0
gender = ''
recommend = ''
search = ''
option = ''
songName = ''
height = 0
weight = 0
days = 0
part = ''

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start, 輸入 music
    def is_going_to_initial(self, event):
        return True
    #選擇要查詢的分類
    def on_enter_initial(self, event):
        send_text_message(event.reply_token, '輸入『music』進入音樂模式；\n輸入『rec』進入推薦模式；\n隨時輸入『chat』跟bot聊天；\n\n隨時輸入『restart』從頭開始。')
    # user start, 輸入 music
    def is_going_to_input_search(self, event):
        text = event.message.text
        return text.lower() == 'music'
    #選擇要查詢的分類
    def on_enter_input_search(self, event):
        title = '請選擇要查詢的項目'
        text = '.'
        btn = [
            MessageTemplateAction(
                label = '藝人介紹',
                text ='藝人介紹'
            ),
            MessageTemplateAction(
                label = '作品總表',
                text ='作品總表'
            ),
            MessageTemplateAction(
                label = '歌詞',
                text ='歌詞'
            ),
            MessageTemplateAction(
                label = '聽歌',
                text = '聽歌'
            ),
        ]
        url = 'https://upload.cc/i1/2022/12/18/ePnBsr.jpeg'
        send_button_message(event.reply_token, title, text, btn, url)
    #只要 is_going_to_intro return true, 則會自動進入到 on_enter_intro

    def is_going_to_intro(self, event):
        text = event.message.text
        if(text == '藝人介紹'):
                return True
        return False

    def on_enter_intro(self, event):
        message = [
            FlexSendMessage(
                'intro', 
                json.load(open('card.json', 'r', encoding='utf-8'))
            ),
            # 傳文字
            TextSendMessage(  
                text = "輸入任意字回到起始"
            ),]
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_lists(self, event):
        text = event.message.text
        if(text == '作品總表'):
                return True
        return False

    def on_enter_lists(self, event):
        message = [
            #傳圖片
            ImageSendMessage( 
                original_content_url = "https://upload.cc/i1/2022/12/18/AflYSF.png",
                preview_image_url = "https://upload.cc/i1/2022/12/18/AflYSF.png"
            ),
            # 傳文字
            TextSendMessage(  
                text = "輸入任意字回到起始"
            ),]
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_lyrics(self, event):
        text = event.message.text
        if(text == '歌詞'):
                return True
        return False

    def on_enter_lyrics(self, event):
        message = [
            # 傳文字
            TextSendMessage(  
                text = "https://mojim.com/twh242206.htm"
            ),
            TextSendMessage(  
                text = "輸入任意字回到起始"
            ),]
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_age(self, event):
        text = event.message.text
        if(text == 'rec'):
                return True
        return False

    def on_enter_age(self, event):
        message = [
            # 傳文字
            TextSendMessage(  
                text = "推薦模式\n請輸入您的年齡（整數）"
            ),]
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_gender(self, event):
        global age
        text = event.message.text

        if text.lower().isnumeric():
            age = int(text)
            return True
        return False

    def on_enter_gender(self, event):
        title = '選擇您的性別'
        text = '您是『男生』還是『女生』'
        btn = [
            MessageTemplateAction(
                label = '男生',
                text ='男生'
            ),
            MessageTemplateAction(
                label = '女生',
                text = '女生'
            ),
        ]
        url = 'https://i.imgur.com/T2bLdbN.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_recommendFinal(self, event):
        global gender
        text = event.message.text

        if text == '男生':
            gender = '男生'
            return True
        elif text == '女生':
            gender = '女生'
            return True
        return False

    def on_enter_recommendFinal(self, event):
        global age, gender, recommend
        if gender == '男生':
            if age < 30:
                recommend = '推薦歌曲：旦保\nhttps://www.youtube.com/watch?v=3m2kF0DPjZU\n輸入任意字回到起始'
            if age >= 30:
                recommend = '推薦歌曲：讓你倚靠的力量\nhttps://www.youtube.com/watch?v=7uRSWzbK0Jo\n輸入任意字回到起始'
        elif gender == '女生':
            if age < 50:
                recommend = '推薦歌曲：堯平\nhttps://www.youtube.com/watch?v=XnPQEiAIhUA\n輸入任意字回到起始'
            if age >= 50:
                recommend = '推薦歌曲：阿公阿嬤的芭樂\nhttps://www.youtube.com/watch?v=pMU8Yr388d4\n輸入任意字回到起始'

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = recommend))

    def is_going_to_listen(self, event):
        text = event.message.text
        if(text == '聽歌'):
                return True
        return False

    def is_going_to_end(self, event):
        text = event.message.text
        if(text == 'restart'):
                return False
        return True
    def on_enter_end(self, event):
        send_text_message(event.reply_token, '請輸入restart')

    def on_enter_listen(self, event):
        message = [
            FlexSendMessage( 
                'listen', 
                json.load(open('song.json', 'r', encoding='utf-8'))
            ),
            # 傳文字
            TextSendMessage(  
                text = "輸入任意字回到起始"
            ),]
        line_bot_api.reply_message(event.reply_token, message)
    #
    #
    def is_going_to_chat(self, event):
        text = event.message.text
        if(text == 'chat'):
                return True
        return False

    def on_enter_chat(self, event):
        send_text_message(event.reply_token, '進入聊天模式')

    # chat mode
    def is_going_to_chat2(self, event):
        text = event.message.text
        if(text == 'restart'):
                return False
        return True

    def on_enter_chat2(self, event):
        message = event.message.text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = message))
    #chat end
    def is_going_to_chatEnd(self, event):
        text = event.message.text
        if(text == 'restart'):
                return True
        return False
    def on_enter_chatEnd(self, event):
        send_text_message(event.reply_token, '重新開始')
