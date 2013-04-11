#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on Apr 8, 2013

@author: lrvillan
'''

import unittest
import sys
from cryptkicker.cryptkicker import CryptKicker


class TestCryptKicker(unittest.TestCase):


    def setUp(self):
        self.phrase = u"uñou uñ ub eceuhoc axrx yiu bcñ vcekruñ xqisxh x xtisxr x bx pfuñox bx wcrrx qxpu rxafsxeuhou krfhqc ñckru ub aurrc humrc bcñ qchqirñcñ su arcmrxexqfch ñch sfnurofscñ"
        self.phrase2 = u"vhgv vh vo nlnvmgl vm jfv glwlh xlnrvmazm z tirgzi xfzmwl kivxrhznvmgv oz aliiz xzuv izkrwznvmgv yirmxl hlyiv vo kviil mvtil jfv ml szxrz nzh jfv wlinri"
        self.phrase3 = u"ftubcbnpt bij tfoubept dvboep ef sfqfouf ubo gvhba rvf qbsfdjb vo sbzp mboabep qps fm njtnp tfñps efm usvfop bij ftubcb zp dvboep mb apssb dbgf sbqjebnfouf csjodp tpcsf fm qfssp ofhsp rvf tfhvjb tjo foufoefs rvf fsb mp rvf qbtbcb"
        self.seed = u"la zorra cafe rapidamente brinco sobre el perro negro"
        
        sys.stdout = sys.stderr


    def tearDown(self):
        pass


    def testFindSeedPos(self):       
        ck = CryptKicker(self.phrase, self.seed)
        position = ck.__find_seed_pos()
        self.assertEquals(position, 14)        
    
    def testProcessSeed(self):
        # ck = CryptKicker(self.phrase, self.seed)
        # ck.__decrypt_using_seed()
        # ck.__decrypt_unknown_words()
        # ck = CryptKicker(self.phrase2, self.seed)
        # ck.__decrypt_using_seed()
        # ck.__decrypt_unknown_words()
        # ck = CryptKicker(self.phrase3, self.seed)
        # ck.__decrypt_using_seed()
        # ck.__decrypt_unknown_words()
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()