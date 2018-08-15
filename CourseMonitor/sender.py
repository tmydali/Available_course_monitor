import os
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot import LineBotApi


line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])

def message_sender(to, text):
	line_bot_api.push_message(
			to, 
			TextSendMessage(text))