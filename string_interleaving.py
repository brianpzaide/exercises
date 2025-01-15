from typing import List


def interleave_strings(a: str, b: str) -> List[str]:
    interleaved_strings = []
    
    def _interleave_strings(a_index:int, b_index: int, sofar: str):
        if a_index == len(a):
            interleaved_strings.append(sofar + b[b_index:])
            return
        
        if b_index == len(b):
            interleaved_strings.append(sofar + a[a_index:])
            return
        
        _interleave_strings(a_index+1, b_index, sofar + a[a_index])
        _interleave_strings(a_index, b_index+1, sofar + b[b_index])
    
    _interleave_strings(0, 0, "")
    return interleaved_strings
    

def is_interleaved(a: str, b: str, c: str) -> bool:
    a_len = len(a)
    b_len = len(b)

    if a_len + b_len != len(c):
        return False
    
    T = [[False for _ in range(a_len + 1)] for _ in range(b_len + 1)]
        
    for row in range(b_len+1):
        for col in range(a_len+1):
            if col == 0 and row == 0:
                T[row][col] = True
            elif col == 0:
                T[row][col] = T[row-1][col] if b[row-1] == c[row-1] else False
            elif row == 0:
                T[row][col] = T[row][col-1] if a[col-1] == c[col-1] else False
            elif c[row + col-1] == a[col-1] and c[row + col-1] != b[row-1]:
                T[row][col] = T[row][col-1]
            elif c[row + col-1] == b[row-1] and c[row + col-1] != a[col-1]:
                T[row][col] = T[row-1][col]
            elif c[row + col-1] == b[row-1] and c[row + col-1] == a[col-1]:
                T[row][col] = T[row][col-1] or T[row-1][col]
    
    return T[-1]

def main():
    s1 = "abcd"
    s2 = "12345"
    interleaved_strings: List[str] = interleave_strings(s1, s2)

    all_passed = True

    for test_str in interleaved_strings:
        if not is_interleaved(s1, s2, test_str):
            all_passed = False
            print(f"{test_str} is not interleaving of {s1} and {s2}")
        # else:
        #     print(f"{test_str} is interleaving of {s1} and {s2}")
    
    if all_passed:
        print(f"Successfully interleaved strings {s1} and {s2}. Got {len(interleaved_strings)} interleaved strings")


if __name__ == '__main__':
    main()