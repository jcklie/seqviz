from typing import List, Tuple

import torch


def tokenize_for_bert(text: str, tokenizer) -> Tuple[torch.Tensor, List[int]]:
    my_tokens = text.strip().split()

    grouped_inputs = []
    grouped_inputs.append(torch.LongTensor([tokenizer.cls_token_id]))

    for token in my_tokens:
        tokens = tokenizer.encode(token, return_tensors="pt", add_special_tokens=False)
        grouped_inputs.append(tokens.squeeze(axis=0))

    grouped_inputs.append(torch.LongTensor([tokenizer.sep_token_id]))

    flattened_inputs = torch.cat(grouped_inputs)
    flattened_inputs = torch.unsqueeze(flattened_inputs, 0)

    sizes = [len(group) for group in grouped_inputs]

    return flattened_inputs, sizes
