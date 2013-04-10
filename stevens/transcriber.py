# -*- coding: utf-8 -*-
from hyphen import Hyphenator
from hyphen.dictools import install, is_installed
from urllib2 import HTTPError


class NotLanguageSupported(Exception):
    pass


def transcribe(text, lang="es_ES", alphabet="IPA",
               variety=None, syllabic_separator=None):
    if not syllabic_separator:
        syllabic_separator = u"."
    alphabet = alphabet.lower()
    error_message = "Unsupported language code '{}'".format(lang)
    if lang == "es_ES":
        try:
            if not is_installed(lang):
                install(lang)
        except HTTPError:
            raise NotLanguageSupported(error_message)
        return transcribe_es(text=text, syllabic_separator=syllabic_separator)
    else:
        raise NotLanguageSupported(error_message)


def transcribe_es(text, syllabic_separator=None):
    words = text.split(u" ")
    transcription = []
    for word in words:
        transcribed_word = transcribe_word_es(
            word,
            syllabic_separator=syllabic_separator
        )
        transcription.apppend(transcribed_word)
    return transcription

def transcribe_word_es(word, syllabic_separator=None):
    vowels = u"aeiouw"
    accented_vowels = u"áéíóúü"
    # consonants = u"bcdfghjklmnñpqrstvwxyz"
    invariable_constants = u"bfklmnprs"
    h = Hyphenator("es_ES")
    syllables = h.syllables(word)
    transcription = []
    for syllable in syllables:
        syllable_length = len(syllable)
        if syllable_length == 2:
            if syllable[0] in invariable_constants:
                consonant = syllable[0]
                if syllable[1] in accented_vowels:
                    vowel = vowels[accented_vowels.index(syllable[1])]
                else:
                    vowel = syllable[1]
                transcription.append(consonant)
                transcription.append(vowel)
                transcription.append(syllabic_separator)
            else:
                transcription.append(syllable[0])
                transcription.append(syllable[1])
                transcription.append(syllabic_separator)
        else:
            transcription.append(syllable)
            transcription.append(syllabic_separator)
    return "".join(transcription)

