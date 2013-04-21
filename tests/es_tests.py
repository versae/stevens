#/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import unittest

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
)


class SpanishTestCase(unittest.TestCase):

    def test_import_castillian(self):
        from importlib import import_module
        castillian = import_module("stevens.languages.es.castillian")
        text = u"Esto es una prueba"
        transcriptor = castillian.Transcriptor()
        transcribed_text = transcriptor.transcribe(text)
        self.assertEqual(transcribed_text, u"ˈes.to|es|ˈuna|ˈprue.ba")


if __name__ == '__main__':
    unittest.main()
