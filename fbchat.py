from fbchat import Client, log, _graphql
from fbchat.models import *
import json
import random
import wolframalpha
import requests
import sqlite3
import os
import concurrent.futures
from difflib import SequenceMatcher, get_close_matches
# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
options = Options()
c = DesiredCapabilities.CHROME
c["pageLoadStrategy"] = "none"
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-sh-usage")



driver = webdriver.Chrome(
    service=Service(os.environ.get("CHROMEDRIVER_PATH")),
                    options=options, desired_capabilities=c)

class ChatBot(Client):

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            msg = str(message_object).split(",")[15][14:-1]
            if ("//video.xx.fbcdn" in msg):
                msg = msg
            else:
                msg = str(message_object).split(",")[19][20:-1]
        except:
            try:
                msg=(message_object.text).lower()
            except:
                pass

        def sendMsg():
            if (author_id != self.uid):
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        def sendQuery():
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        if(author_id == self.uid):
            pass
        else:
            try:
                conn=sqlite3.connect("messages.db")
                c=conn.cursor()
                c.execute("""
                CREATE TABLE IF NOT EXISTS "{}" (
                    mid text PRIMARY KEY,
                    message text NOT NULL
                );
                """.format(str(author_id).replace('"', '""')))

                c.execute("""
                INSERT INTO "{}" VALUES (?, ?)
                """.format(str(author_id).replace('"', '""')), (str(mid), msg))
                conn.commit()
                conn.close()
            except:
                pass


    def onMessageUnsent(self, mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):
        if(author_id == self.uid):
            pass
        else:
            try:
                conn=sqlite3.connect("messages.db")
                c=conn.cursor()
                c.execute("""
                SELECT * FROM "{}" WHERE mid = "{}"
                """.format(str(author_id).replace('"', '""'), mid.replace('"', '""')))

                fetched_msg=c.fetchall()
                conn.commit()
                conn.close()
                unsent_msg=fetched_msg[0][1]
                if("//video.xx.fbcdn" in unsent_msg):
                    reply = f"You just unsent a video"
                    self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                        file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                        file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                elif("//scontent.xx.fbc" in unsent_msg):
                    reply=f"You just unsent an image"
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                else:
                    reply=f"You just unsent a message:\n{unsent_msg} "
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
            except:
                pass
            
    def onReactionRemoved(self, mid=None, author_id=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="You just removed reaction from the message."
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

cookies = {
        "sb":"Yk6wYgsxeOS2Xg8omrhK-VqL",
        "fr":"0t4EwnIRMTTP2s7No.AWXEIhLtnysYP3wXleRpjHqQWsc.BkBVAi.SA.AAA.0.0.BkBVzm.AWXB5ctUb9c",
        "c_user":"100078119543134",
        "datr":"Yk6wYg_czopOZjuCXNc1Xr2E",
        "xs":"36%3AZwe1-wYVNjPCmw%3A2%3A1678150579%3A-1%3A3328"
       }


client=ChatBot("",
                "", session_cookies=cookies)
print(client.isLoggedIn())

try:
    client.listen()
except:
    time.sleep(3)
    client.listen()
