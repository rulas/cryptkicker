'''
Created on Apr 8, 2013

@author: Raul Villanueva
'''

from __future__ import division
from spanishdict import SpanishDict
import re

class CryptKicker():

    def __init__(self, phrase, seed):
        """

        @param phrase: the phrase to be decrypted

        @param seed: a sentence that we know exists within phrase
        """

        #TODO: we may want to pass the dictionary as an object, instead of creating here.
        self.__spanish_dictionary = SpanishDict('../../dictionaries/CREA_total.TXT', maxentries=100000)

        self.set_phrase_seed(phrase, seed)

        self.decrypt()

    def set_phrase_seed(self, phrase, seed):
        """

        """
        self.phrase = phrase
        self.seed = seed
        self.__phrase_words_list = self.phrase.split()
        self.__phrase_words_set = set(self.__phrase_words_list)
        self.__seed_words_list = self.seed.split()
        # make a dictionary for all words to be translated
        self.__words_translation_dict = {}
        for word in self.__phrase_words_set:
            self.__words_translation_dict[word] = '*' * len(word)
            # self.__decryption_mask = {}
        # for word in self.__phrase_words_list:
        #     self.update_decrypt_dict(word, word, '*' * len(word))
        # make a dictionary that contains letter translation for decryption
        self.__character_translation_dict = {}

    def decrypt(self):
        """

        """
        # process seed so that we can at least decrypt some words
        self.__decrypt_using_seed()
        # decrypt the remaining words
        self.decrypted = self.__decrypt_unknown_words()
       
    def __print_progress(self, long=False, enable=False):
        """
        prints a summary of decryption process
        """
        if enable:
            if long:
                print "\n%s" % " ".join([item for item in self.__character_translation_dict.keys()])
                print "%s" % " ".join([item for item in self.__character_translation_dict.values()])
                print "==> %s" % self.phrase

            output = " ".join([self.__words_translation_dict[word] for word in self.__phrase_words_list])
            print "--> %s" % output

              
        
    def __find_seed_pos(self):
        """
        Find the position of the seed within the phrase

        @return: the position where the match occurred
        """

        # form a string that indicates the lengths for the seed and phrase
        seed_lengths = " ".join([str(len(word)) for word in self.__seed_words_list])
        phrase_lengths = " ".join([str(len(word)) for word in self.__phrase_words_list])

        # so that we can search seed within phrase using string.find
        position = phrase_lengths.find(seed_lengths)
        
        # word number within phrase is equal to the number of spaces until the seed was found minus 1
        word_position = len(phrase_lengths[:position].split())
        
        return word_position
    
    def __decrypt_using_seed(self):
        """
        decrypt the phrase using seed
               
        @return: True if success, false otherwise
        """
        # find the place where the seed should be based on the seed words lenght
        seed_position = self.__find_seed_pos()
        
        if not seed_position:
            raise ValueError("seed was not found within phrase, we can not continue")
        
        # once found marks those words as decrypted and update the translation dictionary accordingly
        seed_length = len(self.__seed_words_list)
        start = seed_position
        end = seed_position + seed_length
        found_words = self.__phrase_words_list[start:end]
        
        for encrypted, decrypted  in zip(found_words, self.__seed_words_list):
            self.__update_translation(encrypted, decrypted)
        
        # process the remaining words and decrypt all the known letters and mark those letters as decrypted
        self.__propagate_update()
        self.__print_progress(long=True)
        
        
    def __propagate_update(self):
        """
        propagate the result of a any found character to all unencrypted words.
        """
        # for each word within the list of words, check if there are any letter that can be translated
        for dict_key in self.__phrase_words_set:

            dict_value = self.__words_translation_dict[dict_key]

            # an asterisk in dict_value means there are characters pending to translate,
            # so attempt to translate that character
            if '*' in dict_value:
                new_dict_value = ""

                for key_char, value_char in zip(dict_key, dict_value):
                    if value_char is '*':
                        if key_char in self.__character_translation_dict:
                            new_dict_value += self.__character_translation_dict[key_char]
                        else:
                            new_dict_value += value_char
                    else:
                        new_dict_value += value_char

                self.__words_translation_dict[dict_key] = new_dict_value

                    
    def __update_character_translation_dict(self, word, found_word):
        """
        updates the character translation dictionary

        :param word: w
        :param found_word:
        """
        for char1, char2 in zip(word, found_word):
            if char1 not in self.__character_translation_dict:
                self.__character_translation_dict[char1] = char2


    def __update_word_translation_dict(self, word, found_word):
        """
        updates the word translation dictionary

        :param word: word that will be updated
        :param found_word: update content
        """

        self.__words_translation_dict[word] = found_word

    def __decrypt_unknown_words(self):
        # find all words with unknown chars
        unknown_words = []
        for word in self.__phrase_words_set:
            if '*' in self.__words_translation_dict[word]:
                unknown_words.append(word)

        # if not unkownn words, then we are done. just return.
        if not unknown_words:
            #FIMXE: add check to stop if we can not continue decrypting words
            return True
            
        # order words by higher ratio of unknown versus known chars
        ordered_unknown_words = sorted(unknown_words, key=lambda word: self.__words_translation_dict[word].count('*')/len(self.__words_translation_dict[word]))
        ordered_unknown_words = [self.__words_translation_dict[word] for word in ordered_unknown_words]

        first_unknown_word = ordered_unknown_words[0]

        nearest_word = self.__spanish_dictionary.findnearest(str(first_unknown_word))
        
        # find the key of value within the words_translation_dict
        word_key = None
        for key, value in self.__words_translation_dict.iteritems():
            if value == first_unknown_word:
                word_key = key
                break
                
        self.__update_translation(word_key, nearest_word)
        self.__propagate_update()
        self.__print_progress()

        # recursion
        self.__decrypt_unknown_words()
                    
    
    def __update_translation(self, word, found_word):
        """
        indicates that we found a decryption method for word. This is found word
        and we need to update everything based on that

        @param word: the word that will be updated
        @param found_word: word used to update
        """
        self.__update_character_translation_dict(word, found_word)
        self.__update_word_translation_dict(word, found_word)


    def get_decrypted_text(self):
        """
        returns the result of the decryption

        """
        result = " ".join([self.__words_translation_dict[word] for word in self.__phrase_words_list])
        return result
