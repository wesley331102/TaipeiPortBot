from flask import Flask, request
import json
import configparser
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import datetime
import time

config = configparser.ConfigParser()
config.read('./config.ini')

user_config = config['config']['user']
token_config = config['config']['token']
secret_config = config['config']['secret']
time_config = int(config['config']['time'])
port_config = int(config['config']['port'])

app = Flask(__name__)

@app.route("/")
def home():
    while True:
        time_now = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')
        msg = "none"
        if time_now == "07:18":
            msg = "現在時間早上 7 點 20 分，請各位同仁起床。"
        elif time_now == "07:28":
            msg = "現在時間早上 7 點 30 分，請各位同仁至一樓進行晨間環境打掃。"
        elif time_now == "07:58":
            msg = "現在時間早上 8 點整，請各位同仁至車庫發車，測試無線電。"
        elif time_now == "13:58":
            msg = "現在時間下午 2 點整，請各位同仁起床。"
        elif time_now == "14:28":
            msg = "現在時間下午 2 點 30 分，請各位同仁至一樓進行本日常訓。"
        if msg != "none":
            try:    
                access_token = token_config
                line_bot_api = LineBotApi(access_token)
                line_bot_api.push_message(user_config, TextSendMessage(text=''))
            except:
                print("===================================================================")
                print("Clock Error")
                print("-------------------------------------------------------------------")
                print(time_now)            
                print("===================================================================")
        time.sleep(time_config)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        access_token = token_config
        secret = secret_config
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        type = json_data['events'][0]['message']['type']
        if type == 'text':
            msg = json_data['events'][0]['message']['text']
            if validate_date(msg):
                print(str(datetime.date.fromisoformat(msg).month))
                print(str(datetime.date.fromisoformat(msg).day))
            elif msg == '班表':
                reply = '請輸入欲查詢的日期，格式為[YYYY-MM-DD]，範例如下：[2023-09-10]，請輸入[]內的關鍵字'
            else:
                reply = "目前僅提供以下服務，請輸入[]內的關鍵字以使用此服務~\n-[班表]"
        else:
            reply = "請輸入文字~"
            print("===================================================================")
            print("Format Error")
            print("-------------------------------------------------------------------")
        print(reply)
        print("===================================================================")
        line_bot_api.reply_message(tk,TextSendMessage(reply))
    except:
        print("===================================================================")
        print("Exception Error")
        print("-------------------------------------------------------------------")
        print(body)
        print("===================================================================")
    return 'OK'

def validate_date(date_text):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(port=port_config)