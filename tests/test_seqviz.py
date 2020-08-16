from seqviz import TaggedSequence


def test_from_iob1_simple():
    data = [
        ("Alex", "I-PER"),
        ("is", "O"),
        ("going", "O"),
        ("to", "O"),
        ("Los", "I-LOC"),
        ("Angeles", "I-LOC"),
        ("in", "O"),
        ("California", "I-LOC"),
    ]

    seq = TaggedSequence.from_bio(data, fmt="iob1")
    s = str(seq)

    assert s == "[Alex](PER) is going to [Los Angeles](LOC) in [California](LOC)"


def test_from_iob1_adjacent():
    data = [
        ("Today", "O"),
        ("Alice", "I-PER"),
        ("Bob", "B-PER"),
        ("and", "O"),
        ("I", "B-PER"),
        ("ate", "O"),
        ("lasagna", "O"),
    ]

    seq = TaggedSequence.from_bio(data, fmt="iob1")
    s = str(seq)

    assert s == "Today [Alice](PER) [Bob](PER) and [I](PER) ate lasagna"


def test_from_iob2_simple():
    data = [
        ("Alex", "B-PER"),
        ("is", "O"),
        ("going", "O"),
        ("to", "O"),
        ("Los", "B-LOC"),
        ("Angeles", "I-LOC"),
        ("in", "O"),
        ("California", "B-LOC"),
    ]

    seq = TaggedSequence.from_bio(data, fmt="iob2")
    s = str(seq)

    assert s == "[Alex](PER) is going to [Los Angeles](LOC) in [California](LOC)"


def test_from_iob2_adjacent():
    data = [
        ("Today", "O"),
        ("Alice", "I-PER"),
        ("Bob", "B-PER"),
        ("and", "O"),
        ("I", "B-PER"),
        ("ate", "O"),
        ("lasagna", "O"),
    ]

    seq = TaggedSequence.from_bio(data, fmt="iob2")
    s = str(seq)

    assert s == "Today [Alice](PER) [Bob](PER) and [I](PER) ate lasagna"


def test_from_bert():
    text = "Hugging Face is a French company based in New York."
    predictions = [
        {"word": "Hu", "score": 0.9968873858451843, "entity": "I-ORG", "index": 1},
        {"word": "##gging", "score": 0.9329524040222168, "entity": "I-ORG", "index": 2},
        {"word": "Face", "score": 0.9781811237335205, "entity": "I-ORG", "index": 3},
        {"word": "French", "score": 0.9981815814971924, "entity": "I-MISC", "index": 6},
        {"word": "New", "score": 0.9987512826919556, "entity": "I-LOC", "index": 10},
        {"word": "York", "score": 0.9976728558540344, "entity": "I-LOC", "index": 11},
    ]
