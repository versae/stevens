stevens
=======

Stevens, the assistant phonetician


Getting Started
---------------

```python
>>> from stevens import transcribe
>>> transcribe(u"Hola, qué tal", lang="es_ES")
```

Using the auto discovering language feature::

```python
>>>  transcribe(u"Hola, muy buenos días")
```

Getting a `Transcriptor` object::
```python
>>> from stevens import get_transcriptor

>>> castillian_transcriptor = get_transcriptor("es_ES")
>>> castillian_transcriptor.transcribe(u"Hola, qué tal")
```

Or getting the `Transcriptor` class::

```python
>>> from stevens.languages.es import castillian
>>> tr = castillian.Transcriptor(u"Buenos días")
>>> tr.transcribe()
```

