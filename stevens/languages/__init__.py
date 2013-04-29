# -*- coding: utf-8 -*-
import re


class BaseTranscriptor(object):

    def __init__(self, text=None, hyphenator=None, lang="es_ES",
                 alphabet="IPA", syllabic_separator=u".", word_separator=u"|",
                 phrase_separator=u"/", flattern=True,
                 stress_mark=u"'"):
        """
        :param text: unicode string to transcribe
        :param hyphenator: Hyphenator object
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
        self._phrase_separator = phrase_separator
        self._rules = {}
        self._transcription_rules()

    def rule(self, chunk):
        """Decorator that associates a function to a chunk to apply on"""
        def wrapper(fn):
            self.rules[chunk] = fn
        return wrapper

    def _get_rules(self):
        return self._rules
    rules = property(fget=_get_rules)

    def get_syllables(self, word):
        h = self._hyphenator
        syllables = h.syllables(word)
        return syllables

    def get_surroundings(self, index, item, items, items_length):
        if 0 < index < items_length - 1:
            previous = items[index - 1]
            next = items[index + 1]
        else:
            previous = next = None
            if index > 0:
                previous = items[index - 1]
            elif index < items_length - 1:
                next = items[index + 1]
        return previous, next

    def get_phrases(self, text):
        text = (text or self._text).lower()
        return [w for w in re.split(self._punctuation, text) if len(w) > 0]

    def get_words(self, phrase):
        return phrase.split()

    def transcribe(self, text=None, syllabic_separator=None, alphabet=None,
                   stress_mark=None, word_separator=None,
                   phrase_separator=None):
        phrases = self.get_phrases(text)
        transcription = []
        phrases_length = len(phrases)
        for i, phrase in enumerate(phrases):
            previous, next = self.get_surroundings(i, phrase, phrases,
                                                   phrases_length)
            transcribed_phrase = self.transcribe_phrase(
                phrase,
                previous=previous,
                next=next,
                syllabic_separator=syllabic_separator,
                alphabet=alphabet,
                stress_mark=stress_mark
            )
            transcription.append(transcribed_phrase)
        return self._phrase_separator.join(transcription)

    def transcribe_phrase(self, phrase, previous=None, next=None,
                          syllabic_separator=None, alphabet=None,
                          word_separator=None, stress_mark=None):
        words = self.get_words(phrase)
        transcription = []
        words_length = len(words)
        for i, word in enumerate(words):
            previous, next = self.get_surroundings(i, word, words,
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
        return self._word_separator.join(transcription)

    def transcribe_word(self, word, previous=None, next=None,
                        syllabic_separator=None, alphabet=None,
                        stress_mark=None):
        syllables = self.get_syllables(word)
        transcription = []
        syllables_len = len(syllables)
        for i, syllable in enumerate(syllables):
            previous, next = self.get_surroundings(i, syllable, syllables,
                                                   syllables_len)
            transcribed_syllable = self.transcribe_syllable(
                syllable,
                previous=previous,
                next=next,
                alphabet=alphabet,
                stress_mark=stress_mark
            )
            transcription.append(transcribed_syllable)
        stress_index = self.find_stress(transcription)
        if stress_index:
            transcription[stress_index] = \
                stress_mark + transcription[stress_index]
        return self._syllabic_separator.join(transcription)
