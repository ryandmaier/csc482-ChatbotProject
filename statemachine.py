# Ryan Maier and Bret Craig
import time
import random
from chatbot import ChatBot

class StateMachine:
    
    def __init__(self, irc, chatbot):
        self.irc = irc
        self.chatbot : ChatBot = chatbot
        self.speaker = None
        self.partner = None
        self.state = 'END'
        self.start_convo_waiter = time.time()
        self.transitions = {
            'START': 'INITIAL_OUTREACH_1',
            'INITIAL_OUTREACH_1': 'OUTREACH_REPLY_2',
            'SECONDARY_OUTREACH_1': 'OUTREACH_REPLY_2',
            'GIVEUP_FRUSTRATED': 'END',
            'INQUIRY_1': 'INQUIRY_REPLY_2',
            'INQUIRY_REPLY_1': 'END',
            'OUTREACH_REPLY_2': 'INQUIRY_1',
            'INQUIRY_2': 'INQUIRY_REPLY_1',
            'INQUIRY_REPLY_2': 'INQUIRY_2',
            'END': 'START'
        }
        self.timeouts = {
            'INITIAL_OUTREACH_1': 'SECONDARY_OUTREACH_1',
            'SECONDARY_OUTREACH_1': 'GIVEUP_FRUSTRATED',
            'OUTREACH_REPLY_2': 'GIVEUP_FRUSTRATED',
            'INQUIRY_1': 'END', # If there never is an inquiry, end convo
            'INQUIRY_REPLY_2': 'GIVEUP_FRUSTRATED',
            'INQUIRY_2': 'END', # If there never is an inquiry, end convo
            'INQUIRY_REPLY_1': 'GIVEUP_FRUSTRATED'
        }
    
    def transition(self, transition_dict, state=None):
        self.state = transition_dict[self.state]
        if state:
            self.state = state
        print(f'transitioning to {self.state}')
        exec(f"self.{self.state}()")
        return
    
    def await_response(self):
        t1 = time.time()
        print(f'waiting for response from {self.partner}...')
        while time.time() - t1 < 10:
            info = self.chatbot.recieve_message(self)
            if info == "forget":
                return self.transition(self.transitions, state="END")
            if info is not None and info['sender'] == self.partner:
                return self.transition(self.transitions)
        
        # time expired
        print("did not get a response.")
        self.transition(self.timeouts)
    
    def send_message(self, choices):
        message = random.choice(choices)
        print('Sending message: ',message)
        self.irc.send(f"{self.partner}: {message}")
    
    ###################
    # STATE FUNCTIONS #
    ###################
    
    def START(self):
        print("In the start state!")
        self.speaker = 1
        self.state = 'START'
        self.transition(self.transitions)
    
    def INITIAL_OUTREACH_1(self):
        print('in initial outreach, speaker',self.speaker)
        if self.speaker == 1:
            users_presplit = self.chatbot._get_users()
            print(users_presplit)
            users = users_presplit.split(' ')
            print(users)
            user = self.chatbot.irc.botnick
            while user == self.chatbot.irc.botnick:
                user = random.choice(users)
            self.partner = user

            print(f"Chosen user: {self.partner}")
            self.send_message(['hello', 'hi', 'hey'])
            
        self.await_response()      
    
    def SECONDARY_OUTREACH_1(self):
        print('in secondary outreach, speaker',self.speaker)
        if self.speaker == 1:
            self.send_message(['I said hi!', 'excuse me, hello?', 'are you there?'])
        self.await_response()
               
    def OUTREACH_REPLY_2(self, sender=None):
        print('in outreach reply, speaker',self.speaker)
        if self.speaker is None: # where stm begins as speaker 2
            self.state = 'OUTREACH_REPLY_2'
            self.speaker = 2
            self.partner = sender
            self.send_message(["Hi back!", "hello there", "hey buddy", "hey", "hii :)"])
            
        self.transition(self.transitions)
        
        
    def INQUIRY_1(self):
        print('in inquiry 1, speaker',self.speaker)
        if self.speaker == 1:
            self.send_message(['how are you?', "what's happening", "what's up?"])
            self.transition(self.transitions)
        else:
            self.await_response()
        
    def INQUIRY_REPLY_2(self):
        print('in inquiry reply 2, speaker',self.speaker)
        if self.speaker == 2:
            self.send_message(["I'm doing well", "I'm good", "I'm fine"])
            self.transition(self.transitions)
        else:
            self.await_response()
    
    
    def INQUIRY_2(self):
        print('in inquiry 2, speaker',self.speaker)
        if self.speaker == 2:
            self.send_message(["how about you?", "and yourself?", "and how are you doing?"])
            self.transition(self.transitions)
        else:
            self.await_response()
    
    def INQUIRY_REPLY_1(self):
        print('in inquiry reply 1, speaker',self.speaker)
        if self.speaker == 1:
            self.send_message(["I'm good", "I'm fine, thanks for asking", "doing well."])
            self.transition(self.transitions) # this will transition to END
        else:
            # Wait for inquiry reply, then transition to END
            self.await_response()   
    
    def GIVEUP_FRUSTRATED(self):
        self.send_message(['Ok, forget you.', 'Whatever.', 'I give up!'])
        self.transition(self.transitions)
    
    def END(self):
        print("in end")
        self.speaker = None
        self.partner = None
        self.start_convo_waiter = time.time()
        self.state = 'END'

            
    
    
    

    