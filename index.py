from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from chatgpt import ChatGPT  # 修正引用方式
import os

# 環境變數讀取
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFAULT_TALKING", "true").lower() == "true"  # 修正拼寫
app = Flask(__name__)
chatgpt = ChatGPT()

# 測試路由
@app.route('/')
def home():
    return 'Hello, World!'

# LINE Webhook 路由
@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        return abort(400)  # 回應 400 錯誤碼
    return 'OK', 200  # 明確回應 200，避免 LINE 認為 Webhook 無效

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status

    if event.message.type != "text":
        return

    if working_status:
        chatgpt.add_msg(f"Human:{event.message.text}\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg)
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
