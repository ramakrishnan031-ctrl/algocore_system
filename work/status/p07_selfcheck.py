import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
defs = re.findall(r"^- (P07-S\d{3}) (FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|OPEN QUESTION)\b", t, re.M)
ids = [d[0] for d in defs]
nums = [int(i[5:]) for i in ids]
print("statements:", len(ids), "first", ids[0], "last", ids[-1])
print("gaps:", sorted(set(range(1, max(nums)+1)) - set(nums)))
print("dups:", sorted({i for i in ids if ids.count(i) > 1}))
print("out of order:", [ids[k] for k in range(1, len(nums)) if nums[k] < nums[k-1]])
starts = re.findall(r"^- (P07-S\d{3})(.{0,40})", t, re.M)
bad = [s for s in starts if not re.match(r" (FACT|UNKNOWN / NOT ESTABLISHED|INTERPRETATION|HISTORICAL|OPEN QUESTION)", s[1])]
print("unlabelled:", bad)
refs = set(re.findall(r"P07-S\d{3}", t))
print("dangling refs:", sorted(refs - set(ids)))
for k in ("AP", "U", "R"):
    pat = {"AP": r"^- (P07-AP\d{2})", "U": r"^- (P07-U\d{2})", "R": r"^- (P07-R\d)"}[k]
    d = re.findall(pat, t, re.M)
    print(k, len(d), d[:1], d[-1:])
    r = set(re.findall(pat.replace("^- (", "(").replace(")", ")"), t))
r_ap = set(re.findall(r"P07-AP\d{2}", t)); d_ap = set(re.findall(r"^- (P07-AP\d{2})", t, re.M))
r_r = set(re.findall(r"P07-R\d", t)); d_r = set(re.findall(r"^- (P07-R\d)", t, re.M))
print("dangling AP:", sorted(r_ap - d_ap), "dangling R:", sorted(r_r - d_r))
labels = {}
for i, l in defs: labels[l] = labels.get(l, 0) + 1
print("labels:", labels)
