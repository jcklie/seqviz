# seqviz

**seqviz** (sequence visualization) is a Python package to visualize sequence tagging results. It can be either be used
to print to console or in Jupyter Notebooks.

## Usage

You can load tagged sentences from many common formats:

**iob1**

```python
from seqviz import TaggedSequence

data = [
    ('Alex', 'I-PER'),
    ('is', 'O'),
    ('going', 'O'),
    ('to', 'O'),
    ('Los', 'I-LOC'),
    ('Angeles', 'I-LOC'),
    ('in', 'O'),
    ('California', 'I-LOC')
]

tagged = TaggedSequence.from_bio(data, fmt="iob1")

print(tagged) # [Alex](PER) is going to [Los Angeles](LOC) in [California](LOC)
```

**iob2**

```python
from seqviz import TaggedSequence

data = [
    ("Today", "O"),
    ("Alice", "B-PER"),
    ("Bob", "B-PER"),
    ("and", "O"),
    ("I", "B-PER"),
    ("ate", "O"),
    ("lasagna", "O"),
]

tagged = TaggedSequence.from_bio(data, fmt="iob1")

print(tagged) # Today [Alice](PER) [Bob](PER) and [I](PER) ate lasagna
```

**BIOES**

```python
from seqviz import TaggedSequence

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
    ("Angeles", "E-LOC")
]

tagged = TaggedSequence.from_bio(data, fmt="bioes")

print(tagged) # "[Alex](PER) is going with [Marty A Rick](PER) to [Los Angeles](LOC)"
```

## Jupyter Notebook integration

You can also use `TaggedSequence` in an Jupyter notebook:

## Integration with other NLP frameworks

*seqviz* can be used to visualize sequences from many different popular NLP frameworks.

### Hugging Face Transformers

```python
from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch

from seqviz import TaggedSequence, fix_bert_subtokenization

model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

label_list = [
    "O",       # Outside of a named entity
    "B-MISC",  # Beginning of a miscellaneous entity right after another miscellaneous entity
    "I-MISC",  # Miscellaneous entity
    "B-PER",   # Beginning of a person's name right after another person's name
    "I-PER",   # Person's name
    "B-ORG",   # Beginning of an organisation right after another organisation
    "I-ORG",   # Organisation
    "B-LOC",   # Beginning of a location right after another location
    "I-LOC"    # Location
]

text = "Hugging Face Inc. is a company based in New York City. Its headquarters are in DUMBO, therefore very" \
           "close to the Manhattan Bridge."

# Bit of a hack to get the tokens with the special tokens
tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))
inputs = tokenizer.encode(text, return_tensors="pt")

outputs = model(inputs)[0]
predictions = torch.argmax(outputs, dim=2)

data = [(token, label_list[prediction]) for token, prediction in zip(tokens, predictions[0].tolist())]

fixed_data = fix_bert_subtokenization(text, data)

seq = TaggedSequence.from_bio(fixed_data, fmt="iob1")
```

<div style="font-size: 24px;"><span style="outline: 1px dotted grey;"><ruby style="color:rgb(153, 153, 153)"> Hugging Face Inc <rp>(</rp><rt>ORG</rt><rp>)</rp> </ruby></span> . is a company based in <span style="outline: 1px dotted grey;"><ruby style="color:rgb(228, 26, 28)"> New York City <rp>(</rp><rt>LOC</rt><rp>)</rp> </ruby></span> . Its headquarters are in <span style="outline: 1px dotted grey;"><ruby style="color:rgb(228, 26, 28)"> DUMBO <rp>(</rp><rt>LOC</rt><rp>)</rp> </ruby></span> , therefore very close to the <span style="outline: 1px dotted grey;"><ruby style="color:rgb(228, 26, 28)"> Manhattan Bridge <rp>(</rp><rt>LOC</rt><rp>)</rp> </ruby></span> .</div>
