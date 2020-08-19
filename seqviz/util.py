from typing import List, Tuple


def fix_bert_subtokenization(text: str, seq: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    chars = list(text)
    fixed_tokens = []
    fixed_tags = []

    is_whitespace = False

    for token, tag in seq[1:-1]:
        is_subword = token.startswith("##")
        token = token.replace("##", "")

        for c in token:
            removed = chars.pop(0)
            assert removed == c, f"[{removed}] != [{c}]"

        if is_subword and not is_whitespace:
            fixed_tokens[-1] += token
        else:
            fixed_tokens.append(token)
            fixed_tags.append(tag)

        if chars and chars[0] == " ":
            chars.pop(0)
            is_whitespace = True
        else:
            is_whitespace = False

    assert len(fixed_tokens) == len(fixed_tags)
    return [(token, tag) for token, tag in zip(fixed_tokens, fixed_tags)]
