# P06 checker: re-derive SRDetectorConfig fields, defaults and the committed sr_detector: keys (text parsing of git show output only; nothing from legacy code is imported or run)
import re, subprocess, sys
def show(p):
    return subprocess.run(["git","-C","/home/claude/repos/legacy","show","970aabf:"+p],capture_output=True,text=True,check=True).stdout.split("\n")
L = show("core/config_loader.py")
fields = []
for i in range(1152, 1224):   # 0-based index i -> line i+1 ; L1153..L1224
    m = re.match(r"^    ([a-z_0-9]+): ([^=]+?)(?: = (.+?))?\s*(#.*)?$", L[i])
    if m and not L[i].strip().startswith("model_config"):
        default = m.group(3)
        if default and "default_factory" in default:
            default = re.sub(r"Field\(default_factory=(lambda: )?","",default).rstrip(")")
        fields.append((i+1, m.group(1), m.group(2).strip(), (default or "").strip()))
print("FIELDS", len(fields))
Y = show("config/system_config.yaml")
keys = {}
for i in range(507, 545):  # L508..L545
    m = re.match(r"^  ([a-z_0-9]+):\s*(.+?)\s*(#.*)?$", Y[i])
    if m: keys[m.group(1)] = (i+1, m.group(2))
print("YAML KEYS", len(keys))
def norm(v, typ):
    v = v.strip().strip('"').strip("'")
    if typ.startswith("bool"): return v.lower()
    if typ.startswith("float"):
        try: return float(v)
        except: return v
    if typ.startswith("int"):
        try: return int(v)
        except: return v
    if typ.startswith("list"): return re.sub(r"\s","",v).replace("'",'"')
    return v
diff = []; notin = []
for ln, name, typ, d in fields:
    if name in keys:
        y = keys[name]
        eq = norm(y[1], typ) == norm(d, typ)
        print(f"L{ln}\t{name}\t{typ}\tdefault={d}\tyaml=L{y[0]}:{y[1]}\t{'SAME' if eq else 'DIFFERS'}")
        if not eq: diff.append(name)
    else:
        print(f"L{ln}\t{name}\t{typ}\tdefault={d}\tNOT IN FILE"); notin.append(name)
extra = [k for k in keys if k not in [f[1] for f in fields]]
print("DIFFERS:", diff); print("NOT IN FILE (%d):"%len(notin), notin); print("YAML keys not fields:", extra)
