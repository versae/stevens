# -*- coding: utf-8 -*-
import re

from stevens.languages import BaseTranscriptor


class Transcriptor(BaseTranscriptor):

    def __init__(self, *args, **kwargs):
        super(Transcriptor, self).__init__(*args, **kwargs)
        self._punctuation = re.compile(r"[ \.,\?\!¡¿\n\t\s]+")
        self._grave = re.compile(u'[aeiouns]')
        self._irregular = re.compile(u'[áéíóú]')
        self._stress_mark = u"ˈ"

    def transcribe_syllable(self, syllable, previous=None, next=None,
                            alphabet=None, stress_mark=None):
        return syllable

    def mark_stress(self, syllable_list, stress_mark=u"ˈ"):
        if len(syllable_list) > 1:
            irreg_stress = False
            for ndx,syl in enumerate(syllable_list):
                if self._irregular.search(syl):
                    syllable_list[ndx] = self._stress_mark + syl
                    irreg_stress = True
                    break
            if irreg_stress == False:
                if self._grave.search(syllable_list[-1][-1]):
                    syllable_list[-2] = self._stress_mark + syllable_list[-2]
                else:
                    syllable_list[-1] = self._stress_mark + syllable_list[-1]
        return syllable_list


