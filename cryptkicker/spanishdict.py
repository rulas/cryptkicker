#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import Levenshtein as lv
from unidecode import unidecode


class SpanishDict():
    
    def __init__(self, finput, maxentries):
        
        lines = []
        
        try:
            ffile = open(finput)
            lines = ffile.readlines()
        except IOError as e:
            print e
        
        self.entries = maxentries
        if maxentries is -1:
            self.entries = len(lines) - 1
            
        self.wordslist = []
        self.sizewordsdict = {}
            
        self.__build_words_list(lines)
        self.__build_word_size_list(lines)
         
        
        del lines    
        ffile.close()

    def __build_words_list(self, lines):
        self.wordslist = []
        
        # start retriving the dictionary entries and put them in a list
        remaining_entries = self.entries
        
        for line in lines[1:]:
            # 2nd column is the key
            self.wordslist.append(unidecode(line.split()[1]))
            remaining_entries -= 1
            if not remaining_entries:
                break 
            
    def __build_word_size_list(self, lines):
        # initializes the dictionary to contain a list each
        for index in range(0,50):
            self.sizewordsdict[index] = []
            
        # start categorizing words by their length
        for word in self.wordslist:
            self.sizewordsdict[len(word)].append(word)

    def wordexists(self, name):
        return name in self.wordslist

    def findnearest(self, name, maxdist=1):
        wordslist = self.sizewordsdict[len(name)]
#         for word in wordslist:
#             print word, name, lv.distance(name, word)
        distances = [lv.distance(name, word) for word in wordslist]
        mindistance = min(distances)
        mindistances = []
        nearestwords = []
        for index, distance in enumerate(distances):
            if distance == mindistance:
                mindistances.append(index)
                nearestwords.append(wordslist[index])
        
        return nearestwords[0]
                
    def __getitem__(self, name):
        pass
    
    def __contains__(self, name):
        pass
    
    def has_key(self, name):
        pass

    
    
    
            
            
if __name__ == '__main__':
    pass