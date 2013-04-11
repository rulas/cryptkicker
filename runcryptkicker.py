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
    receives a file handler and parses the number of phrases and the prahses to be decrypted
    TODO: add checks for maximum 100 phrases 
    TODO: add checks for maximi 100 chars length for each line
    """
    class States():
        SEARCH_NUM, SEARCH_BLANK, SEARCH_PHRASE, IN_PHRASE, END, ABORTING = range(6)
    class Events():
        pass
        
    state = States.SEARCH_NUM
    num_phrases = 0
    phrases = list()
    current_phrase = str()
    
    for line in finput.readlines():
        
        if state == States.SEARCH_NUM:
            print "CS: SEARCH_NUM"
            try:
                num_phrases = int(line.strip())
                if num_phrases:
                    state = States.SEARCH_BLANK
                    print "NS: SEARCH_BLANK"
                else:
                    print "Number of phrases is 0"
                    state = States.END
                    print "NS: END"
            except ValueError as e:
                print "NS: ABORTING"
                state = States.ABORTING
                
        elif state == States.SEARCH_BLANK:
            print "CS: SEARCH_BLANK"      
            if line.strip() == '':
                state = States.SEARCH_PHRASE
                print "NS: SEARCH_PHRASE"   
            
        elif state == States.SEARCH_PHRASE:
            print "CS: SEARCH_PHRASE"
            if line.strip() == '':
                pass
            elif not current_phrase:
                    current_phrase += line.strip()
                    state = States.IN_PHRASE
                    print "NS: IN_PHRASE"
                    
        elif state == States.IN_PHRASE:
            print "CS: SEARCH_PHRASE"
            if line.strip() == '':
                phrases.append(current_phrase)
                current_phrase = ''
                num_phrases -= 1;
                if not num_phrases:
                    state = States.END
                    print "NS: END"
            else:
                current_phrase += " " + line.strip()
                
        elif state == States.END:
            print "CS: END"
            pass
        
        elif state == States.ABORTING:
            print "CS: ABORTING"
            break
        
    if current_phrase:
        phrases.append(current_phrase)
        
    return num_phrases, phrases


def main(args):
    #process each of the files submitted as input
    for fpath in args:
        # process the input fpath for input pharases to be decrypted
        try:
            print "Processing: %s fpath" % fpath
            num, phrases = parse_input(open(fpath))
        except IOError, e:
            print e
            
        if num == 0:
            print "No phrases to be decrypted. Quitting"
            sys.exit(-1)
        
        # decrypt each phrase individually
        for phrase in phrases:
            print decrypt(phrase)
            
            

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except:
        print "There was an problem"
    
    
    


