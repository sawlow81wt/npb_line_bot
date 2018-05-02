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


LINE_ACCESS_TOKEN=os.environ["LINE_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET=os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/test/", methods=['GET'])
def ok():
    return "ok!!?"

@app.route("/callback", methods=['POST'])
def callback():
    print(request.data)
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_msg = "\n".join(getGameScore.get_today_score_list(text))
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_msg))

if __name__ == "__main__":
    app.run(ssl_context='adhoc')
