#!/usr/bin/env python3
"""P04 checker helper: print or compare the source text of named functions/classes
in a legacy file at given commits. Reads text with `git show` and parses it with
`ast` only; never imports or runs legacy code.

Usage:
  python3 -I -B p04chk_func.py show <commit> <path> <qualname>
  python3 -I -B p04chk_func.py cmp <commitA> <commitB> <path> <qualname> [<qualname> ...]
"""
import ast
import subprocess
import sys

REPO = "/home/claude/repos/legacy"


def text_at(commit, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{commit}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def find(src, qualname):
    tree = ast.parse(src)
    parts = qualname.split(".")
    nodes = tree.body
    node = None
    for p in parts:
        node = next((n for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == p), None)
        if node is None:
            return None
        nodes = node.body
    lines = src.splitlines()
    start = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
    return start, node.end_lineno, "\n".join(lines[start - 1:node.end_lineno])


def main():
    if sys.argv[1] == "show":
        _, _, commit, path, q = sys.argv
        r = find(text_at(commit, path), q)
        print(f"{q}: L{r[0]} to L{r[1]}")
        print(r[2])
    elif sys.argv[1] == "cmp":
        a, b, path = sys.argv[2:5]
        sa, sb = text_at(a, path), text_at(b, path)
        for q in sys.argv[5:]:
            ra, rb = find(sa, q), find(sb, q)
            same = ra is not None and rb is not None and ra[2] == rb[2]
            print(f"{path}::{q} {a}=L{ra[0] if ra else '-'}..{ra[1] if ra else '-'} "
                  f"{b}=L{rb[0] if rb else '-'}..{rb[1] if rb else '-'} identical={same}")


if __name__ == "__main__":
    main()
