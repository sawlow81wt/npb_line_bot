from flask import Flask, jsonify, request
import os
import json
import getGameScore

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)


LINE_ACCESS_TOKEN=os.getenv("LINE_ACCESS_TOKEN")
LINE_CHANNEL_SECRET=os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=['POST'])
def callbask():

    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.loger.info("Request body: {}".format(body))

    try:
        handler.handl(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'ok'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    favor_team = event.message.text
    data = getGameScore.get_today_score_list(favor_team)
    reply_message = "\n".join(data)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
