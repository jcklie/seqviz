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
        ("Alice", "B-PER"),
        ("Bob", "B-PER"),
        ("and", "O"),
        ("I", "B-PER"),
        ("ate", "O"),
        ("lasagna", "O"),
    ]

    seq = TaggedSequence.from_bio(data, fmt="iob2")
    s = str(seq)

    assert s == "Today [Alice](PER) [Bob](PER) and [I](PER) ate lasagna"


def test_from_bioes_simple():
    data = [
        ("Alex", "S-PER"),
        ("is", "O"),
        ("going", "O"),
        ("with", "O"),
        ("Marty", "B-PER"),
        ("A", "I-PER"),
        ("Rick", "E-PER"),
        ("to", "O"),
        ("Los", "B-LOC"),
        ("Angeles", "E-LOC"),
    ]

    seq = TaggedSequence.from_bio(data, fmt="bioes")
    s = str(seq)

    assert s == "[Alex](PER) is going with [Marty A Rick](PER) to [Los Angeles](LOC)"


def test_from_transformers_bio():
    text = "Hugging Face Inc. is a company based in New York City."
    groups = [1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1]
    predictions = [
        "O",
        "I-ORG",
        "I-ORG",
        "I-ORG",
        "I-ORG",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "O",
        "O",
    ]

    assert sum(groups) == len(predictions)

    seq = TaggedSequence.from_transformers_bio(text, groups, predictions)

    s = str(seq)

    assert s == "[Hugging Face Inc.](ORG) is a company based in [New York City.](LOC)"
