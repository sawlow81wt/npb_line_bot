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


LINE_ACCESS_TOKEN=os.getenv("LINE_ACCESS_TOKEN", "not_a_find")
LINE_CHANNEL_SECRET=os.getenv("LINE_CHANNEL_SECRET", "not_a_find")

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/test/", methods=['GET'])
def ok():
    return "ok!!"

@app.route("/callback", methods=['POST'])
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
    app.run(ssl_context='adhoc', debug=True)
