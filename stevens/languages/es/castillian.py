# -*- coding: utf-8 -*-
import re

from stevens.languages import BaseTranscriptor


class Transcriptor(BaseTranscriptor):

    def __init__(self, *args, **kwargs):
        super(Transcriptor, self).__init__(*args, **kwargs)
        self._punctuation = re.compile(r"[ \.,\?\!¡¿\n\t\s]+")

    def transcribe_syllable(self, syllable, previous=None, next=None,
                            alphabet=None, stress_mark=None):
        return syllable

    def mark_stress(self, syllable_list, stress_mark=None):
        return syllable_list
