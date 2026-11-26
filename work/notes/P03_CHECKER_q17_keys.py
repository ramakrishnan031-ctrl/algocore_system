"""P03 checker: text-only comparison of the sr_detector_results key sets (A03 Q-17).
Reads three text files given as arguments (produced by `git show 970aabf:<path>`); imports nothing
from the legacy code and executes none of it."""
import re, sys
store_txt, det_txt, rm_txt = (open(p, encoding="utf-8").read().splitlines() for p in sys.argv[1:4])
def lines(txt, a, b):
    return "\n".join(txt[a-1:b])
cols = re.findall(r'"([a-z_]+)"', lines(store_txt, 1970, 1977))
det = re.findall(r'^\s*"([a-z_]+)"\s*:', lines(det_txt, 269, 294), flags=re.M)
rm = re.findall(r'"([a-z_]+)"\s*:', lines(rm_txt, 413, 431))
print("store _SR_INSERT_COLS:", len(cols)); print(cols)
print("detector row keys:", len(det), "equal in content and order:", det == cols)
print("divert row keys:", len(rm), "equal in content and order:", rm == cols)
print("divert set equal:", set(rm) == set(cols), "missing:", sorted(set(cols)-set(rm)), "extra:", sorted(set(rm)-set(cols)))
