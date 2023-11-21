import sys
import time
import random

class StateMachine:
    
    def __init__(self, irc, chatbot):
        self.irc = irc
        self.chatbot = chatbot
        self.speaker = None
        self.partner = None
        self.state = 'END'
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
            'INITIAL_OUTREACH_1': 'SECONDARY_OUTREACH_2',
            'SECONDARY_OUTREACH_2': 'GIVEUP_FRUSTRATED',
            'OUTREACH_REPLY_2': 'GIVEUP_FRUSTRATED',
            'INQUIRY_1': 'GIVEUP_FRUSTRATED',
            'INQUIRY_2': 'GIVEUP_FRUSTRATED'
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
        # TODO: busy wait? resume and let state handle it?
        print('waiting for response...')
        while time.time() - t1 < 10:
            response = self.irc.get_response()
            info = self.chatbot.get_message_text(response)
            if info is not None and info['sender'] == self.partner:
                self.transition(self.transitions)
                return
        
        # time expired
        print("did not get a response.")
        self.transition(self.timeouts)
    
    def send_message(self, choices):
        message = random.choice(choices)
        self.irc.send(f"{self.partner}: {message}")
    
    # STATE FUNCTIONS #
    
    def START(self):
        print("In the start state!")
        self.speaker = 1
        self.state = 'START'
        self.transition()
    
    def INITIAL_OUTREACH_1(self):
        print('in initial outreach')
        if self.speaker == 1:
            # user = random.choice(self.chatbot._get_users().split(' '))
            user = 'tester7'
            self.partner = user
            self.send_message(['hello', 'hi', 'hey'])
            
        # if speaker 2, just wait for response
        self.await_response()      
    
    def SECONDARY_OUTREACH_1(self):
        print('in secondary outreach')
        if self.speaker == 1:
            self.send_message(['I said hi!', 'excuse me, hello?', 'are you there?'])
        
        self.await_response()
               
    def OUTREACH_REPLY_2(self, sender=None):
        print('in outreach reply')
        if self.speaker is None: # where stm begins as speaker 2
            self.state = 'OUTREACH_REPLY_2'
            self.speaker == 2
            self.partner = sender
            self.send_message(["Hi back!", "hello there", "hey buddy", "hey", "hii :)"])
        
        self.await_response()
        
        
    def INQUIRY_1(self):
        print('in inquiry 1')
        if self.speaker == 1:
            self.send_message(['how are you?', "what's happening", "what's up?"])
        
        self.await_response()
        
    # Doesn't have a timeout according to the diagram
    def INQUIRY_REPLY_2(self):
        print('in inquiry reply 2')
        if self.speaker == 2:
            self.send_message(["I'm doing well", "I'm good", "I'm fine"])
        else:
            self.await_response()
    
    
    def INQUIRY_2(self):
        print("in inquiry 2")
        if self.speaker == 2:
            self.send_message(["how about you?", "and yourself?", "and how are you doing?"])
            
        self.await_response()
    
    # Doesn't have a timeout according to the diagram
    def INQUIRY_REPLY_1(self):
        print("in inquiry reply 1")
        if self.speaker == 1:
            self.send_message(["I'm good", "I'm fine, thanks for asking", "doing well."])
        
        self.transition(self.transitions)        
    
    def GIVEUP_FRUSTRATED(self):
        self.send_message(['Ok, forget you.', 'Whatever.', 'I give up!'])
        self.transition(self.transitions)
    
    def END(self):
        print("in end")
        self.speaker = None
        self.partner = None
        self.state = 'END'
            
    
    
    

    