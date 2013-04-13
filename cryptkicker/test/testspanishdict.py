#!/usr/bin/env python
# -*- coding: utf-8 -*- 


'''
Created on Apr 8, 2013

@author: lrvillan
'''
import random
from symbol import while_stmt

import unittest
import timeit

from cryptkicker.spanishdict import SpanishDict



class TestSpanishDict(unittest.TestCase):
    def setUp(self):        
        DICTPATH = r'../../dictionaries/CREA_total.TXT'
        ENTRIES = 100000
        
        self.spadict = SpanishDict(DICTPATH, ENTRIES)

    def tearDown(self):
        pass
            
    def testCheckForEntry(self):
        self.assertTrue(self.spadict.word_exists('hola'))
        self.assertTrue(self.spadict.word_exists('zapato'))
        self.assertTrue(self.spadict.word_exists('almohada'))
    
    @unittest.SkipTest    
    def testCheckForEntryUnicode(self):
        self.assertTrue(self.spadict.word_exists('años'))
        self.assertTrue(self.spadict.word_exists('informó'))
        self.assertTrue(self.spadict.word_exists('mamá'))

    def __generate_words_chars_hidden(self, word, num_chars, num_words):
        """
        """
        words_list = []
        word_chars = list(word)
        remaining_words = num_words

        while(remaining_words):
            new_word = word
            samples = random.sample(word_chars, num_chars)
            for sample in samples:
                new_word = new_word.replace(sample, '*')

            if new_word not in words_list:
                words_list.append(new_word)
                remaining_words -= 1

        return words_list

    def testFindNearest(self):

        for word in self.__generate_words_chars_hidden('hola', 1, 4):
            self.assertTrue(self.spadict.find_nearest(word) == 'hola')

        for word in self.__generate_words_chars_hidden('hola', 2, 4):
            self.assertTrue(self.spadict.find_nearest(word) == 'hola')

        for word in self.__generate_words_chars_hidden('almohada', 1, 50):
            self.assertTrue(self.spadict.find_nearest(word) == 'almohada')

        for word in self.__generate_words_chars_hidden('almohada', 2, 50):
            self.assertTrue(self.spadict.find_nearest(word) == 'almohada')

        for word in self.__generate_words_chars_hidden('almohada', 3, 50):
            self.assertTrue(self.spadict.find_nearest(word) == 'almohada')

        for word in self.__generate_words_chars_hidden('almohada', 4, 50):
            self.assertTrue(self.spadict.find_nearest(word) == 'almohada')



    def testFindNearestUnicode(self):
        unknown = ['dinertidos', 'concirsos', 'vombres', 'acidan', 'atidar', 'yie']

        for word in unknown:
            print self.spadict.find_nearest(word)

        

if __name__ == '__main__':
    unittest.main()