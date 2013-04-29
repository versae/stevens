# -*- coding: utf-8 -*-
import re

from stevens.languages import BaseTranscriptor
from stevens.hyphenation import get_hyphenator


class Transcriptor(BaseTranscriptor):

    def __init__(self, *args, **kwargs):
        super(Transcriptor, self).__init__(*args, **kwargs)
        if not self._hyphenator:
            self._hyphenator = get_hyphenator("es_ES")
        self._punctuation = re.compile(r"[ \.,\?\!¡¿\n\t]+")
        self._grave = re.compile(u'[aeiouns]')
        self._irregular = re.compile(u'[áéíóú]')
        self._double_consonants = {u'rr': u'R', u'll': u'ʎ', u'ch': u'ʧ',
                                   u'gu': u'g', u'qu': u'q'}
        self._double_consonants_set = set(self._double_consonants.keys())
        self._nasals = u'mnñ'
        self._laterals = u'l'
        self._vowels = u'aeiouáéíóú'
        self._voiced = u'aeioubdglmnrRvw'
        self._voiced_consonants = u'bdglmnrRv'
        self._labiodentals = u'fv'
        self._coronals = u'dlrnstzʧ'
        self._palatals = u'yʎ'
        self._bilabials = u'bmp'
        self._velars = u'gjq'
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
        syllable = self.remove_double_consonants(syllable)
        syllable_length = len(syllable)
        if syllable_length == 1:
            rule_func = self.rules.get(syllable[0],
                                       lambda p, n, i: syllable[0])
            return rule_func(
                cross_syllabic_previous,
                cross_syllabic_next, 0
            )
        for index, letter in enumerate(syllable):
            previous, next = self.get_surroundings(
                index,
                letter,
                syllable,
                syllable_length
            )
            if index == 0:
                rule_func = self.rules.get(letter, lambda p, n, i: syllable[0])
                ipa_symbol = rule_func(
                    cross_syllabic_previous,
                    next,
                    index
                )
                transcribed_syllable += ipa_symbol
            elif index == len(syllable) - 1:
                rule_func = self.rules.get(letter, lambda p, n, i: syllable[0])
                ipa_symbol = rule_func(
                    previous,
                    cross_syllabic_next,
                    index
                )
                transcribed_syllable += ipa_symbol
            else:
                rule_func = self.rules.get(letter, lambda p, n, i: syllable[0])
                ipa_symbol = rule_func(previous, next, index)
                transcribed_syllable += ipa_symbol
        return transcribed_syllable

    def remove_double_consonants(self, syllable):
        if len(syllable) == 1:
            return syllable
        double = syllable[0] + syllable[1]
        if double in self._double_consonants_set:
            syllable = self._double_consonants[double] + syllable[2:]
        return syllable

    def find_stress(self, syllable_list):
        if len(syllable_list) == 1:
            return None
            for index, syllable in enumerate(syllable_list):
                if self._irregular.search(syllable):
                    return index
            if self._grave.search(syllable_list[-1][-1]):
                return len(syllable_list) - 2
            else:
                return len(syllable_list) - 1

    def _transcription_rules(self):

        @self.rule(u"a")
        def transcribe_a(previous, next, index):
            return u'a'

        @self.rule(u"b")
        def transcribe_b(previous, next, index):
            if not previous or previous in self._nasals \
                    or previous == self._pause:
                return u'b'
            else:
                return u'β'

        @self.rule(u"c")
        def transcribe_c(previous, next, index):
            if next in [u'i', u'o']:
                return u's'  # or u'θ'
            else:
                return u'k'

        @self.rule(u"h")
        def transcribe_ch(previous, next, index):
            return u'ʧ'

        @self.rule(u"d")
        def transcribe_d(previous, next, index):
            if not previous or previous in self._nasals \
                    or previous in self._laterals or previous == self._pause:
                return u'd'
            else:
                return u'ð'

        @self.rule(u"e")
        def transcribe_e(previous, next, index):
            return u'e'

        @self.rule(u"e")
        def transcribe_stressed_e(previous, next, index):
            return u'e'

        @self.rule(u"f")
        def transcribe_f(previous, next, index):
            if next in self._voiced:
                return u'v'
            else:
                return u'f'

        @self.rule(u"g")
        def transcribe_g(previous, next, index):
            if next in [u'i', u'e']:
                return u'x'
            elif (not previous or previous in self._nasals
                    or previous == self._pause):
                return u'ɡ'
            else:
                return u'ɣ'

        @self.rule(u"h")
        def transcribe_h(previous, next, index):
            return ''

        @self.rule(u"i")
        def transcribe_i(previous, next, index):
            if next in [u'e', u'a', u'o']:
                return u'j'
            else:
                return u'i'

        @self.rule(u"i")
        def transcribe_stressed_i(previous, next, index):
            return u'i'

        @self.rule(u"j")
        def transcribe_j(previous, next, index):
            return u'x'  # this may vary based on prev, next,
                         # possibly need a uvular u'χ'

        @self.rule(u"l")
        def transcribe_l(previous, next, index):
            return u'l'  # this takes diacritics based on next

        @self.rule(u"l")
        def transcribe_ll(previous, next, index):
            if not previous or previous in self._nasals \
                    or previous in self._laterals or previous == self._pause:
                return u'ʑ'  # maybe u'ʎ'
            else:
                return u'ʝ'

        @self.rule(u"m")
        def transcribe_m(previous, next, index):
            return u'm'

        @self.rule(u"n")
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

        @self.rule(u"e")
        def transcribe_enye(previous, next, index):
            return u'ɲ'

        @self.rule(u"o")
        def transcribe_o(previous, next, index):
            return u'o'

        @self.rule(u"o")
        def transcribe_stressed_o(previous, next, index):
            return u'o'

        @self.rule(u"p")
        def transcribe_p(previous, next, index):
            return u'p'

        @self.rule(u"q")
        def transcribe_q(previous, next, index):
            return u'k'

        @self.rule(u"r")
        def transcribe_r(previous, next, index):
            if not previous or previous in [self._pause, u'l', u'n', u's']:
                return u'r'  # make an attribute maybe
            else:
                return u'ɾ'

        @self.rule(u"l")
        def transcribe_trill(previous, next, index):
            return u'r'

        @self.rule(u"s")
        def transcribe_s(previous, next, index):
            if next in self._voiced_consonants:
                return u'z'
            else:
                return u's'

        @self.rule(u"t")
        def transcribe_t(previous, next, index):
            return u't'

        @self.rule(u"u")
        def transcribe_u(previous, next, index):
            if next in [u'i', u'e', u'a']:  # att?
                return u'w'
            else:
                return u'u'

        @self.rule(u"u")
        def transcribe_stressed_u(previous, next, index):
            return u'u'

        @self.rule(u"v")
        def transcribe_v(previous, next, index):
            if not previous or previous in self._nasals \
                    or previous == self._pause:
                return u'b'
            else:
                return u'β'

        @self.rule(u"w")
        def transcribe_w(previous, next, index):
            return u'w'

        @self.rule(u"x")
        def transcribe_x(previous, next, index):
            if index == 0:
                return u'x'
            else:
                return u'ks'  # need a better sembol here...maybe

        @self.rule(u"y")
        def transcribe_y(previous, next, index):
            if previous is None and next is None:
                return u'i'
            elif not previous or previous in self._nasals \
                    or previous in self._laterals or previous == self._pause:
                return u'ʑ'  # maybe u'ʎ'
            elif previous == u'o':
                return u'i'
            else:
                return u'ʝ'

        @self.rule(u"z")
        def transcribe_z(previous, next, index):
            if next in self._voiced_consonants:
                return u'z'
            else:
                return u's'
