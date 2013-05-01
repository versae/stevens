#/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import unittest

from stevens.languages.es import castillian


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
)


class SpanishTestCase(unittest.TestCase):

    def test_import_castillian(self):
        text = u"Esto es una prueba"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.transcribe(text)
        self.assertEqual(transcribed_text, u"ˈes.to|es|ˈu.na|ˈpɾwe.βa")

    def test_replace_ll(self):
        syllable = u"lla"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.remove_double_consonants(syllable)
        self.assertEqual(transcribed_text, u"ʎa")

    def test_replace_rr(self):
        syllable = u"rro"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.remove_double_consonants(syllable)
        self.assertEqual(transcribed_text, u"Ro")

    def test_replace_gu(self):
        syllable = u"gue"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.remove_double_consonants(syllable)
        self.assertEqual(transcribed_text, u"ge")

    def test_replace_qu(self):
        syllable = u"que"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.remove_double_consonants(syllable)
        self.assertEqual(transcribed_text, u"ke")

    def test_replace_ch(self):
        syllable = u"cha"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.remove_double_consonants(syllable)
        self.assertEqual(transcribed_text, u"ʧa")

    def test_transcribe_syllable(self):
        text = u"bue"
        previous = u"una"
        next = u"na"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.transcribe_syllable(text,previous,next)
        self.assertEqual(transcribed_text, u"βwe")

    def test_transcribe_syllable(self):
        text = u"hi"
        previous = u"un"
        next = u"lo"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.transcribe_syllable(text,previous,next)
        self.assertEqual(transcribed_text, u"i")

    def test_find_stress(self):
        text = u"página"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.find_stress(text)
        self.assertEqual(transcribed_text, 0)

    def test_find_stress(self):
        text = u"ojalá"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.find_stress(text)
        self.assertEqual(transcribed_text, 2)

    def test_find_stress(self):
        text = u"problema"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.find_stress(text)
        self.assertEqual(transcribed_text, 1)

    def test_find_stress(self):
        text = u"verdad"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.find_stress(text)
        self.assertEqual(transcribed_text, 1)

    def test_find_stress(self):
        text = u"conectividad"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.find_stress(text)
        self.assertEqual(transcribed_text, 4)


if __name__ == '__main__':
    unittest.main()
