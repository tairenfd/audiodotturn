audiodotturn package basic usage
=======================

EXTRACTING AND CONSTRUCTING
---------------------------

```py
    import audiodotturn

    file = 'turn (ft. tester) "long john" ft. me, turner.wav'

    files = [
        'turn (ft. tester) "long john" ft. me, turner.wav',
        'YG Feat. Dj Mustard "Pop It, Shake It" (Uncut) (WSHH Exclusive - Official Music Video) [kQ2KSPz4iSw].wav',
        'Lady Gaga, Ariana Grande - Rain On Me (Official Music Video) [AOm9Fv8NTG0].mp3'
    ]

    audiodotturn = audiodotturn.AudioDotTurn()
    extraction = audiodotturn.extract_file(file)
    extractions = audiodotturn.extract_files(files)

    for extract in extraction:
        print('extraction single:\n', extract, '\n')

    for extract in extractions:
        print('extraction:\n', extract, '\n')

    constructions = audiodotturn.construct("enclosed", extraction, auto=False)
    auto_constructions = audiodotturn.construct("simple", extractions, auto=True)

    print(constructions, '\n')
    print(auto_constructions, '\n')
```

EXTRACTION IN DESIRED FORMAT
----------------------------

```py
    from rich.pretty import pprint
    import audiodotturn

    file = 'turn (ft. tester) "long john" ft. me, turner.wav'

    adt_runner = audiodotturn.AudioDotTurn()
    adt_runner.extract_file(file)

    _dict = adt_runner.extractor.get_extraction("dict")
    _yaml = adt_runner.extractor.get_extraction("yaml")
    _str = adt_runner.extractor.get_extraction("str")
    _values = adt_runner.extractor.get_extraction("values")
```

UPDATING DATABASE
-----------------

```py
    from rich.pretty import pprint
    from rich.console import Console
    import audiodotturn

    console = Console()

    file = 'turn (ft. tester) "long john" ft. me, turner.wav'

    adt_runner = audiodotturn.AudioDotTurn()
    extraction = adt_runner.extract_file(file)

    adt_runner.update_database(extraction)

    artists = adt_runner.get_all_artists()

    for artist in artists:
        print(artist["artist_id"])
        print(artist["name"])

    # The above produces:
    #
    # 1
    # turn
```
