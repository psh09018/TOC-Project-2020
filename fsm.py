from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    #schedule
    def is_going_to_schedule(self, event):
        text = event.message.text
        return text == "賽程"
    def on_enter_schedule(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入欲查詢賽程之日期：\n11/07\n11/08\n11/14\n11/15")

    #team_info
    def is_going_to_team_info(self, event):
        text = event.message.text
        return text == "隊伍資訊"
    def on_enter_team_info(self, event):
        reply_token = event.reply_token
        send_image_message(reply_token, 'https://i.imgur.com/T2bLdbN.jpg')
        send_text_message(reply_token, "可輸入隊伍代號查詢選手名單")
        self.go_back()

    #detail
    def is_going_to_detail(self, event):
        text = event.message.text
        return text == "活動詳情"
    def on_enter_detail(self, event):
        reply_token = event.reply_token
        infomation = "---活動名稱---\n\
                      第五屆成功大學女子排球聯賽\n\
                      ---活動宗旨---\n\
                      促進排球風氣，並增進系隊情誼\n\
                      ---活動時間---\n\
                      中華民國109年\n\
                      預賽：11/07,08\n\
                      複賽：11/15\n\
                      決賽：11/16\n\
                      雨備：11/22,23\n\
                      ---活動地點---\n\
                      光復校區排球場\n\
                      ---主辦單位---\n\
                      成功大學資訊工程學系女排\n".replace(" ", "")
        send_text_message(reply_token, infomation)
        self.go_back()

    #fsm
    def is_going_to_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"
    def on_enter_fsm(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "fsm")
        self.go_back()

    #meme
    def is_going_to_meme(self, event):
        text = event.message.text
        return text.lower() == "meme"
    def on_enter_meme(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "meme")
        self.go_back()

    # #go back to start
    # def is_going_to_start(self, event):
    #     text = event.message.text
    #     if text.lower() == "restart":
    #         self.go_back()
    #     # return text.lower() == "restart"

    # def on_enter_start(self, event):
    #     reply_token = event.reply_token
    #     send_text_message(reply_token, "go back to start condition")
    #     self.go_back()

    #date
    def is_going_to_date_1107(self, event):
        text = event.message.text
        return text == "11/07"
    def on_enter_date_1107(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "11/07")
        self.go_schedule()
    
    def is_going_to_date_1108(self, event):
        text = event.message.text
        return text == "11/08"
    def on_enter_date_1108(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "11/08")
        self.go_schedule()
    
    def is_going_to_date_1114(self, event):
        text = event.message.text
        return text == "11/14"
    def on_enter_date_1114(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "11/14")
        self.go_schedule()
    
    def is_going_to_date_1115(self, event):
        text = event.message.text
        return text == "11/15"
    def on_enter_date_1115(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "11/15")
        self.go_schedule()
    
    


