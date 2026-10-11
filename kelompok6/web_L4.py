#!/usr/bin/env python3
"""
web_L4.py - data LIVE dari controller kampus (dashboard Wi-Fi FILKOM) sebagai pendukung survei lantai 4.
Jalankan setelah ambil_web_filkom.py (minimal sekali) dan solusi_L4.py:

  10_web_pengguna_L4.png     rata-rata perangkat per jam di lantai 4 (7 hari) vs asumsi kelompok
  11_web_airtime_L4.png      airtime 5 GHz per AP lantai 4: spreadsheet Agustus 2025 vs dashboard sekarang
  web_ringkasan_L4.txt       angka kunci

Yang dipakai hanya data live (api/public/recommend dan clients). Peta 3D (api/public/wifimodel: posisi, model, EIRP,
kanal) belum diperbarui, jadi TIDAK dipakai; kanal & posisi AP tetap dari survei kami.

  python web_L4.py
"""
import glob
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import solusi_L4 as S

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "data", "web_filkom")
OUT = S.OUT
# nama AP di dashboard -> nama kita (lokasi fisik)
NAMA_KITA = {"F4.1": "AP-F4.1", "F4.3": "AP-F4.3", "F4.4": "AP-F4.4", "F4.6": "AP-F4.6", "F4-Ext-F4.9": "AP-F4.9",
             "F4-Ext-F4.10": "AP-F4.10", "F4-Ext-4.13": "AP-F4.13", "F4-Ext-4.14": "AP-F4.14"}
ASUMSI_USER = 12 * 35  # 12 ruang kuliah x 35 orang (asumsi kelompok)
MERAH, ABU = "#e30613", "#9a9a94"


def snapshot_terakhir():
    d = sorted(glob.glob(os.path.join(WEB, "20*")))[-1]
    return json.load(open(os.path.join(d, "recommend.json"), encoding="utf-8"))


def kanal_survei():
    """Kanal tiap AP lantai 4 hasil survei kami (bukan dari peta 3D website)."""
    t, rssi, rssi_all, xy, kanal, est, aktif = S.muat()
    ap = S.posisi_ap(est)
    return {k: int(kanal.at[a.radio, "ch"]) for k, a in ap.iterrows()}


def gambar_pengguna(rec):
    a = {x["area"]: x for x in rec["areas"]}
    h4 = np.array(a["Lantai 4"]["hourly"], float)
    jam = np.arange(24)
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=170)
    ax.bar(jam, h4, color=["#121212" if v < h4.max() else MERAH for v in h4], width=0.75)
    ax.axhline(ASUMSI_USER, color=MERAH, ls="--", lw=1.4)
    ax.text(5.6, ASUMSI_USER + 8, "asumsi kelompok: 12 kelas x 35 = %d" % ASUMSI_USER, color=MERAH, fontsize=10)
    p = int(h4.argmax())
    ax.annotate("puncak %.0f perangkat\n(rata-rata 7 hari, termasuk Sabtu-Minggu)" % h4[p], (p, h4[p]), xytext=(p + 1.2, h4[p] + 25),
                fontsize=10, arrowprops=dict(arrowstyle="-", color="#121212"))
    ax.scatter([15 + 40 / 60], [364], marker="D", s=60, color="#f2a900", zorder=5)
    ax.annotate("26 Agu 2025 15:40: 364 klien\n(daftar AP kampus, 8 AP L4)", (15 + 40 / 60, 364), xytext=(16.4, 330), fontsize=9)
    ax.set_xticks(range(6, 23), [f"{h:02d}" for h in range(6, 23)])
    ax.set_xlim(5.4, 22.6)
    ax.set_ylim(0, 470)
    ax.set_xlabel("jam (WIB)")
    ax.set_ylabel("perangkat 5 GHz tersambung di lantai 4")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "10_web_pengguna_L4.png"), facecolor="white")
    plt.close(fig)
    return h4


def gambar_airtime(ch_survei):
    poll = pd.read_csv(os.path.join(WEB, "poll_ap.csv"))
    poll = poll[poll.area == "Lantai 4"]
    sekarang = poll.groupby("ap").agg(air=("airtime", "mean"), lo=("airtime", "min"), hi=("airtime", "max"), klien=("klien", "max"))
    sekarang.index = [NAMA_KITA[a] for a in sekarang.index]
    sekarang["ch"] = [ch_survei[a] for a in sekarang.index]
    sekarang = sekarang.sort_values("air", ascending=False)
    waktu = sorted(poll.waktu.unique())

    sp = pd.read_csv(os.path.join(HERE, "..", "RuckusAPList.csv"))   # hanya nama, kanal, klien, airtime yang dipakai
    sp = sp[sp["AP Name"].astype(str).str.contains("F4")]
    lama = pd.DataFrame({"air": sp["Airtime Utilization (5G)"].values, "klien": sp["Clients"].values,
                         "ch": sp["Channel (5G)"].str.extract(r"(\d+)")[0].astype(int).values},
                        index=sp["AP Name"].values).sort_values("air", ascending=False)

    fig, axs = plt.subplots(1, 2, figsize=(14, 5.2), dpi=170, sharey=True)
    for ax, df, judul in ((axs[0], lama, "26 Agustus 2025, ±15:40 (jam kuliah)\ndaftar AP kampus (nama AP lama)"),
                          (axs[1], sekarang, "11 Oktober 2026, %s–%s WIB (Minggu malam)\nwebsite Wi-Fi FILKOM, %d snapshot"
                           % (waktu[0][-5:], waktu[-1][-5:], len(waktu)))):
        x = np.arange(len(df))
        warna = [MERAH if c == 153 else "#121212" for c in df.ch]
        ax.bar(x, df.air, color=warna, width=0.65)
        if "lo" in df:
            ax.errorbar(x, df.air, yerr=[df.air - df.lo, df.hi - df.air], fmt="none", ecolor=ABU, capsize=3)
        for i, r in enumerate(df.itertuples()):
            ax.text(i, getattr(r, "hi", r.air) + 2.5, "ch%d\n%d klien" % (r.ch, r.klien), ha="center", fontsize=8.5)
        ax.set_xticks(x, df.index, rotation=35, ha="right", fontsize=9)
        ax.set_title(judul, fontsize=11)
        ax.set_ylim(0, 100)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axs[0].set_ylabel("airtime 5 GHz terpakai (%)")
    fig.text(0.5, 0.005, "merah = kanal 153. Kiri: kanal & nama dari daftar AP kampus 2025. "
             "Kanan: nama & kanal dari survei kami, airtime & klien dari website Wi-Fi FILKOM (live).", ha="center", fontsize=9, color="#4d4d47")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(OUT, "11_web_airtime_L4.png"), facecolor="white")
    plt.close(fig)
    return sekarang, lama


def main():
    rec = snapshot_terakhir()
    h4 = gambar_pengguna(rec)
    sekarang, lama = gambar_airtime(kanal_survei())
    snr = pd.read_csv(os.path.join(WEB, "poll_klien.csv"))
    teks = [
        "Perangkat L4 per jam (rata-rata 7 hari): puncak %.0f pukul %02d:00; jam 08-16 rata-rata %.0f"
        % (h4.max(), h4.argmax(), h4[8:17].mean()),
        "Airtime sekarang (rata-rata snapshot): " + ", ".join("%s(ch%d)=%.0f%% [%d-%d]" % (a, r.ch, r.air, r.lo, r.hi)
                                                            for a, r in sekarang.iterrows()),
        "Airtime Agustus 2025: " + ", ".join("%s(ch%d)=%d%%/%d klien" % (a, r.ch, r.air, r.klien) for a, r in lama.iterrows()),
        "SNR klien 5 GHz se-gedung (semua snapshot): median %.0f dB, n=%d" % (snr.snr.median(), len(snr)),
    ]
    open(os.path.join(OUT, "web_ringkasan_L4.txt"), "w", encoding="utf-8").write("\n".join(teks) + "\n")
    print("\n".join(teks))


if __name__ == "__main__":
    main()
