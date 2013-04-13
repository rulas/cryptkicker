#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import fileinput
import sys
from cryptkicker.cryptkicker import CryptKicker

def decrypt(phrase, seed):
    ck = CryptKicker(phrase, seed)
    return ck.get_decrypted_text()



def parse_input(finput):
    """
    receives a file handler and parses the number of phrases and the prahses to be __decrypted
    TODO: add checks for maximum 100 phrases 
    TODO: add checks for maximi 100 chars length for each line
    """
    class States():
        SEARCH_NUM, SEARCH_BLANK, SEARCH_PHRASE, IN_PHRASE, END, ABORTING = range(6)

    state = States.SEARCH_NUM
    remaining_phrases = 0
    phrases = list()
    current_phrase = str()
    lines = finput.readlines()

    for line in lines:
        
        if state == States.SEARCH_NUM:
            # print "CS: SEARCH_NUM"
            try:
                remaining_phrases = int(line.strip())
                if remaining_phrases:
                    state = States.SEARCH_BLANK
                    # print "NS: SEARCH_BLANK"
                else:
                    # print "Number of phrases is 0"
                    state = States.END
                    # print "NS: END"
            except ValueError as e:
                # print "NS: ABORTING"
                state = States.ABORTING
                
        elif state == States.SEARCH_BLANK:
            # print "CS: SEARCH_BLANK"
            if line.strip() == '':
                state = States.SEARCH_PHRASE
                # print "NS: SEARCH_PHRASE"
            
        elif state == States.SEARCH_PHRASE:
            # print "CS: SEARCH_PHRASE"
            if line.strip() == '':
                pass
            elif not current_phrase:
                    current_phrase += line.strip()
                    state = States.IN_PHRASE
                    # print "NS: IN_PHRASE"
                    
        elif state == States.IN_PHRASE:
            # print "CS: SEARCH_PHRASE"
            if line.strip() == '':
                phrases.append(current_phrase)
                current_phrase = ''
                remaining_phrases -= 1
                state = States.SEARCH_PHRASE
                if not remaining_phrases:
                    state = States.END
                    # print "NS: END"
            else:
                current_phrase += " " + line.strip()

        elif state == States.END:
            # print "CS: END"
            pass
        
        elif state == States.ABORTING:
            # print "CS: ABORTING"
            break
        
    if current_phrase:
        phrases.append(current_phrase)
        
    return phrases


def main(args):
    #process each of the files submitted as input
    for fpath in args:
        # process the input fpath for input pharases to be __decrypted
        phrases = None
        try:
            print "Processing: %s file" % fpath
            phrases = parse_input(open(fpath))
        except IOError, e:
            print e

        if not phrases:
            print "No phrases to be decrypted. Quitting"
            sys.exit(-1)
        
        # decrypt each phrase individually
        seed = u"la zorra cafe rapidamente brinco sobre el perro negro"
        for phrase in phrases:
            print decrypt(phrase, seed)
            
            

if __name__ == "__main__":
    main(sys.argv[1:])

    
    


