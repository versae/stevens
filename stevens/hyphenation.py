# -*- coding: utf-8 -*-
from urllib2 import HTTPError

from hyphen import Hyphenator
from hyphen.dictools import install, is_installed

from stevens.exceptions import NotLanguageSupported


def get_hyphenator(lang):
    try:
        hyphenator = Hyphenator(lang)
    except IOError:
        try:
            if not is_installed(lang):
                install(lang)
                hyphenator = Hyphenator(lang)
        except HTTPError:
            raise NotLanguageSupported(lang)
    return hyphenator
