import os
import sys
# import numpy as np

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_message

load_dotenv()


machine = TocMachine(
    states=["start", "schedule", "team_info", "team_choose", "detail", "fsm", "meme", 
            "date_1107", "date_1108", "date_1114", "date_1115", "team_choose"],

    transitions=[
        # start-schedule
        {
            "trigger": "advance",
            "source": "start",
            "dest": "schedule",
            "conditions": "is_going_to_schedule",
        },
        # start-team_info
        {
            "trigger": "advance",
            "source": "start",
            "dest": "team_info",
            "conditions": "is_going_to_team_info",
        },
        # start-detail
        {
            "trigger": "advance",
            "source": "start",
            "dest": "detail",
            "conditions": "is_going_to_detail",
        },
        # start-fsm
        {
            "trigger": "advance",
            "source": "start",
            "dest": "fsm",
            "conditions": "is_going_to_fsm",
        },
        # start-meme
        { "trigger": "advance", "source": "start", "dest": "meme", "conditions": "is_going_to_meme",},
        #####

        #schedule
        { "trigger": "advance", "source": "schedule", "dest": "date_1107", "conditions": "is_going_to_date_1107",},
        { "trigger": "advance", "source": "schedule", "dest": "date_1108", "conditions": "is_going_to_date_1108",},
        { "trigger": "advance", "source": "schedule", "dest": "date_1114", "conditions": "is_going_to_date_1114",},
        { "trigger": "advance", "source": "schedule", "dest": "date_1115", "conditions": "is_going_to_date_1115",},

        #info
        { "trigger": "advance", "source": "team_info", "dest": "team_choose", "conditions": "is_going_to_team_choose",},
        #####
        
        # #team_info
        # { "trigger": "advance", "source": "team_info", "dest": "A", "conditions": "is_going_to_A",},
        # { "trigger": "advance", "source": "team_info", "dest": "B", "conditions": "is_going_to_B",},
        # { "trigger": "advance", "source": "team_info", "dest": "C", "conditions": "is_going_to_C",},
        # { "trigger": "advance", "source": "team_info", "dest": "D", "conditions": "is_going_to_D",},
        # { "trigger": "advance", "source": "team_info", "dest": "E", "conditions": "is_going_to_E",},
        # { "trigger": "advance", "source": "team_info", "dest": "F", "conditions": "is_going_to_F",},
        # { "trigger": "advance", "source": "team_info", "dest": "G", "conditions": "is_going_to_G",},
        # { "trigger": "advance", "source": "team_info", "dest": "H", "conditions": "is_going_to_H",},
        # { "trigger": "advance", "source": "team_info", "dest": "I", "conditions": "is_going_to_I",},
        # { "trigger": "advance", "source": "team_info", "dest": "J", "conditions": "is_going_to_J",},
        # { "trigger": "advance", "source": "team_info", "dest": "K", "conditions": "is_going_to_K",},
        # { "trigger": "advance", "source": "team_info", "dest": "L", "conditions": "is_going_to_L",},
        # { "trigger": "advance", "source": "team_info", "dest": "M", "conditions": "is_going_to_M",},
        # { "trigger": "advance", "source": "team_info", "dest": "N", "conditions": "is_going_to_N",},
        # { "trigger": "advance", "source": "team_info", "dest": "O", "conditions": "is_going_to_O",},
        # { "trigger": "advance", "source": "team_info", "dest": "P", "conditions": "is_going_to_P",},

        #back_forward
        { "trigger": "go_back", "source": ["schedule", "team_info", "team_choose", "detail", "fsm", "meme"], "dest": "start"},
        { "trigger": "go_team_info", "source": ["team_choose"], "dest": "team_info"},
        { "trigger": "go_schedule", "source": ["date_1107", "date_1108", "date_1114", "date_1115"], "dest": "schedule"},
        # { "trigger": "go_team_info", "source": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"], "dest": "team_info"},
    ],
    initial="start",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


# @app.route("/callback", methods=["POST"])
# def callback():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue

#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.message.text)
#         )

#     return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

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
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        response = machine.advance(event)
        if response == False:
            if machine.state != 'start' and event.message.text.lower() == 'restart':
                information = "歡迎使用女排聯賽機器人\n\
                               請輸入『賽程』、『隊伍資訊』、『活動詳情』獲得比賽相關資訊\n\
                               也可輸入『meme』讓你獲得快樂\n\
                               隨時輸入『restart』重新開始\n\
                               ----------------------\n\
                               輸入『fsm』獲得fsm\n".replace(" ", "")
                send_text_message(event.reply_token, information)      
                machine.go_back()
            elif machine.state == 'schedule':
                send_text_message(event.reply_token, "該天沒有賽程或是輸入錯誤，請重新輸入")    
            elif machine.state == 'team_info':
                send_text_message(event.reply_token, "沒有該參賽隊伍代號或是輸入錯誤，請重新輸入")    


    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)