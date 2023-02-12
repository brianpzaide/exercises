# write your code here
import re
import os
import sys
import ast
from collections import defaultdict, OrderedDict, namedtuple


def check_length_err(line: str) -> bool:
    return len(line) > 79


def check_indentation_err(line: str) -> bool:
    return (len(line) - len(line.lstrip())) % 4 != 0


def check_semicolon_err(line: str) -> bool:
    if "#" in line:
        pieces = line.split("#")
        if len(pieces) >= 2:
            if pieces[0].strip():
                return pieces[0].strip()[-1] == ";"
            return False
        return False
    else:
        return line[-1] == ";"


def check_inline_comments_spaces_err(line: str) -> bool:
    pieces = line.split("#")
    if len(pieces) >= 2:
        if pieces[0].strip():
            l = len(pieces[0])
            return pieces[0][l - 2:l] != "  "
        return False
    return False


def check_todo_err(line):
    p = re.compile(".*# [Tt][Oo][Dd][Oo]")
    return p.match(line.lstrip()) is not None


def check_construction_name_space_err(line, line_no) -> str:
    line = line.strip()
    if line.startswith("class  "):
        return f"Line {line_no}: S{7:03d} Too many spaces after 'class'"
    if line.startswith("def  "):
        return f"Line {line_no}: S{7:03d} Too many spaces after 'def'"


def check_snake_case(name):
    for l in name:
        if l.isupper():
            return True
    return False


def check_camel_case(name):
    return True if (name[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ") or ("_" in name) else False


def check_name_format(name, line_no, err_no):
    if err_no == 8:
        if check_camel_case(name):
            return f"Line {line_no}: S{err_no:03d} Class name {name} should be written in CamelCase"
        return None
    if err_no == 9:
        if check_snake_case(name):
            return f"Line {line_no}: S{err_no:03d} Function name {name} should be written in snake_case"
        return None
    if err_no == 10:
        if check_snake_case(name):
            return f"Line {line_no}: S{err_no:03d} Argument name {name} should be snake_case"
        return None
    if err_no == 11:
        if check_snake_case(name):
            return f"Line {line_no}: S{err_no:03d} Argument name {name} should be snake_case"
        return None


def check_functions_err(file_name):
    ArgLineno = namedtuple("ArgLineno", ["arg_name", "line_no"])
    m_errs = defaultdict(list)
    args_name: list[ArgLineno] = []
    src = ""
    with open(file_name) as f:
        src = str(f.read())
    tree = ast.parse(src)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            line_no = node.lineno
            function_name = node.name
            # checking if function name is snake_case
            if err := check_name_format(function_name, line_no, 9):
                m_errs[line_no].append(err)

            # checking if arguments' names are snake_case
            args_name.extend([ArgLineno(arg.arg, arg.lineno) for arg in node.args.args])
            args_name.extend([ArgLineno(arg.arg, arg.lineno) for arg in node.args.posonlyargs])
            args_name.extend([ArgLineno(arg.arg, arg.lineno) for arg in node.args.kwonlyargs])
            if node.args.vararg:
                args_name.append(ArgLineno(node.args.vararg.arg, node.args.vararg.lineno))
            if node.args.kwarg:
                args_name.append(ArgLineno(node.args.kwarg.arg, node.args.kwarg.lineno))
            args_name.sort(key=lambda a: a.line_no)

            # checking if any argument is mutable
            default_values = []
            default_values.extend([df.lineno for df in node.args.defaults if
                                   isinstance(df, ast.List) or isinstance(df, ast.Set) or isinstance(df, ast.Dict)])
            default_values.extend([df.lineno for df in node.args.kw_defaults if
                                   isinstance(df, ast.List) or isinstance(df, ast.Set) or isinstance(df, ast.Dict)])
            default_values.sort()
            for d in default_values:
                err = f"Line {d}: S{12:03d} Default argument value is mutable"
                m_errs[line_no].append(err)
                break

            body = node.body
            for el in body:
                if isinstance(el, ast.Assign):
                    for t in el.targets:
                        if isinstance(t, ast.Name):
                            if err := check_name_format(t.id, t.lineno, 11):
                                m_errs[t.lineno].append(err)
    for al in args_name:
        if err := check_name_format(al.arg_name, al.line_no, 10):
            m_errs[al.line_no].append(err)
            break

    return m_errs


def check_classes_err(file_name):
    m_errs = defaultdict(list)
    src = ""
    with open(file_name) as f:
        src = str(f.read())
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            line_no = node.lineno
            class_name = node.name
            if err := check_name_format(class_name, line_no, 8):
                m_errs[line_no].append(err)
    return m_errs


def check_file_ers(file_name: str):
    line_no = 0
    blank_lines_count = 0
    errs = defaultdict(list)
    with open(file_name) as f:
        for line in f.readlines():
            line_no += 1
            if line.strip():
                if check_length_err(line[:-1]):
                    errs[line_no].append(f'Line {line_no}: S{1:03d} Too long')
                if check_indentation_err(line[:-1]):
                    errs[line_no].append(f'Line {line_no}: S{2:03d} Indentation is not a multiple of four')
                if check_semicolon_err(line[:-1]):
                    errs[line_no].append(f'Line {line_no}: S{3:03d} Unnecessary semicolon')
                if check_inline_comments_spaces_err(line[:-1]):
                    errs[line_no].append(
                        f'Line {line_no}: S{4:03d} At least two spaces required before inline comments')
                if check_todo_err(line[:-1]):
                    errs[line_no].append(f'Line {line_no}: S{5:03d} TODO found')
                if blank_lines_count > 2:
                    errs[line_no].append(f'Line {line_no}: S{6:03d} More than two blank lines used before this line')
                if err := check_construction_name_space_err(line[:-1], line_no):
                    errs[line_no].append(err)
                blank_lines_count = 0
            else:
                blank_lines_count += 1
    l_errs = check_classes_err(file_name)
    for l_no, e in l_errs.items():
        errs[l_no].extend(e)

    l_errs = check_functions_err(file_name)
    for l_no, e in l_errs.items():
        errs[l_no].extend(e)

    errs = OrderedDict(errs.items())
    return errs.values()


def print_errors(m_errs):
    for file_name, ers in m_errs.items():
        for er in ers:
            for e in er:
                print(f'{file_name}: {e}')


def main():
    folder_or_file = sys.argv[1]
    m_errs = {}
    if os.path.isdir(folder_or_file):

        for root, dirs, files in os.walk(folder_or_file):
            for f in files:
                if f.endswith(".py") and f != "tests.py":
                    file_name = os.path.join(root, f)
                    m_errs[file_name] = check_file_ers(file_name)

        print_errors(m_errs)

    else:
        m_errs = {folder_or_file: check_file_ers(folder_or_file)}
        print_errors(m_errs)


if __name__ == "__main__":
    main()
