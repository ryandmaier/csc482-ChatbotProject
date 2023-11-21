import socket
import sys
import time

from chatbot import ChatBot
from statemachine import StateMachine

class IRC:
 
    irc = socket.socket()
  
    def __init__(self, channel, botnick):
        # Deefine the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel = channel
        self.botnick = botnick

    def command(self,msg):
        self.irc.send(bytes(msg + "\n", "UTF-8"))
 
    def send(self, msg):
        time.sleep(1)
        # Transfer data
        self.command("PRIVMSG " + self.channel + " :" + msg)
 
    def connect(self, server, port, botpass, botnickpass):
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.command("USER " + self.botnick + " " + self.botnick +" " + self.botnick + " :python")
        self.command("NICK " + self.botnick)
        #self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n", "UTF-8"))
        time.sleep(5)

        # join the channel
        self.command("JOIN " + self.channel)
 
    def get_response(self):
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode("UTF-8")
 
        if resp.find('PING') != -1:
           self.command('PONG ' + resp.split()[1]  + '\r') 
 
        return resp

import os
import random

## IRC Config
server = "irc.libera.chat" 	# Provide a valid server IP/Hostname
port = 6667
channel = "#CSC482"
if len(sys.argv) > 1:
    channel = f"#{sys.argv[1]}" # "#maierChatBot" # 
botnick = "maier-bot"
botnickpass = ""		# in case you have a registered nickname
botpass = ""			# in case you have a registered bot	

irc = IRC(channel=channel, botnick=botnick)
irc.connect(server, port, botpass, botnickpass)

my_bot = ChatBot(irc=irc)
stm = StateMachine(irc=irc, chatbot=my_bot)
while True:
    my_bot.recieve_message(stm)