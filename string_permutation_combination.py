from typing import List

def string_permutations(txt: str) -> List[str]:
    permutations, sofar = [], [""]*len(txt)
    txt_signature, txt_distinct_chars = {}, []
    
    for ch in txt:
        if txt_signature.get(ch) is None:
            txt_signature[ch] = 1
            txt_distinct_chars.append(ch)
        else:
            txt_signature[ch] += 1

    def permute(level: int):
        if level == len(txt):
            permutations.append("".join(sofar))
            return
        for ch in txt_distinct_chars:
            if txt_signature[ch] == 0:
                continue
            txt_signature[ch] -= 1
            sofar[level] = ch
            permute(level+1)
            txt_signature[ch] += 1

    permute(0)
    return permutations

def string_combinations(txt: str) -> List[str]:
    combinations, sofar = [], [""]*len(txt)
    txt_signature, txt_distinct_chars = {}, []
    
    for ch in txt:
        if txt_signature.get(ch) is None:
            txt_signature[ch] = 1
            txt_distinct_chars.append(ch)
        else:
            txt_signature[ch] += 1

    def combination(index, level: int):
        combinations.append("".join(sofar[:level]))
        for i in range(index, len(txt_distinct_chars)):
            ch = txt_distinct_chars[i]
            if txt_signature[ch] == 0:
                continue
            txt_signature[ch] -= 1
            sofar[level] = ch
            combination(i, level+1)
            txt_signature[ch] += 1

    combination(0, 0)
    return combinations

if __name__ == "__main__":
    txt = "12231"
    print(string_permutations(txt))
    print(string_combinations(txt))
