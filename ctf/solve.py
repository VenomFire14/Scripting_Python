import json
from collections import defaultdict

data = json.load(open("transactions.json"))

seen = defaultdict(list)

for name, tx in data.items():
    sig = tx["signature_der"]

    # DER decode manually
    # 30 LL 02 rlen r 02 slen s
    rlen = int(sig[6:8],16)
    r = sig[8:8+rlen*2]

    seen[r].append((name,tx))

for r, items in seen.items():
    if len(items) > 1:
        print("DUPLICATE R:", r)
        for x in items:
            print(x[0], x[1]["amount"])