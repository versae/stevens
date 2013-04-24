# -*- coding: utf-8 -*-
import re

from stevens.languages import BaseTranscriptor
from stevens.hyphenation import get_hyphenator


class Transcriptor(BaseTranscriptor):
    # untested as part of the class. the gist runs well, too early to say awesome,
    # but looking good.
    # set all of the text processing constants to attributes.
    # don't know how this works with transcription_rules functions.
    # can change.
    def __init__(self, *args, **kwargs):
        super(Transcriptor, self).__init__(*args, **kwargs)
        if not self._hyphenator:
            self._hyphenator = get_hyphenator("es_ES")
        self._punctuation = re.compile(r"[ \.,\?\!¡¿\n\t\s]+")
        self._grave = re.compile(u'[aeiouns]')
        self._irregular = re.compile(u'[áéíóú]')
        self._double_letters = {u'rr':u'R',u'll':u'ʎ',u'ch':u'ʧ',u'gu':u'g',u'qu':u'q'}
        self._nasals = set([u'm',u'n',u'ñ'])
        self._laterals = set([u'l'])
        self._vowels = set([u'a',u'e',u'i',u'o',u'u',u'á',u'é',u'í',u'ó',u'ú'])
        self._voiced = set([u'a',u'e',u'i',u'o',u'u',u'b',u'd',u'g',u'l',u'm',
                        u'n',u'r',u'R',u'v',u'w'])
        self._voiced_consonants = set([u'b',u'd',u'g',u'l',u'm',u'n',u'r',u'R',u'v'])
        self._labiodentals = set([u'f',u'v'])
        self._coronals = set([u'd',u'l',u'r',u'n',u's',u't',u'z',u'ʧ'])
        self._palatals = set([u'y',u'ʎ'])
        self._bilabials = set([u'b',u'm',u'p'])
        self._velars = set([u'g',u'j',u'q'])
        self._pause = u'‖'

    def transcribe_syllable(self, syllable, previous=None, next=None,
                            alphabet=None, stress_mark=None):
        transcribed_syllable = unicode()
        if previous:
            cross_syllabic_previous = previous[-1]
        else:
            cross_syllabic_previous = None
        if next:
            cross_syllabic_next = next[0]
        else:
            cross_syllabic_next = None
        syllable = self.kill_doubles(syllable)
        syllable_length = len(syllable)
        if syllable_length == 1:
            return rule_dict[syllable[0]](
                cross_syllabic_previous,
                cross_syllabic_next,0
            )
        for index, letter in enumerate(syllable):
            previous, next = self.get_surroundings(
                index,
                letter,
                syllable,
                syllable_length
            )
            if index == 0:
                ipa_symbol = rule_dict[letter](
                    cross_syllabic_previous,
                    next,
                    index
                )
                transcribed_syllable += ipa_symbol
            elif index == len(syllable) - 1:
                ipa_symbol = rule_dict[letter](
                    previous,
                    cross_syllabic_next,
                    index
                )
                transcribed_syllable += ipa_symbol
            else:
                ipa_symbol = rule_dict[letter](previous,next,index)
                transcribed_syllable += ipa_symbol
        return transcribed_syllable

    def kill_doubles(self,syllable):
        if len(syllable) == 1:
            return syllable
        double = syllable[0] + syllable[1]
        if double in self._double_letters.keys():
            syllable = self._double_letters[double] + syllable[2:] 
        return syllable

    def transcription_rules(self):

        def transcribe_a(previous, next, index):
            return u'a'
                                                                                                
        def transcribe_b(previous, next, index):
            if not previous or previous in self._nasals \
                    or previous == self._pause:
                return u'b'
            else:
                return u'β'
         
        def transcribe_c(previous, next, index):
            if next in [u'i',u'o']:
                return u's' # or u'θ'
            else:
                return u'k'

        def transcribe_ch(previous, next, index):
            return u'ʧ'
         
        def transcribe_d(previous, next, index): 
            if not previous or previous in self._nasals \
                    or previous in self._laterals or previous == self._pause:
                return u'd'
            else:
                return u'ð'

        def transcribe_e(previous, next, index):
            return u'e'

        def transcribe_stressed_e(previous, next, index):
            return u'e'
         
        def transcribe_f(previous, next, index):
            if next in self._voiced:
                return u'v'
            else:
                return u'f'
         
        def transcribe_g(previous, next, index):
            if next in [u'i',u'e']:
                return u'x'
            elif not previous or previous in self._nasals \
                        or previous == self._pause:
                return u'ɡ'
            else:
                return u'ɣ'

        def transcribe_h(previous, next, index):
            return ''

        def transcribe_i(previous, next, index):
            if next in [u'e',u'a',u'o']:
                return u'j'
            else:
                return u'i'

        def transcribe_stressed_i(previous,next):
            return u'i'
         
        def transcribe_j(previous, next, index):
            return u'x' # this may vary based on prev, next, 
                        # possibly need a uvular u'χ'

        def transcribe_l(previous, next, index):
            return u'l' # this takes diacritics based on next

        def transcribe_ll(previous, next, index):
            if not previous or previous in self._nasals \
                    or previous in self._laterals or previous == self._pause:
                return u'ʑ' # maybe u'ʎ'
            else:
                return u'ʝ'

        def transcribe_m(previous, next, index):
            return u'm'
         
        def transcribe_n(previous, next, index):
            if not next or next in self._vowels:
                return u'n'
            elif next in self._labiodentals:
                return u'ɱ'
            elif next in self._coronals:
                return u'n'
            elif next in self._palatals:
                return u'ɲ'
            elif next in self._bilabials:
                return u'm'
            elif next in self._velars:
                return u'ŋ'
            else:
                return u'ɴ'

        def transcribe_enye(previous, next):
            return u'ɲ'

        def transcribe_o(previous, next, index):
            return u'o'

        def transcribe_stressed_o(previous, next, index):
            return u'o'

        def transcribe_p(previous, next, index):
            return u'p'

        def transcribe_q(previous, next, index):
            return u'k'

        def transcribe_r(previous, next, index):
            if not previous or previous in [self._pause,u'l',u'n',u's']: 
                return u'r'                 # make an attribute maybe
            else:
                return u'ɾ'

        def transcribe_trill(previous, next, index):
            return u'r'

        def transcribe_s(previous, next, index):
            if next in self._voiced_consonants:
                return u'z'
            else:
                return u's'

        def transcribe_t(previous, next, index):
            return u't'

        def transcribe_u(previous, next, index):
            if next in [u'i',u'e',u'a']: # att?
                return u'w'
            else:
                return u'u'

        def transcribe_stressed_u(previous, next, index):
            return u'u'

        def transcribe_v(previous, next, index):
            return u'v'

        def transcribe_w(previous, next, index):
            return u'w'

        def transcribe_x(previous, next, index):
            if index == 0:
                return u'x'
            else:
                return u'ks' # need a better smbol here...maybe

        def transcribe_y(previous, next, index):
            if previous == None and next == None:
                return u'i'
            elif not previous or previous in self._nasals \
                    or previous in self._laterals or previous == self._pause:
                return u'ʑ' # maybe u'ʎ'
            elif previous == u'o':
                return u'i'
            else:
                return u'ʝ' 

        def transcribe_z(previous, next, index):
            if next in self._voiced_consonants:
                return u'z'
            else:
                return u's'
                
        return locals()

    def mark_stress(self, syllable_list):
        ### maybe change name to find_stress
        if len(syllable_list) == 1:
            return None 
            for index, syllable in enumerate(syllable_list):
                if self._irregular.search(syllable):
                    return index
            if self._grave.search(syllable_list[-1][-1]):
                return len(syllable_list) - 2
            else:
                return len(syllable_list) - 1
