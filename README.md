# seqviz

**seqviz** (sequence visualization) is a Python package to
visualize sequence tagging results.

## Usage

```python
from seqviz import TaggedSequence

bio = [('Alex', 'I-PER'),
 ('is', 'O'),
 ('going', 'O'),
 ('to', 'O'),
 ('Los', 'I-LOC'),
 ('Angeles', 'I-LOC'),
 ('in', 'O'),
 ('California', 'I-LOC')]

tagged = TaggedSequence.from_bio(bio)

print(tagged)
```

In the terminal, this prints

    [Alex](PER) is going to [Los Angeles](LOC) in [California](LOC)

You can also use it in an Jupyter notebook which gives

<div><span style="  outline: 1px dotted green;"><ruby style="color:rgb(153, 153, 153);"> Alex <rp>(</rp><rt>PER</rt><rp>)</rp> </ruby></span> is going to <span style="  outline: 1px dotted green;"><ruby style="color:rgb(228, 26, 28);"> Los Angeles <rp>(</rp><rt>LOC</rt><rp>)</rp> </ruby></span> in <span style="  outline: 1px dotted green;"><ruby style="color:rgb(228, 26, 28);"> California <rp>(</rp><rt>LOC</rt><rp>)</rp> </ruby></span></div>

