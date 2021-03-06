from transitions.extensions import GraphMachine
from utils import send_text_message, send_image_message, send_mix_message

import random

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.tmp = None
    
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
        send_mix_message(reply_token, "請輸入隊伍代號查詢賽程\nex. B", 'https://i.imgur.com/94QHPjs.png')

    #team_choose
    def is_going_to_team_choose(self, event):
        text = event.message.text
        self.tmp = text 
        return text in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    def on_enter_team_choose(self, event):
        information = '11/07 ' + self.tmp + " 比賽時程如下: \n"
        sch7 = ['08:00 A-B / E 光低四','08:00 K-P / O 光低五', '08:00 L-M / I 光高東', 
                '09:00 C-D / B 光低四','09:00 N-O / K 光低五', '09:00 G-H / F 光高東', 
                '10:00 A-E / D 光低四','10:00 L-P / M 光低五', '10:00 I-J / H 光高東', 
                '14:00 K-O / L 光低四','14:00 M-P / N 光低五', '14:00 F-G / J 光高東', 
                '15:00 B-C / A 光低四','15:00 L-N / P 光低五', '15:00 H-I / G 光高東', 
                '16:00 D-E / C 光低四','16:00 M-O / L 光低五', '16:00 F-J / N 光高東']
        for word in sch7:
            for symbol in word:
                if self.tmp == symbol:
                    information = information + word + '\n'

        reply_token = event.reply_token
        send_text_message(reply_token, information[:-1])
        self.go_team_info()

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
                      複賽：11/14\n\
                      決賽：11/15\n\
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
        send_image_message(reply_token,'https://i.imgur.com/ExlNlEj.png')
        self.go_back()

    #meme
    def is_going_to_meme(self, event):
        text = event.message.text
        return text.lower() == "meme"
    def on_enter_meme(self, event):
        pick = random.randint(0,8)
        if pick==0:
            url = 'https://i.imgur.com/8WTPDr3.png'
        elif pick==1:
            url = 'https://i.imgur.com/cVUaO2w.jpg'
        elif pick==2:
            url = 'https://i.imgur.com/7XNk23T.png'
        elif pick==3:
            url = 'https://i.imgur.com/sON6KEx.png'
        elif pick==4:
            url = 'https://i.imgur.com/7Yom7qI.png'
        elif pick==5:
            url = 'https://i.imgur.com/hTOOBVD.png'
        elif pick==6:
            url = 'https://i.imgur.com/LsCkGNq.png'
        elif pick==7:
            url = 'https://i.imgur.com/WPukVvs.png'
        elif pick==8:
            url = 'https://i.imgur.com/PBcQAkD.png'
        reply_token = event.reply_token
        send_image_message(reply_token, url)
        self.go_back()

    #date
    def is_going_to_date_1107(self, event):
        text = event.message.text
        return text == "11/07"
    def on_enter_date_1107(self, event):
        reply_token = event.reply_token
        send_image_message(reply_token,'https://i.imgur.com/nxZWO5f.png')
        self.go_schedule()
    
    def is_going_to_date_1108(self, event):
        text = event.message.text
        return text == "11/08"
    def on_enter_date_1108(self, event):
        reply_token = event.reply_token
        send_image_message(reply_token,'https://i.imgur.com/ymN9iRr.png')
        self.go_schedule()
    
    def is_going_to_date_1114(self, event):
        text = event.message.text
        return text == "11/14"
    def on_enter_date_1114(self, event):
        reply_token = event.reply_token
        send_mix_message(reply_token, "複賽賽程尚未開始，初賽結束後將更新", 'https://i.imgur.com/E4wPZvc.png')
        self.go_schedule()
    
    def is_going_to_date_1115(self, event):
        text = event.message.text
        return text == "11/15"
    def on_enter_date_1115(self, event):
        reply_token = event.reply_token
        send_mix_message(reply_token, "決賽賽程尚未開始，複賽結束後將更新", 'https://i.imgur.com/cr9DkYV.png')
        self.go_schedule()