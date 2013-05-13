#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# from unidecode import unidecode
import sys


class SpanishDict(object):

    """

    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpanishDict, cls).__new__(cls, *args, **kwargs)
        return cls._instance


    def __init__(self, finput, maxentries):
        
        lines = []
        ffile = None
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
        self.__build_word_size_list()
         
        
        del lines    
        ffile.close()

    def __build_words_list(self, lines):
        self.wordslist = []
        
        # start retriving the dictionary entries and put them in a list
        remaining_entries = self.entries
        
        for line in lines[1:]:
            # 2nd column is the key
            # self.wordslist.append(unidecode(line.split()[1]))
            try:
                self.wordslist.append(line.split()[1])
                remaining_entries -= 1
                if not remaining_entries:
                    break
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise

    def __build_word_size_list(self):
        # initializes the dictionary to contain a list each
        for index in range(0,50):
            self.sizewordsdict[index] = []
            
        # start categorizing words by their length
        for word in self.wordslist:
            self.sizewordsdict[len(word)].append(word)

    def __find_word_differences(self, string1, string2):
        """
        compares two string character by character and returns the number of chars that
        don't match
        @param string1
        @param string2
        """
        return len([True for char1, char2 in zip(string1, string2) if char1 != char2])

    def word_exists(self, name):
        return name in self.wordslist

    def find_nearest(self, name):
        # get the list of words that matches the length of name
        """

        :param name:
        :return:
        """
        same_length_words = self.sizewordsdict[len(name)]

        # calculate the difference
        word_differences = [(self.__find_word_differences(word, name), word) for word in same_length_words]

        min_difference = min([num for num, word in word_differences])

        nearest_words = [word for num, word in word_differences if num == min_difference]

        return nearest_words
                


if __name__ == '__main__':
    pass