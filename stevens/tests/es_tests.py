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


if __name__ == '__main__':
    unittest.main()
