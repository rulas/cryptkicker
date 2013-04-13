# coding=utf-8
"""
Created on Apr 8, 2013

@author: Raul Villanueva
"""

from __future__ import division
from spanishdict import SpanishDict


class CryptKicker(object):

    """

    """

    def __init__(self, phrase, seed):
        """

        @param phrase: the phrase to be decrypted

        @param seed: a sentence that we know exists within phrase
        """

        #TODO: we may want to pass the dictionary as an object, instead of creating here.
        self.__spanish_dictionary = SpanishDict('./dictionaries/CREA_total.TXT', maxentries=100000)

        self.set_phrase_seed(phrase, seed)

        self.decrypt()

    def set_phrase_seed(self, phrase, seed):
        """

        :param seed:
        :param phrase:
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

        # make a dictionary that contains letter translation for decryption
        self.__character_translation_dict = {}

        # this will tell us the number of unknown words so far
        self.__unknown_words_list = self.__get_unkown_words()
        self.__unknown_words = len(self.__unknown_words_list)
        self.__decryption_attempts = 0
        self.__decrypted = False


    def decrypt(self):
        """
	performs full decryption
        """
        # process seed so that we can at least decrypt some words
        self.__decrypt_using_seed()
        # decrypt the remaining words
        self.__decrypt_unknown_words()
       
    def __print_progress(self, verbose=False, enable=0):
        """
        prints a summary of decryption process
        """
        if enable:
            if verbose:
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
        
        # once found marks those words as __decrypted and update the translation dictionary accordingly
        seed_length = len(self.__seed_words_list)
        start = seed_position
        end = seed_position + seed_length
        found_words = self.__phrase_words_list[start:end]
        
        for encrypted, decrypted  in zip(found_words, self.__seed_words_list):
            self.__update_translation(encrypted, decrypted)
        
        # process the remaining words and decrypt all the known letters and mark those letters as __decrypted
        self.__propagate_update()
        self.__print_progress(verbose=True)
        
        
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

    def __get_unkown_words(self):
        unknown_words = []
        for word in self.__phrase_words_set:
            if '*' in self.__words_translation_dict[word]:
                unknown_words.append(word)

        self.__unknown_words = len(unknown_words)
        return unknown_words

    def __guess_word(self, unknown_word):
        """
        guess the word
        """
        nearest_words = self.__spanish_dictionary.find_nearest(str(unknown_word))

        return nearest_words

    def __count_char_differences(self, word1, word2):
        count = 0
        # count different characters
        for char1, char2 in zip(word1, word2):
            if char1 != char2:
                count += 1

        return count

    def __find_dict_key_from_value(self, value):
        """
        find the key of value within the words_translation_dict
        """
        word_key = None
        for k, v in self.__words_translation_dict.iteritems():
            if v == value:
                word_key = k
                break

        return word_key

    def __decrypt_unknown_words(self):
        # find all words with unknown chars
        unknown_words = self.__get_unkown_words()
        remaining_attempts = 3
        words_found = 0

        # FIRST PASS
        # attempt to guess the word using a dictionary, but only if the number of possible words that can fit in the
        # unencrypted word is 1 choice. we need to be really sure we find the exact word here.
        while unknown_words and remaining_attempts:
            # order words by higher ratio of unknown versus known chars
            # ordered_unknown_words = sorted(unknown_words, key=lambda word: \
            #         self.__words_translation_dict[word].count('*')/len(self.__words_translation_dict[word]))
            # ordered_unknown_words = [self.__words_translation_dict[word] for word in ordered_unknown_words]

            #print "unknown words: %s" % (unknown_words)
            # guess word. A word is found if only one word was returned.
            for word in unknown_words:
                word = self.__words_translation_dict[word]
                guessed_words = self.__guess_word(word)

                if len(guessed_words) == 1:
                    #print "**** 1 word found: %s ****" % (guessed_words[0])
                    # find the key associated to word in order to update
                    key = self.__find_dict_key_from_value(word)
                    # update and propagate findings to all words
                    self.__update_translation(key, guessed_words[0])
                    self.__propagate_update()
                    self.__print_progress()
                    words_found += 1

            unknown_words = self.__get_unkown_words()
            remaining_attempts -= 1

        # SECOND PASS
        # At this state, we know there are still unknown words. However, it seems we will have to predict them
        # by using the most used words as per the dictionary. there may be another way, but for now this should be
        # fine
        if unknown_words:

            for word in unknown_words:
                word = self.__words_translation_dict[word]
                guessed_words = self.__guess_word(word)

                char_diff = self.__count_char_differences(word, guessed_words[0])

                if char_diff <= 2:
                    key = self.__find_dict_key_from_value(word)
                    self.__update_character_translation_dict(key, guessed_words[0])
                    self.__update_word_translation_dict(key, guessed_words[0])
                    self.__propagate_update()
                    self.__print_progress()

            unknown_words = self.__get_unkown_words()

        if not unknown_words:
            self.__decrypted = True
            return

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
        if self.__decrypted:
            result = " ".join([self.__words_translation_dict[word] for word in self.__phrase_words_list])
        else:
            result = "NO SE ENCONTRO SOLUCION"
        return result
