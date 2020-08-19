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
    def from_bio(seq: List[Tuple[str, str]], fmt="iob2") -> "TaggedSequence":
        if fmt == "iob1":
            labels = TaggedSequence._iob1_to_iob2([s[1] for s in seq])
        elif fmt == "iob2" or fmt == "bioes":
            labels = [s[1] for s in seq]
        else:
            raise ValueError(f"Invalid tagging scheme: {fmt}")

        tokens = [s[0] for s in seq]
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

    @staticmethod
    def _iob1_to_iob2(tags: List[str]) -> List[str]:
        """
        Check that tags have a valid IOB format.
        Tags in IOB1 format are converted to IOB2.
        """
        # https://gist.github.com/allanj/b9bd448dc9b70d71eb7c2b6dd33fe4ef

        result = []
        for i, tag in enumerate(tags):
            if tag == "O":
                result.append("O")
                continue

            split = tag.split("-")
            if len(split) != 2 or split[0] not in ["I", "B"]:
                raise ValueError("Invalid IOB1 sequence")

            if split[0] == "B":
                result.append(tag)
            elif i == 0 or tags[i - 1] == "O":
                result.append("B" + tag[1:])
            elif tags[i - 1][1:] == tag[1:]:
                result.append(tag)
            else:
                result.append("B" + tag[1:])

        return result

    @staticmethod
    def from_bert(seq: List[Tuple[str, str]]) -> "TaggedSequence":
        pass

    @staticmethod
    def from_conll(s: str) -> "Tagger":
        pass

    def __str__(self) -> str:
        result = ""
        offset = 0
        for annotation in self._annotations:
            start = annotation.start
            end = annotation.end

            result += self._text[offset:start]
            result += f"[{self._text[start:end]}]({annotation.tag})"
            offset = end

        result += self._text[offset:]
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
            style = f"color:rgb({r}, {g}, {b})"

            ruby = f'<ruby style="{style}"> {s} <rp>(</rp><rt>{tag}</rt><rp>)</rp> </ruby>'
            span = f'<span style="outline: 1px dotted grey;">{ruby}</span>'
            result += span
            offset = end

        result += self._text[offset:]

        return f'<div style="font-size: 24px;">{result}</div>'
