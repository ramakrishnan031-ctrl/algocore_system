"""P06 checker helper: list every `with self._lock` block of screening/entry_gate.py at the baseline and
the calls inside it. Reads the text with `git show` (never imports or runs legacy code)."""
import ast, subprocess, sys
src = subprocess.run(["git", "-C", "/home/claude/repos/legacy", "show", "970aabf:screening/entry_gate.py"],
                     capture_output=True, text=True, check=True).stdout
tree = ast.parse(src)
for fn in ast.walk(tree):
    if isinstance(fn, (ast.FunctionDef,)):
        for node in ast.walk(fn):
            if isinstance(node, ast.With):
                ctx = ast.unparse(node.items[0].context_expr)
                if ctx == "self._lock":
                    calls = sorted({ast.unparse(c.func) for b in node.body for c in ast.walk(b) if isinstance(c, ast.Call)})
                    raises = [n.lineno for b in node.body for n in ast.walk(b) if isinstance(n, ast.Raise)]
                    print(f"{fn.name}: L{node.lineno}-L{node.end_lineno} calls={calls} raises={raises}")
