# -*- coding: utf-8 -*-
import re

from stevens.languages import BaseTranscriptor
from stevens.hyphenation import get_hyphenator


class Transcriptor(BaseTranscriptor):

    def __init__(self, *args, **kwargs):
        super(Transcriptor, self).__init__(*args, **kwargs)
        if not self._hyphenator:
            self._hyphenator = get_hyphenator("es_ES")
        self._punctuation = re.compile(r"[ \.,\?\!¡¿\n\t\s]+")
        self._grave = re.compile(u'[aeiouns]')
        self._irregular = re.compile(u'[áéíóú]')

    def transcribe_syllable(self, syllable, previous=None, next=None,
                            alphabet=None, stress_mark=None):
        return syllable

    def mark_stress(self, syllable_list, stress_mark=None):
        stress_mark = stress_mark or self._stress_mark
        if len(syllable_list) > 1:
            irreg_stress = False
            for index, syllable in enumerate(syllable_list):
                if self._irregular.search(syllable):
                    syllable_list[index] = stress_mark + syllable
                    irreg_stress = True
                    break
            if irreg_stress is False:
                if self._grave.search(syllable_list[-1][-1]):
                    syllable_list[-2] = stress_mark + syllable_list[-2]
                else:
                    syllable_list[-1] = stress_mark + syllable_list[-1]
        return syllable_list
