stevens
=======

Stevens, the assistant phonetician


Getting Started
---------------

```python
>>> from stevens import transcriber
>>> transcriber(u"Hola, qué tal", lang="es_ES")

>>> from stevens import get_transcriptor

>>> EsTranscriptor = get_transcriptor("es_ES")
>>> obj = EsTranscriptor(u"Hola, qué tal")

>>> obj.get_syllables()
```

