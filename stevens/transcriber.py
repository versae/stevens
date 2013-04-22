# -*- coding: utf-8 -*-
from importlib import import_module
from urllib2 import HTTPError

try:
    import langid
except ImportError:
    langid = None
from hyphen import Hyphenator
from hyphen.dictools import install, is_installed


class NotLanguageSupported(Exception):
    pass


def get_transcriptor(lang="es_ES", alphabet="IPA",
                     syllabic_separator=u".", stress_mark=u"'",
                     word_separator=u"|"):
    """
    Return a `Transcriptor` object

    :param lang: string with the ISO 639-1 code or IETF language tag of `text`
    :param alphabet: string with the name of the phonetic alphabet to use
    :param syllabic_separator: string with the syllabic separator character
    :param stress_mark: string to mark the stress in words
    :param word_separator: string with the word separator character
    :return: a `Transcriptor` object
    """
    if not syllabic_separator:
        syllabic_separator = u"."
    alphabet = alphabet.lower()
    # Language identification
    error_message = "Unsupported language code '{}'".format(lang)
    if lang.lower() in ("es", "es_es"):
        lang = "es_ES"
        try:
            hyphenator = Hyphenator(lang)
        except IOError:
            try:
                if not is_installed(lang):
                    install(lang)
                    hyphenator = Hyphenator(lang)
            except HTTPError:
                raise NotLanguageSupported(error_message)
        module = import_module("stevens.languages.es.castillian")
        transcriptor = module.Transcriptor(
            hyphenator=hyphenator,
            syllabic_separator=syllabic_separator,
            word_separator=word_separator,
            alphabet=alphabet,
            stress_mark=stress_mark,
        )
        return transcriptor
    else:
        raise NotLanguageSupported(error_message)


def transcribe(text, lang="es_ES", alphabet="IPA",
               syllabic_separator=u".", stress_mark=u"'", word_separator=u"|",
               auto_lang=False):
    """
    Get the phonetic transcription of `text`

    :param text: unicode string to transcribe
    :param lang: string with the ISO 639-1 code or IETF language tag of `text`
    :param alphabet: string with the name of the phonetic alphabet to use
    :param syllabic_separator: string with the syllabic separator character
    :param stress_mark: string to mark the stress in words
    :param word_separator: string with the word separator character
    :param auto_lang: boolean to perform an automatic language identification
    :return: string with the phonetic transcription of `text`
    """
    if auto_lang:
        if not langid:
            raise ImportError("Please, install langid")
        lang = langid.classify(text)[0]
    transcriptor = get_transcriptor(
        lang=lang,
        alphabet=alphabet,
        syllabic_separator=syllabic_separator,
        word_separator=word_separator,
        stress_mark=stress_mark)
    return transcriptor.transcribe(
        text=text,
        syllabic_separator=syllabic_separator,
        word_separator=word_separator,
        alphabet=alphabet,
        stress_mark=stress_mark,
    )
