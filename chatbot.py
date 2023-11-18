
import sys
import random

class ChatBot:
    
    def __init__(self, irc):
        self.irc = irc
        
    def get_message_text(self, msg):
        print("Full msg:",msg)
        # Split to isolate message itself from the full text
        split = msg.split(f"PRIVMSG {self.irc.channel} :{self.irc.botnick}:")
        sender = msg.split("!")[0][1:]
        if len(split) > 1:
            return {'text': split[1].strip().lower(), 'sender': sender}
        # returns None if split doesn't work (not PRIVMSG, or different channel, or bot name not at message start)
        
    def hello(self, stm):
        # if stm.state == 'END'
        resps = ["Hello World!", "hello there", "what's up", "hey buddy", "hey", "hii :)"]
        self.irc.send(random.choice(resps))
        
    def _get_users(self):
        self.irc.command(f"NAMES {self.irc.channel}")
        message = self.irc.get_response()
        print(f"Users message: {message}")
        return message.split("\n")[0].split(f"{self.irc.channel} :{self.irc.botnick}")[1]
        
    def users(self):
        self.irc.send(self._get_users())
        return
    
    def usage(self, sender):
        line1 = f"{sender}: I am bot {self.irc.botnick}, created by Ryan Maier for CSC 482-03."
        print(line1)
        self.irc.send(line1)
        # TODO: line 2 explain what special abilities the bot has...
        return
    
    def forget(self):
        # TODO: Chatbot must forget all it knows...
        return
    
    def initiate_greeting(self, stm):
        user = random.choice(self._get_users().split(' '))
        greeting = random.choice(['hello', 'hi', 'hey'])
        self.irc.send(f"{user}: {greeting}")
        stm.state = 'START'
        stm.speaker = 1
        stm.transition()
    
    #########################
    # Main response handler #
    #########################

    def recieve_message(self, stm):
        message = self.irc.get_response()
        info = self.get_message_text(message)
        if info is None:
            return
        text = info['text']
        print(f"sender: {info['sender']}")
        
        print("Chatbot recieved message:",text)
        
        if ("hello" in text) or ("hi" in text) or ("hey" in text):
            return self.hello(stm)

        if "die" in text:
            self.irc.send("you may take my life but you'll never take my freedom")
            self.irc.command("QUIT")
            sys.exit()
            
        if "users" in text:
            self.users()
            
        if ("usage" in text) or ("who are you?" in text):
            self.usage(info['sender'])
            
        if "forget" in text:
            self.forget()