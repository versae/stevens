stevens
=======

Stevens, the assistant phonetician


Getting Started
---------------

```python
>>> from stevens import transcribe
>>> transcribe(u"Hola, qué tal", lang="es_ES")

>>> from stevens import get_transcriptor

>>> CastillianSpanishTranscriptor = get_transcriptor("es_ES")
>>> tr = CastillianSpanishTranscriptor(u"Hola, qué tal")

>>> from stevens.languages.es.castillian import Transcriptor
>>> tr = castillian.Transcriptor(u"Buenos días")
>>> tr.transcribe()
```

