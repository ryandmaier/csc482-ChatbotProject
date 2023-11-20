
import time

class StateMachine:
    
    def __init__(self, irc):
        self.irc = irc
        self.speaker = None
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
        
        return
    
    def transition(self, transition_dict, state=None):
        self.state = transition_dict[self.state]
        if state:
            self.state = state
        exec(f"self.{self.state}()")
        return
    
    def await_response(self):
        t1 = time.time()
        # TODO: busy wait? resume and let state handle it?
        while time.time() - t1 < 25:
            response = self.irc.get_response()
            # info = chatbot.get_message_text(response)
            # if info is not none:
                # self.transition(self.transitions)
        
        # time expired
        # TODO: maybe create another transition dict for transitions that occur after timeout
        self.transition(self.timeouts)
    
    # STATE FUNCTIONS #
    
    def START(self):
        print("In the start state!")
        # self.transition()
        return
    
    def INITIAL_OUTREACH_1(self):
        if self.speaker == 1:
            # (If we move initiate_greeting() functionality to stm):
            # get list of users
            # randomly choose users
            # send greeting: random.choice(['hello', 'hi', 'hey'])
            pass
            
        # if speaker 2, just wait for response
        self.await_response()
        
    
    def SECONDARY_OUTREACH_1(self):
        pass
    
    def OUTREACH_REPLY_2(self):
        pass
    
    def INQUIRY_1(self):
        pass
    
    # Doesn't have a timeout according to the diagram
    def INQUIRY_REPLY_1(self):
        pass
    
    def INQUIRY_2(self):
        pass
    
    # Doesn't have a timeout according to the diagram
    def INQUIRY_REPLY_2(self):
        pass
    
    def GIVEUP_FUSTRATED(self):
        pass
    
    
    
    

    