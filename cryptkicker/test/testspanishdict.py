#!/usr/bin/env python
# -*- coding: utf-8 -*- 


'''
Created on Apr 8, 2013

@author: lrvillan
'''

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
        self.assertTrue(self.spadict.wordexists('hola'))
        self.assertTrue(self.spadict.wordexists('zapato'))
        self.assertTrue(self.spadict.wordexists('almohada'))
    
    @unittest.SkipTest    
    def testCheckForEntryUnicode(self):
        self.assertTrue(self.spadict.wordexists('años'))
        self.assertTrue(self.spadict.wordexists('informó'))
        self.assertTrue(self.spadict.wordexists('mamá'))
        
    @unittest.SkipTest    
    def testFindNearest(self):
        self.assertTrue(self.spadict.findnearest('hols') == 'hola')
        self.assertTrue(self.spadict.findnearest('rapato') == 'zapato')
        self.assertTrue(self.spadict.findnearest('almojada') == 'almohada')

    def testFindNearestUnicode(self):
        unknown = ['dinertidos', 'concirsos', 'vombres', 'acidan', 'atidar', 'yie']

        for word in unknown:
            print self.spadict.findnearest(word)
        

if __name__ == '__main__':
    unittest.main()