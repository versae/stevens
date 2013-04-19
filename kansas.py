# -*- encoding: utf-8 -*-
from hyphenate import Hyphenator, patterns, exceptions
import re

class Lawrence(object):
    """Lawrence is just a regular working class guy from Kansas trying to put 
        together a text with markup showing word and syllable boundries and stress"""

    def __init__(self, text):
        self.words = text.split()
        self.syllables = self.syllabify()
        self.stress = self.stress()
        self._text = self.combine()

    def _get_text(self):
        return self._text

    text = property(_get_text)

    def syllabify(self):
        HY = Hyphenator(patterns,exceptions)
        syllables = []
        for word in self.words:
            syllables.append(HY.hyphenate_word(word))
        return syllables

    def stress(self):
        for sndx,syl_list in enumerate(self.syllables):
            strtest = False
            if len(syl_list) > 1:
                for ndx,syl in enumerate(syl_list):
                    if s.search(syl):
                        self.syllables[sndx][ndx] = stress + syl
                        strtest = True
                if strtest == False:
                    if v.search(syl_list[-1][-1]):
                        self.syllables[sndx][-2] = stress + syl_list[-2]
                    else:
                        self.syllables[sndx][-1] = stress + syl_list[-1]
        return self.syllables

    def combine(self):
        text = unicode()
        text += '.'.join(self.syllables[0])
        for syl_list in self.syllables[1:]:
            word = '.'.join(syl_list)
            text += "/" 
            text += word
        return text

c = re.compile(u'[bcdfghijklmpqrtvwxyz]')
v = re.compile(u'[aeiouns]')
s = re.compile(u'[áéíóú]')
stress = u"ˈ"



