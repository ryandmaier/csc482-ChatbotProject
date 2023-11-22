
import sys
import random
import time

class ChatBot:
    
    def __init__(self, irc):
        self.irc = irc
        self.start_convo_waiter = time.time()
        
    def get_message_text(self, msg):
        print("Full msg:",msg)
        # Split to isolate message itself from the full text
        split = msg.split(f"PRIVMSG {self.irc.channel} :{self.irc.botnick}:")
        sender = msg.split("!")[0][1:].replace('@','')
        if len(split) > 1:
            return {'text': split[1].strip().lower(), 'sender': sender}
        # returns None if split doesn't work (not PRIVMSG, or different channel, or bot name not at message start)
        
    def hello(self, stm):        
        resps = ["Hello World!", "hello there", "what's up", "hey buddy", "hey", "hii :)"]
        self.irc.send(random.choice(resps))
        
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
        # TODO: Chatbot must forget all it knows...
        return
    
    #########################
    # Main response handler #
    #########################

    def recieve_message(self, stm):
        if time.time() - self.start_convo_waiter > 5 and stm.state == 'END':
            print("Initiating Greeting!")
            stm.START()
        
        message = self.irc.get_response()
        info = self.get_message_text(message)
        if info is None:
            return
        
        text = info['text']
        print(f"sender: {info['sender']}")
        
        print("Chatbot recieved message:",text)
        
        if ("hello" in text) or ("hi" in text) or ("hey" in text):
            stm.OUTREACH_REPLY_2(sender=info['sender'])

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