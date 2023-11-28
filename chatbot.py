# Ryan Maier and Bret Craig
import sys
from book import recommend_book

import numpy as np
import requests
import re

def get_bday(name, search=True):
    bday_descs = ["born","date of birth","bday"]
    main_page_id = r"class=\"infobox.*?vcard\""
    search_page_id = '<div id="mw-content-text" class="mw-body-content">'

    name = name.replace('_',' ')
    url = f"https://en.wikipedia.org/w/index.php?search={'_'.join(name.split(' '))}"
    print('url: ',url)
    text = requests.get(url).text.lower()

    if re.search(main_page_id, text):
        if np.array([desc in text for desc in bday_descs]).any():
            regex = f"<th.*?>.*?(?:{'|'.join(bday_descs)}).*?</th>"
            td = re.split(regex, text)[1].split('/td')[0]
            innerhtml = re.sub(r"<.*?>|\[.*?\]|\&\#\d+\;", " ", td)
            bdays = re.findall(r"\w+\s\d+,\s\d+|\d+\s\w+.*?\d{4}", innerhtml)
            if len(bdays) > 0:
                return re.sub(r"\s+", " ",f"According to Wikipedia, {name.title()} was born {bdays[0].title()}.")
    if (search_page_id in text) and (search == True):
        content = text.split(search_page_id)[1]
        if "mw-search-results-container" in content:
            content = ''.join(content.split("mw-search-results-container")[1:])
        elif 'id="people"' in content:
            content = ''.join(content.split('id="people"')[1:])
        pages = [ s.split('\"')[0] for s in content.split("\"/wiki/")[1:] ]
        return get_bday(pages[0], search=False)
    
    return f"No birthdate found for {name.replace('_',' ').title()}"
    
def bday_question(q):
    q = q.lower()
    regex = r"when was .*? born\?"
    if re.match(regex, q):
        name = q.split("when was ")[1].split(" born?")[0]
        return get_bday(name)

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
        line2 = f"""{sender}: I can tell you someone's birthday by looking them up on Wikipedia. Just ask "When was [NAME] born?" """
        line3 = f"{sender}: I can also recommend books based on author or genre. Try these commands:"
        line4 = f"{sender}: > recommend a [GENRE] book"
        line5 = f"{sender}: > recommend a book by [AUTHOR]"
        self.irc.send(line2)
        self.irc.send(line3)
        self.irc.send(line4)
        self.irc.send(line5)
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
        sender = info['sender']
        print(f"sender: {sender}")
        
        print("Chatbot recieved message:",text)
        
        
        ### BRET'S FEATURE ###
        
        genre_pattern = r"recommend a (.+) book"
        author_pattern = r"recommend a book by (.+)"
        genre_match = re.match(genre_pattern, text, re.IGNORECASE)
        author_match = re.match(author_pattern, text, re.IGNORECASE)

        if genre_match and stm.state == 'END':
            genre = genre_match.group(1)
            query = f"subject:{genre}"
            self.irc.send(f'{sender}: {recommend_book(query)}')
            
        elif author_match and stm.state == 'END':
            author = author_match.group(1)
            query = f'inauthor:"{author}"'
            self.irc.send(f'{sender}: {recommend_book(query)}')
            
        #######################
        
        elif (("hello" in text) or ("hi" in text) or ("hey" in text)) and stm.state == 'END':
            stm.OUTREACH_REPLY_2(sender=info['sender'])

        elif "die" in text:
            self.irc.send("you may take my life but you'll never take my freedom")
            self.irc.command("QUIT")
            sys.exit()
            
        elif "users" in text:
            self.users()
            return None
            
        elif ("usage" in text) or ("who are you?" in text):
            self.usage(sender)
            return None
            
        elif text == "forget":
            # return message so stm knows to transition to END and return
            return self.forget()
        
        elif re.match(r"when was .*? born\?", text):
            self.irc.send(f"{info['sender']}: {bday_question(text)}")
            return None
        
        else:
            return info
