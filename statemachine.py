
import time
import random

class StateMachine:
    
    def __init__(self, irc):
        self.irc = irc
        self.speaker = None
        self.state = 'END'
        self.transitions = {
            'START': 'INITIAL_OUTREACH_1',
            'INITIAL_OUTREACH_1': 'OUTREACH_REPLY_2',
            'SECONDARY_OUTREACH_1': 'OUTREACH_REPLY_2',
            'GIVEUP_FRUSTRATED_1': 'END',
            'INQUIRY_1': 'INQUIRY_REPLY_2',
            'INQUIRY_REPLY_1': 'END',
            'OUTREACH_REPLY_2': 'INQUIRY_1',
            'INQUIRY_2': 'INQUIRY_REPLY_1',
            'GIVEUP_FRUSTRATED_2': 'END',
            'INQUIRY_REPLY_2': 'INQUIRY_2',
            'END': 'START'
        }
        
        return
    
    def transition(self, state=None):
        self.state = self.transitions[self.state]
        if state:
            self.state = state
        exec(f"self.{self.state}()")
        return
    
    def await_response(self):
        t1 = time.time()
        # TODO: busy wait? resume and let state handle it?
        while time.time() - t1 < 25:
            response = self.irc.get_response()
            # process response...
        
        # time expired
        # TODO: maybe create another transition dict for transitions that occur
        # after timeout
        self.transition()
    
    # STATE FUNCTIONS #
    
    def START(self):
        print("In the start state!")
        return
    
    def INITIAL_OUTREACH_1(self):
        if self.speaker == 1:
            self.await_response()
        return
    
    def SECONDARY_OUTREACH_1(self):
        pass
    
    def GIVEUP_FUSTRATED_1(self):
        pass
    
    def INQUIRY_1(self):
        pass
    
    def INQUIRY_REPLY_1(self):
        pass
    
    def OUTREACH_REPLY_2(self):
        pass
    
    def GIVEUP_FUSTRATED_2(self):
        pass
    
    def INQUIRY_2(self):
        pass
    
    def INQUIRY_REPLY_2(self):
        pass
    
    
    
    

    