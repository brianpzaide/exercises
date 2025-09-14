import pathlib
from collections import deque, namedtuple
from typing import NamedTuple

ELBOW = "└── "
TEE = "├── "
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

class TreeItem(NamedTuple):
    root: pathlib.Path
    indent: str
    prefix: str

def tree_recursive(root: pathlib.Path, indent, prefix: str):
    print(f"{prefix}{root.name}")
    if not root.is_dir():
        return
    fis = sorted([fi.name for fi in root.iterdir() if not fi.name.startswith(".")])
    for i, fi in enumerate(fis):
        add_ = PIPE_PREFIX
        if i == len(fis)-1:
            prefix_ = indent + ELBOW
            add_ = SPACE_PREFIX
        else:
            prefix_ = indent + TEE
        tree_recursive(root.joinpath(fi), indent+add_, prefix_)

def tree_iterative(root: pathlib.Path):
    q = deque()
    q.append(TreeItem(root, "", ""))
    while len(q) != 0:
        ti: TreeItem = q.pop()
        print(f"{ti.prefix}{ti.root.name}")
        if not ti.root.is_dir():
            continue
        fis = sorted([fi.name for fi in ti.root.iterdir() if not fi.name.startswith(".")])
        children_tis = []
        for i, fi in enumerate(fis):
            add_ = PIPE_PREFIX
            if i == len(fis)-1:
                prefix_ = ti.indent + ELBOW
                add_ = SPACE_PREFIX
            else:
                prefix_ = ti.indent + TEE
            children_tis.append(TreeItem(ti.root.joinpath(fi), ti.indent + add_, prefix_))
        q.extend(children_tis[-1::-1])



if __name__ == "__main__":
    root = "."
    user_input = input().strip()
    if user_input == "" or user_input == ".":
        root = pathlib.Path.cwd()

    print("=====Recursive=====")
    tree_recursive(root, "", "")
    print()
    print("=====Iterative=====")
    tree_iterative(root)