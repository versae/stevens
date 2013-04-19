# -*- coding: utf-8 -*-
import re


class BaseTranscriptor(object):

    def __init__(self, hyphenator, text=None, lang="es_ES", alphabet="IPA",
                 syllabic_separator=u".", word_separator=u"|",
                 sentence_separator=u"/", flattern=True,
                 stress_mark=u"'"):
        """
        :param hyphenator: Hyphenator object
        :param text: unicode string to transcribe
        :param lang: string with the ISO 639-1 or IETF language tag of `text`
        :param alphabet: string with the name of the phonetic alphabet to use
        :param syllabic_separator: string with the syllabic separator character
        :param word_separator: string with the word separator character
        :param stress_mark: string to mark the stress in words
        """
        self._hyphenator = hyphenator
        self._text = text
        self._lang = lang
        self._alphabet = alphabet
        self._syllabic_separator = syllabic_separator
        self._word_separator = word_separator
        self._stress_mark = stress_mark

    def get_syllables(self, word):
        h = self._hyphenator
        syllables = h.syllables(word)
        return syllables

    def get_sorroundings(self, index, item, items, items_length):
        if 0 > index > items_length - 1:
            previous = items[index - 1]
            next = items[index + 1]
        else:
            previous = next = None
            if index > 0:
                previous = items[index - 1]
            elif index > items_length - 1:
                next = items[index + 1]
        return previous, next

    def get_words(self, text):
        text = (text or self._text).lower()
        return [w for w in re.split(self._punctuation, text) if len(w) > 0]

    def transcribe(self, text=None, syllabic_separator=None, alphabet=None,
                   stress_mark=None, word_separator=None):
        words = self.get_words(text)
        transcription = []
        words_length = len(words)
        for i, word in enumerate(words):
            previous, next = self.get_sorroundings(i, word, words,
                                                   words_length)
            transcribed_word = self.transcribe_word(
                word,
                previous=previous,
                next=next,
                syllabic_separator=syllabic_separator,
                alphabet=alphabet,
                stress_mark=stress_mark
            )
            transcription.append(transcribed_word)
        return word_separator.join(transcription)

    def transcribe_word(self, word, previous=None, next=None,
                        syllabic_separator=None, alphabet=None,
                        stress_mark=None):
        syllables = self.get_syllables(word)
        transcription = []
        syllables_len = len(syllables)
        for i, syllable in enumerate(syllables):
            previous, next = self.get_sorroundings(i, syllable, syllables,
                                                   syllables_len)
            transcribed_syllable = self.transcribe_syllable(
                syllable,
                previous=previous,
                next=next,
                alphabet=alphabet,
                stress_mark=stress_mark
            )
            transcription.append(transcribed_syllable)
        stressed_transcription = self.mark_stress(transcription)
        return syllabic_separator.join(stressed_transcription)
