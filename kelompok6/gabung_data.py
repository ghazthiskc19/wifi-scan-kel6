#!/usr/bin/env python3
"""
gabung_data.py - gabungkan hasil scan semua laptop per lantai:
  data/passive_L{n}_<device>.csv  ->  data/passive_L{n}.csv     (n = 3, 4, 5)
  data/passive_L{n}_<device>_T2.csv -> data/passive_L{n}_T2.csv
Jalankan setelah semua file CSV anggota dikumpulkan ke folder data/.
"""
import glob
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

for n in (3, 4, 5):
    for slot in ("", "_T2"):
        pola = os.path.join(HERE, "data", "passive_L%d_*%s.csv" % (n, slot))
        files = [f for f in glob.glob(pola) if slot or not f.endswith("_T2.csv")]
        if not files:
            continue
        df = pd.concat([pd.read_csv(f, dtype=str) for f in files], ignore_index=True)
        out = os.path.join(HERE, "data", "passive_L%d%s.csv" % (n, slot))
        df.to_csv(out, index=False, encoding="utf-8")
        print("L%d%s: %d file, %d titik, perangkat %s -> %s" % (
            n, slot, len(files), df.titik_id.nunique(), sorted(df.device.unique()), os.path.relpath(out, HERE)))
