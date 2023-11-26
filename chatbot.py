
import sys
import random
import time

class ChatBot:
    
    def __init__(self, irc):
        self.irc = irc
                
    def get_message_text(self, message):
        print("Full msg:",message)
        # Split by newline incase multiple messages come through as one
        # return first message that matches f"PRIVMSG {self.irc.channel} :{self.irc.botnick}:"
        messages = message.split('\n')
        for msg in messages:
            # Split to isolate message itself from the full text
            split = msg.split(f"PRIVMSG {self.irc.channel} :{self.irc.botnick}:")
            sender = msg.split("!")[0][1:].replace('@','')
            if len(split) > 1:
                return {'text': split[1].strip().lower(), 'sender': sender}
        # returns None if split doesn't work (not PRIVMSG, or different channel, or bot name not at message start)
        
    def _get_users(self):
        split = []
        while len(split) < 2:
            self.irc.command(f"NAMES {self.irc.channel}")
            message = self.irc.get_response()
            if '\n' in message:
                message = [ m for m in message.split('\n') if '353' in m ][0]
            print(f"Users message: {message}")
            if '353' in message:
                split_by = f"{self.irc.botnick} @ {self.irc.channel} :" # f"{self.irc.channel} :{self.irc.botnick}"
                print(f"splitting by {split_by}")
                split = message.split(split_by)
        return split[1].replace('\r','').replace('@','').strip()
        
    def users(self):
        self.irc.send(self._get_users())
        return
    
    def usage(self, sender):
        line1 = f"{sender}: I am bot {self.irc.botnick}, created by Ryan Maier and Bret Craig for CSC 482-03."
        print(line1)
        self.irc.send(line1)
        # TODO: line 2 explain what special abilities the bot has...
        return
    
    def forget(self):
        self.irc.send("Forgetting everything...")
        return "forget"
    
    #########################
    # Main response handler #
    #########################

    def recieve_message(self, stm):
        message = self.irc.get_response()
        info = self.get_message_text(message)
        if info is None:
            return None
        
        text = info['text']
        print(f"sender: {info['sender']}")
        
        print("Chatbot recieved message:",text)
        
        if (("hello" in text) or ("hi" in text) or ("hey" in text)) and stm.state == 'END':
            stm.OUTREACH_REPLY_2(sender=info['sender'])

        elif "die" in text:
            self.irc.send("you may take my life but you'll never take my freedom")
            self.irc.command("QUIT")
            sys.exit()
            
        elif "users" in text:
            self.users()
            return None
            
        elif ("usage" in text) or ("who are you?" in text):
            self.usage(info['sender'])
            return None
            
        elif text == "forget":
            # return message so stm knows to transition to END and return
            return self.forget()
        
        else:
            return info