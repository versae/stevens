# -*- coding: utf-8 -*-


class NotLanguageSupported(Exception):

    def __init__(self, lang):
        message = "Unsupported language code '{}'".format(lang)
        super(NotLanguageSupported, self).__init__(message)
