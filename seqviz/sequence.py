from collections import namedtuple
from typing import List, Tuple

import matplotlib
from matplotlib import cm

from seqviz.seqeval import get_entities

Annotation = namedtuple("Annotation", ["start", "end", "tag"])


class TaggedSequence:
    def __init__(self, text: str, annotations: List[Annotation] = None):
        self._text: str = text
        self._annotations: List[Annotation] = annotations if annotations else []

    @staticmethod
    def from_bio(seq: List[Tuple[str, str]]) -> "TaggedSequence":
        tokens = [s[0] for s in seq]
        labels = [s[1] for s in seq]
        text = " ".join(tokens)

        start_offsets = []
        end_offsets = []

        offset = 0
        for token in tokens:
            start_offsets.append(offset)
            offset += len(token)
            end_offsets.append(offset)
            offset += 1

        annotations = []
        for tag, start_idx, end_idx in get_entities(labels):
            start_offset = start_offsets[start_idx]
            end_offset = end_offsets[end_idx]

            annotation = Annotation(start_offset, end_offset, tag)
            annotations.append(annotation)

        return TaggedSequence(text, annotations)

    def __str__(self) -> str:
        result = ""
        offset = 0
        for annotation in self._annotations:
            start = annotation.start
            end = annotation.end

            result += self._text[offset:start]
            result += f"[{self._text[start:end]}]({annotation.tag})"
            offset = end

        return result

    def __repr__(self) -> str:
        return str(self)

    def _repr_html_(self):
        result = ""
        offset = 0

        tags = list(set(a.tag for a in self._annotations))
        tags_to_idx = {tag: idx for idx, tag in enumerate(sorted(tags))}

        norm = matplotlib.colors.Normalize(vmin=0, vmax=len(tags) - 1)
        cmap = matplotlib.cm.get_cmap("Set1")

        for annotation in self._annotations:
            start = annotation.start
            end = annotation.end

            result += self._text[offset:start]
            s = self._text[start:end]
            tag = annotation.tag

            rgba = cmap(norm(tags_to_idx[tag]))
            r = int(rgba[0] * 255)
            g = int(rgba[1] * 255)
            b = int(rgba[2] * 255)
            style = f"color:rgb({r}, {g}, {b});"

            ruby = f'<ruby style="{style}"> {s} <rp>(</rp><rt>{tag}</rt><rp>)</rp> </ruby>'
            span = f'<span style="  outline: 1px dotted green;">{ruby}</span>'
            result += span
            offset = end

        return f"<div>{result}</div>"


def main():
    iob2 = """
    Alex B-PER
    is O
    going O
    to O
    get O
    rich O
    by O
    shorting O
    Tesla B-ORG
    stocks O
    """
    iob2 = """
    Mr. B-NP
    Meador I-NP
    had B-VP
    been I-VP
    executive B-NP
    vice I-NP
    president I-NP
    of B-PP
    Balcor B-NP
    """
    seq = [tuple(s.strip().split(" ")) for s in iob2.split("\n") if s.strip()]

    tagged = TaggedSequence.from_bio(seq)

    print(tagged)
    print(tagged._repr_html_())

    cmap = matplotlib.cm.get_cmap("Spectral")


if __name__ == "__main__":
    main()
