from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os, sqlite3
from CourseMonitor import (websiteParser, monitor, sender)


app = Flask(__name__)
dept = websiteParser.Department_list()
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

@app.route("/callback", methods=['POST'])
def callback():
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
	to = event.source.user_id
	try:
		#check if the message from user matches the format
		usr_DeptNo, usr_CrsNo = event.message.text.split()
		monitor.multithrd(to, usr_DeptNo, usr_CrsNo, dept)
	except ValueError:
		print("Format error!")
		text = "格式錯誤！\n系所和科目代碼間記得空格"
		sender.message_sender(to, text)
	except:
		print("System error!\n")
		text = "系統錯誤\n哇，GG"
		sender.message_sender(to, text)
		raise
		
   
if __name__ == "__main__":
    app.run(port=os.environ["PORT"])
	