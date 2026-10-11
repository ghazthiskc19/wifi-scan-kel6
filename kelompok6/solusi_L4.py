#!/usr/bin/env python3
"""
solusi_L4.py - gambar laporan lantai 4: heatmap + posisi AP, area layanan AP, pemakaian kanal,
usulan solusi (AP tambahan, rencana kanal, daya pancar), dan prediksi heatmap setelah solusi.

  python solusi_L4.py            (jalankan analyze.py L4 dulu; keluaran di output/solusi_L4/)

Posisi AP lantai 4:
  - Ext: hasil pemetaan di bawah AP (--ap F4.9/F4.10/F4.13/F4.14) = tengah ruangannya.
  - Gedung utama: estimasi dari 3 titik terkuat tiap radio (pemetaan "F4.3" tidak cocok dengan
    data: RSSI-nya hanya -54 dBm, jadi posisi diambil dari data survei).
Prediksi memakai model log-distance (tanpa redaman dinding) yang dipasang ke data survei,
jadi angkanya perkiraan, bukan pengukuran.
"""
import itertools
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Patch
import numpy as np
import pandas as pd

import analyze as A

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output", "solusi_L4")
DENAH = os.path.join(HERE, "denah", "denah_L4.png")
SSID, SCALE = "WiFi-UB.x", 20.0
KANAL = [36, 40, 44, 48, 149, 153, 157, 161]  # non-DFS 20 MHz (UNII-1 + UNII-3)
DFS = [52, 56, 60, 64]  # UNII-2: diizinkan (5250-5350 MHz, dalam ruangan) tetapi wajib DFS
KANAL_DFS = KANAL + DFS
BOBOT_DFS = 3  # penalti per AP di kanal DFS: dipakai hanya bila mengurangi interferensi cukup banyak
WARNA_KANAL = {36: "#1f77b4", 40: "#17becf", 44: "#2ca02c", 48: "#98df8a",
               52: "#e377c2", 56: "#f7b6d2", 60: "#bcbd22", 64: "#dbdb8d",
               149: "#9467bd", 153: "#d62728", 157: "#ff7f0e", 161: "#8c564b"}
DENGAR = -85  # radio di kanal sama >= ini dihitung sebagai CCI (sama dengan analyze.py)

# AP lantai 4 (radio 5 GHz SSID WiFi-UB.x). x/y None = pakai estimasi dari data.
AP = [
    ("M1", "c0:c7:0a:98:3a:52", "F4.4", 940, 350),
    ("M2", "c0:c7:0a:98:34:d1", "F4.6 / kanan-atas", None, None),
    ("M3", "c0:c7:0a:98:38:b1", "koridor bawah (F4.3/F4.5)", None, None),
    ("M4", "c0:c7:0a:98:34:11", "F4.1", None, None),
    ("E1", "c8:a6:08:8b:3e:01", "Ext F4.14", 179, 329),
    ("E2", "c0:c7:0a:98:3a:c1", "Ext F4.10", 467, 329),
    ("E3", "c8:a6:08:8b:1e:a1", "Ext F4.13", 179, 591),
    ("E4", "28:b3:71:ab:d3:91", "Ext F4.9", 467, 591),
]
# Usulan
AP_BARU = [("N1", "F4.2 (kiri-atas)", 796, 330), ("N2", "F4.8 (kanan-atas)", 960, 190)]
TURUN_DAYA = {"E1": 6.0}  # dB


def muat():
    df = A.muat_passive(os.path.join(HERE, "data", "passive_L4.csv"), "5", os.path.join(HERE, "data", "titik_L4.csv"))
    df["radio"] = A.kelompok_radio(df, SSID)
    t, pb = A.metrik_titik(df, SSID)
    xy = t.set_index("titik_id")[["x_px", "y_px"]].astype(float)
    # rssi[titik, radio]: SSID target (cakupan) dan semua SSID (radio fisik, untuk CCI)
    rssi = pb[pb.ssid == SSID].groupby(["titik_id", "radio"]).rssi.max().unstack().reindex(xy.index)
    rssi_all = pb.groupby(["titik_id", "radio"]).rssi.max().unstack().reindex(xy.index)
    lebar = pb.groupby("radio").width.max().fillna(20)
    kanal = pb.groupby("radio").channel.first().astype(int)
    est = A.estimasi_ap(pb, SSID).set_index("radio")
    kanal = pd.DataFrame({"ch": kanal, "lebar": lebar})
    aktif = pd.read_csv(os.path.join(HERE, "data", "active_L4.csv"))
    # status + penyebab (termasuk hasil uji aktif) dari analyze.py
    st = pd.read_csv(os.path.join(HERE, "output", "L4_titik.csv"))[["titik_id", "status", "penyebab_utama"]]
    t = t.merge(st, on="titik_id", how="left")
    return t.set_index("titik_id"), rssi, rssi_all, xy, kanal, est, aktif


AP_FISIK = os.path.join(HERE, "data", "ap_fisik_L4.csv")  # ap_id,x_px,y_px,... (edit bila posisi fisik diketahui)


def posisi_ap(est):
    """Posisi AP: data/ap_fisik_L4.csv (bila ada) > koordinat tetap di AP > estimasi dari data."""
    fisik = pd.read_csv(AP_FISIK).set_index("ap_id") if os.path.exists(AP_FISIK) else pd.DataFrame()
    ap = []
    for kode, radio, ruang, x, y in AP:
        if kode in fisik.index and pd.notna(fisik.at[kode, "x_px"]):
            x, y = fisik.at[kode, "x_px"], fisik.at[kode, "y_px"]
            ruang = fisik.at[kode, "lokasi"] if "lokasi" in fisik and pd.notna(fisik.at[kode, "lokasi"]) else ruang
        elif x is None:
            x, y = est.loc[radio, "x_est"], est.loc[radio, "y_est"]
        ap.append(dict(kode=kode, radio=radio, ruang=ruang, x=float(x), y=float(y)))
    return pd.DataFrame(ap).set_index("kode")


def pasang_model(rssi, xy, ap):
    """RSSI = P_ap - 10 n log10(d). n global, P per AP (least squares)."""
    baris = []
    for k, a in ap.iterrows():
        s = rssi[a.radio].dropna()
        s = s[s >= -88]
        d = np.maximum(np.hypot(xy.loc[s.index, "x_px"] - a.x, xy.loc[s.index, "y_px"] - a.y) / SCALE, 1.0)
        for v, dd in zip(s.values, d.values):
            baris.append((k, v, np.log10(dd)))
    kode = list(ap.index)
    X = np.zeros((len(baris), len(kode) + 1))
    y = np.zeros(len(baris))
    for i, (k, v, l) in enumerate(baris):
        X[i, kode.index(k)] = 1
        X[i, -1] = -10 * l
        y[i] = v
    sol, *_ = np.linalg.lstsq(X, y, rcond=None)
    P = dict(zip(kode, sol[:-1]))
    n = sol[-1]
    rmse = float(np.sqrt(np.mean((X @ sol - y) ** 2)))
    return P, n, rmse


def prediksi(P, n, ap, gx, gy):
    """Peta prediksi RSSI per AP: {kode: array}."""
    return {k: P[k] - 10 * n * np.log10(np.maximum(np.hypot(gx - a.x, gy - a.y) / SCALE, 1.0))
            for k, a in ap.iterrows()}


def evaluasi(plan, cov, dengar, rssi_asing, kanal_asing):
    """Ukuran interferensi sebuah rencana kanal.
    cci     : metode analyze.py -> di tiap titik, jumlah radio lain (AP L4 + radio asing) di kanal AP pelayan
              yang terdengar >= DENGAR. Total = jumlah kolom cci di L4_titik.csv.
    overlap : jumlah (titik x pasangan AP L4 sekanal) yang dua-duanya terdengar >= DENGAR, walaupun
              bukan AP pelayan (sel dua AP sekanal saling tumpang tindih -> berbagi airtime).
    dfs     : jumlah AP L4 di kanal DFS (52-64)."""
    cci, detail = 0, {}
    pelayan = cov.idxmax(axis=1)
    for tid, s in pelayan.items():
        ch = plan[s]
        lain = [k for k in dengar.columns if k != s and plan[k] == ch and dengar.at[tid, k] >= DENGAR]
        lain += [r for r in rssi_asing.columns if ch in kanal_asing[r] and rssi_asing.at[tid, r] >= DENGAR]
        cci += len(lain)
        detail[tid] = len(lain)
    terdengar = dengar >= DENGAR
    overlap = sum(int((terdengar[a] & terdengar[b]).sum())
                  for a, b in itertools.combinations(dengar.columns, 2) if plan[a] == plan[b])
    dfs = sum(1 for c in plan.values() if c in DFS)
    return dict(cci=cci, overlap=overlap, dfs=dfs, detail=detail)


def skor(e):
    return e["cci"] + e["overlap"] + BOBOT_DFS * e["dfs"]


def cari_rencana(cov, dengar, rssi_asing, kanal_asing, awal, kanal, ulang=30):
    """Local search (ganti kanal satu AP per langkah sampai tidak ada perbaikan), diulang dari
    beberapa titik awal acak; ambil skor terkecil. Skor = cci + overlap + BOBOT_DFS x jumlah AP DFS."""
    rng = np.random.default_rng(0)
    terbaik_plan, terbaik = None, None
    for u in range(ulang):
        plan = dict(awal) if u == 0 else {k: int(rng.choice(kanal)) for k in awal}
        nilai = skor(evaluasi(plan, cov, dengar, rssi_asing, kanal_asing))
        while True:
            maju = False
            for k, ch in itertools.product(list(plan), kanal):
                if plan[k] == ch:
                    continue
                coba = dict(plan, **{k: ch})
                v = skor(evaluasi(coba, cov, dengar, rssi_asing, kanal_asing))
                if v < nilai:
                    plan, nilai, maju = coba, v, True
            if not maju:
                break
        if terbaik is None or nilai < terbaik:
            terbaik_plan, terbaik = plan, nilai
    return terbaik_plan


def gambar_ap(ax, ap, plan, baru=(), ukuran=16, label=True, judul_ch="ch"):
    for k, a in ap.iterrows():
        ch = plan[k]
        mark = "*" if k in baru else "^"
        ax.scatter(a.x, a.y, marker=mark, s=ukuran * (26 if k in baru else 14), c=WARNA_KANAL[ch],
                   edgecolors="black", linewidths=1.2, zorder=6)
        if label:
            ax.annotate("%s %s %d" % (k, judul_ch, ch), (a.x, a.y), xytext=(9, 7), textcoords="offset points",
                        fontsize=8, weight="bold", zorder=7,
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=WARNA_KANAL[ch], alpha=0.9))


def heat(ax, img_wh, xy, z, judul, vmin=-90, vmax=-40):
    w, h = img_wh
    gx, gy = np.meshgrid(np.arange(0, w, 4), np.arange(0, h, 4))
    gz, _ = A.interpolasi(xy, z, gx, gy, SCALE)
    m = ax.imshow(gz, extent=(0, w, h, 0), cmap="RdYlGn", vmin=vmin, vmax=vmax, alpha=0.6, zorder=2)
    try:
        cs = ax.contour(gx, gy, gz, levels=[-75, -67], colors=["#d73027", "#1a9850"], linewidths=1.3, zorder=3)
        ax.clabel(cs, fmt="%d", fontsize=7)
    except ValueError:
        pass
    ax.set_title(judul, fontsize=12)
    return m


def batas(ax, w, h):
    ax.set_xlim(60, w - 40)
    ax.set_ylim(h - 60, 70)
    ax.axis("off")


def main():
    os.makedirs(OUT, exist_ok=True)
    t, rssi, rssi_all, xy, kanal, est, aktif = muat()
    ap = posisi_ap(est)
    img = plt.imread(DENAH)
    h, w = img.shape[:2]
    plan_kini = {k: int(kanal.at[a.radio, "ch"]) for k, a in ap.iterrows()}

    # ---------- 1. heatmap terukur + posisi AP ----------
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.imshow(img, zorder=1)
    v = t.dropna(subset=["rssi1"])
    m = heat(ax, (w, h), v[["x_px", "y_px"]].to_numpy(float), v.rssi1.to_numpy(float),
             "Lantai 4 - Heatmap RSSI terukur (5 GHz, %s) + posisi AP" % SSID)
    ax.scatter(v.x_px, v.y_px, s=14, c="black", zorder=4)
    for tid, r in v.iterrows():
        ax.annotate("%.0f" % r.rssi1, (r.x_px, r.y_px), xytext=(3, -10), textcoords="offset points", fontsize=7, zorder=4)
    gambar_ap(ax, ap, plan_kini)
    fig.colorbar(m, ax=ax, shrink=0.6, label="RSSI AP terkuat (dBm)")
    ax.legend(handles=[Line2D([], [], marker="^", ls="", mec="black", mfc="#bbbbbb", ms=11, label="AP (warna = kanal)"),
                       Line2D([], [], color="#1a9850", label="kontur -67 dBm (baik)"),
                       Line2D([], [], color="#d73027", label="kontur -75 dBm (lemah)")],
              loc="lower left", fontsize=9, framealpha=0.95)
    batas(ax, w, h)
    fig.savefig(os.path.join(OUT, "1_heatmap_AP_L4.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---------- 2. area layanan tiap AP ----------
    kode_radio = {a.radio: k for k, a in ap.iterrows()}
    warna_ap = dict(zip(ap.index, plt.cm.tab10(np.arange(len(ap)))))
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.imshow(img, zorder=1)
    gx, gy = np.meshgrid(np.arange(0, w, 4), np.arange(0, h, 4))
    from scipy.spatial import cKDTree
    pel = t.radio1.map(kode_radio).fillna("lain")
    d, i = cKDTree(xy.to_numpy()).query(np.column_stack([gx.ravel(), gy.ravel()]))
    lab = pel.to_numpy()[i]
    rgba = np.zeros((gx.size, 4))
    for k in ap.index:
        rgba[lab == k] = warna_ap[k]
    rgba[:, 3] = np.where((d <= 5 * SCALE) & (lab != "lain"), 0.35, 0)
    ax.imshow(rgba.reshape(gx.shape + (4,)), extent=(0, w, h, 0), zorder=2)
    for tid, r in t.iterrows():
        k = pel[tid]
        ax.scatter(r.x_px, r.y_px, s=30, c=[warna_ap.get(k, (0.5, 0.5, 0.5, 1))], edgecolors="black", zorder=4)
        a = ap.loc[k] if k in ap.index else None
        if a is not None:
            ax.plot([r.x_px, a.x], [r.y_px, a.y], color=warna_ap[k], lw=0.7, alpha=0.7, zorder=3)
    for k, a in ap.iterrows():
        ax.scatter(a.x, a.y, marker="^", s=260, c=[warna_ap[k]], edgecolors="black", linewidths=1.5, zorder=6)
        n_titik = int((pel == k).sum())
        ax.annotate("%s - %s\nch %d | %d titik dilayani" % (k, a.ruang, plan_kini[k], n_titik), (a.x, a.y),
                    xytext=(10, 8), textcoords="offset points", fontsize=8, zorder=7,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=warna_ap[k], alpha=0.92))
    ax.set_title("Lantai 4 - Posisi AP dan area layanan (titik diwarnai sesuai AP terkuat; garis = titik -> AP pelayan)\n"
                 "Ext: posisi hasil pemetaan di bawah AP. Gedung utama: posisi estimasi dari 3 titik terkuat.", fontsize=11)
    if (pel == "lain").any():
        ax.annotate("dilayani AP lain:\n" + ", ".join(pel[pel == "lain"].index), (0.01, 0.02), xycoords="axes fraction", fontsize=8)
    batas(ax, w, h)
    fig.savefig(os.path.join(OUT, "2_posisi_area_AP_L4.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---------- data kanal / CCI ----------
    rssi_ap = pd.DataFrame({k: rssi[a.radio] for k, a in ap.iterrows()}).fillna(-100)      # SSID target: AP pelayan
    dengar_ap = pd.DataFrame({k: rssi_all[a.radio] for k, a in ap.iterrows()}).fillna(-100)  # radio fisik: terdengar
    asing = [r for r in rssi_all.columns if r not in kode_radio and rssi_all[r].max() >= DENGAR]
    rssi_asing = rssi_all[asing].fillna(-100)
    kanal_asing = {r: A.kanal_terpakai(kanal.at[r, "ch"], kanal.at[r, "lebar"]) for r in asing}
    ev_kini = evaluasi(plan_kini, rssi_ap, dengar_ap, rssi_asing, kanal_asing)
    cci_kini, det_kini = ev_kini["cci"], ev_kini["detail"]

    # ---------- 3. pemakaian kanal ----------
    fig = plt.figure(figsize=(17, 8.5))
    ax = fig.add_axes([0.0, 0.0, 0.66, 0.92])
    ax.imshow(img, zorder=1)
    # garis antar-AP sekanal yang saling dengar di titik mana pun
    for k1, k2 in itertools.combinations(ap.index, 2):
        if plan_kini[k1] == plan_kini[k2]:
            dengar = ((dengar_ap[k1] >= DENGAR) & (dengar_ap[k2] >= DENGAR)).sum()
            if dengar:
                a1, a2 = ap.loc[k1], ap.loc[k2]
                ax.plot([a1.x, a2.x], [a1.y, a2.y], "--", color="red", lw=2.2, zorder=5)
                ax.annotate("ch %d dipakai 2 AP:\nterdengar bersama di %d titik" %(plan_kini[k1], dengar), ((a1.x + a2.x) / 2, (a1.y + a2.y) / 2),
                            fontsize=8, color="red", weight="bold", zorder=7, ha="center",
                            bbox=dict(fc="white", ec="red", alpha=0.85, boxstyle="round,pad=0.2"))
    # titik dengan CCI dari radio lantai lain / tak dikenal
    for tid, n in det_kini.items():
        if n:
            ax.add_patch(Circle((t.at[tid, "x_px"], t.at[tid, "y_px"]), 8 + 4 * n, fc="none", ec="red", lw=1.4, zorder=4))
            ax.annotate(str(n), (t.at[tid, "x_px"], t.at[tid, "y_px"]), xytext=(6, 4), textcoords="offset points",
                        fontsize=7, color="red", zorder=4)
    gambar_ap(ax, ap, plan_kini)
    ax.set_title("Lantai 4 - Kanal 5 GHz tiap AP (sekarang). Lingkaran merah = jumlah radio sekanal yang terdengar\n"
                 "oleh klien di titik itu (>= %d dBm, termasuk AP lantai 3/5). Total CCI = %d" % (DENGAR, cci_kini), fontsize=11)
    batas(ax, w, h)
    ax2 = fig.add_axes([0.71, 0.12, 0.27, 0.72])
    sendiri = [plan_kini[k] for k in ap.index]
    lain_ch = [c for r in asing for c in kanal_asing[r] if rssi_asing[r].max() >= -75]
    semua = sorted(set(KANAL) | set(lain_ch))
    xpos = np.arange(len(semua))
    a_s = [sendiri.count(c) for c in semua]
    a_l = [lain_ch.count(c) for c in semua]
    ax2.bar(xpos, a_s, color=[WARNA_KANAL.get(c, "#999") for c in semua], edgecolor="black", label="AP lantai 4")
    ax2.bar(xpos, a_l, bottom=a_s, color="#cccccc", edgecolor="black", hatch="//",
            label="radio lain >= -75 dBm (L3/L5/SSID lain)")
    ax2.set_xticks(xpos, [str(c) for c in semua], rotation=0)
    ax2.set_xlabel("kanal 5 GHz (lebar 20 MHz)")
    ax2.set_ylabel("jumlah radio")
    ax2.set_title("Radio per kanal di lantai 4", fontsize=11)
    ax2.legend(fontsize=8, loc="upper left")
    ax2.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    fig.savefig(os.path.join(OUT, "3_kanal_L4.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---------- model + solusi ----------
    P, n, rmse = pasang_model(rssi, xy, ap)
    P_baru = float(np.median([P[k] for k in ap.index if k.startswith("M")]))
    PLAFON = float(max(rssi_ap[k].max() for k in ap.index if k.startswith("M")))
    ap_s = pd.concat([ap, pd.DataFrame([dict(kode=k, radio="", ruang=r, x=float(x), y=float(y)) for k, r, x, y in AP_BARU]).set_index("kode")])
    P_s = dict(P, **{k: P_baru for k, *_ in AP_BARU})
    for k, db in TURUN_DAYA.items():
        P_s[k] -= db
    # RSSI di titik survei setelah solusi: AP lama = terukur (dikurangi bila daya diturunkan), AP baru = model
    rssi_s = rssi_ap.copy()
    dengar_s = dengar_ap.copy()
    for k, db in TURUN_DAYA.items():
        rssi_s[k] = rssi_s[k] - db
        dengar_s[k] = dengar_s[k] - db
    for k, _, x, y in AP_BARU:
        d = np.maximum(np.hypot(xy.x_px - x, xy.y_px - y) / SCALE, 1.0)
        # dibatasi ke RSSI terbaik yang pernah terukur dari AP gedung utama (model tanpa dinding terlalu optimis)
        rssi_s[k] = np.minimum(P_baru - 10 * n * np.log10(d), PLAFON).reindex(rssi_s.index)
        dengar_s[k] = rssi_s[k]
    awal = dict(plan_kini, **{k: KANAL[0] for k, *_ in AP_BARU})
    plan_nd = cari_rencana(rssi_s, dengar_s, rssi_asing, kanal_asing, awal, KANAL)
    plan_s = cari_rencana(rssi_s, dengar_s, rssi_asing, kanal_asing, awal, KANAL_DFS)
    ev_nd = evaluasi(plan_nd, rssi_s, dengar_s, rssi_asing, kanal_asing)
    ev_s = evaluasi(plan_s, rssi_s, dengar_s, rssi_asing, kanal_asing)
    # pembanding: kanal lama dipertahankan, hanya tambah AP (kanal AP baru dipilih terbaik)
    baru_k = [k for k, *_ in AP_BARU]
    plan_tetap = min((dict(plan_kini, **dict(zip(baru_k, c))) for c in itertools.product(KANAL, repeat=len(baru_k))),
                     key=lambda pl: skor(evaluasi(pl, rssi_s, dengar_s, rssi_asing, kanal_asing)))
    ev_tetap = evaluasi(plan_tetap, rssi_s, dengar_s, rssi_asing, kanal_asing)
    cci_s, det_s = ev_s["cci"], ev_s["detail"]
    rssi1_s = rssi_s.max(axis=1)

    # ---------- 4. gambar solusi ----------
    fig = plt.figure(figsize=(17, 9.5))
    ax = fig.add_axes([0.0, 0.0, 0.70, 0.93])
    ax.imshow(img, zorder=1)
    lemah = t[(t.status.isin(["BURUK", "KRITIS"])) | (t.rssi1 < -63)]
    for tid, r in lemah.iterrows():
        ax.add_patch(Circle((r.x_px, r.y_px), 34, fc="#f46d43", alpha=0.25, ec="#d73027", lw=1.5, zorder=3))
        ax.annotate("%s\n%.0f dBm%s" % (tid[3:], r.rssi1, "\n" + r.penyebab_utama if isinstance(r.penyebab_utama, str) else ""),
                    (r.x_px, r.y_px), xytext=(0, -38), textcoords="offset points", ha="center", fontsize=7,
                    color="#a50026", zorder=4)
    for k, a in ap_s.iterrows():
        ch0, ch1 = plan_kini.get(k), plan_s[k]
        baru = k not in ap.index
        ax.scatter(a.x, a.y, marker="*" if baru else "^", s=520 if baru else 230, c=WARNA_KANAL[ch1],
                   edgecolors="black", linewidths=1.5, zorder=6)
        if baru:
            teks = "%s BARU - %s\nch %d" % (k, a.ruang, ch1)
        elif ch0 != ch1:
            teks = "%s ch %d -> %d" % (k, ch0, ch1)
        else:
            teks = "%s ch %d (tetap)" % (k, ch1)
        if k in TURUN_DAYA:
            teks += "\nTx power -%.0f dB" % TURUN_DAYA[k]
            b = t.loc["L4-007"]
            ax.annotate("", (b.x_px, b.y_px), (a.x, a.y), zorder=5,
                        arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=2, ls="--"))
            ax.annotate("sinyal %s bocor sampai 007 (%.0f dBm)" % (k, b.rssi1), ((a.x + b.x_px) / 2, (a.y + b.y_px) / 2),
                        xytext=(0, -14), textcoords="offset points", ha="center", fontsize=8, color="#d35400",
                        weight="bold", zorder=7, bbox=dict(fc="white", ec="none", alpha=0.8))
        ax.annotate(teks, (a.x, a.y), xytext=(14, -34) if k == "N2" else (10, 8), textcoords="offset points", fontsize=8.5,
                    weight="bold", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.25", fc="#fff8dc" if baru else "white", ec=WARNA_KANAL[ch1], lw=1.5))
    ax.set_title("Lantai 4 - Usulan solusi: 2 AP tambahan, rencana kanal baru, penurunan daya AP Ext F4.14", fontsize=12)
    batas(ax, w, h)
    ax.legend(handles=[Line2D([], [], marker="^", ls="", mec="black", mfc="#bbbbbb", ms=11, label="AP lama (warna = kanal baru)"),
                       Line2D([], [], marker="*", ls="", mec="black", mfc="#bbbbbb", ms=17, label="AP baru (usulan)"),
                       Patch(fc="#f46d43", alpha=0.4, ec="#d73027", label="titik lemah / BURUK"),
                       Line2D([], [], color="#ff7f0e", ls="--", label="sinyal AP Ext bocor ke gedung utama")],
              loc="lower left", fontsize=9, framealpha=0.95)
    axt = fig.add_axes([0.71, 0.04, 0.28, 0.88])
    axt.axis("off")
    ubah = ["%s: ch %d -> %d" % (k, plan_kini[k], plan_s[k]) for k in ap.index if plan_kini[k] != plan_s[k]]
    tetap = [k for k in ap.index if plan_kini[k] == plan_s[k]]
    teks = [
        "USULAN SOLUSI LANTAI 4",
        "",
        "1. Tambah 2 AP (ceiling mount, 20 MHz)",
        "   N1 di %s -> ch %d" % (AP_BARU[0][1], plan_s["N1"]),
        "      menutup 005/006/007/008 (-59..-69 dBm,",
        "      007 sekarang dilayani AP Ext, loss 5%)",
        "   N2 di %s -> ch %d" % (AP_BARU[1][1], plan_s["N2"]),
        "      menutup F4.8: 003/203 (-59/-63 dBm,",
        "      jitter 97 ms, loss 5%)",
        "",
        "2. Rencana kanal baru (semua 20 MHz)",
        *["   " + u for u in ubah],
        "   tetap: " + ", ".join(tetap),
        "   2 AP di kanal DFS (%s)" % ", ".join("%s=%d" % (k, c) for k, c in plan_s.items() if c in DFS),
        "   CCI (metode analyze): %d -> %d" % (cci_kini, cci_s),
        "   titik tumpang tindih AP sekanal: %d -> %d" % (ev_kini["overlap"], ev_s["overlap"]),
        "   (tanpa DFS: CCI %d, tumpang tindih %d," % (ev_nd["cci"], ev_nd["overlap"]),
        "    karena 10 AP > 8 kanal non-DFS)",
        "",
        "3. Turunkan Tx power E1 (Ext F4.14) %.0f dB" % TURUN_DAYA["E1"],
        "   -34 dBm di 101, terdengar sampai 007,",
        "   CCI 3-6 radio di 101/102/206",
        "",
        "4. Aktifkan 802.11k/v + min-RSSI ~ -72 dBm",
        "   R2: ping-pong M3<->E2 dalam 10 dtk",
        "   dan putus 1 dtk di Ext",
        "",
        "5. Hall (000): CCI 6 -> %d dengan rencana" % det_s["L4-000"],
        "   kanal baru; jangan pakai 40/80 MHz",
        "",
        "Kanal 165 tidak dipakai: di luar pita",
        "5725-5825 MHz (Permenkominfo 2/2023).",
    ]
    axt.text(0, 1, "\n".join(teks), va="top", family="monospace", fontsize=9.2,
             bbox=dict(fc="white", ec="#444", boxstyle="round,pad=0.6"))
    fig.savefig(os.path.join(OUT, "4_solusi_L4.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---------- 5. prediksi sebelum vs sesudah ----------
    gx, gy = np.meshgrid(np.arange(0, w, 4), np.arange(0, h, 4))
    jarak, _ = cKDTree(xy.to_numpy()).query(np.column_stack([gx.ravel(), gy.ravel()]))
    masker = (jarak > 6 * SCALE).reshape(gx.shape)
    sebelum = np.max(np.stack(list(prediksi(P, n, ap, gx, gy).values())), axis=0)
    pr = prediksi(P_s, n, ap_s, gx, gy)
    for k, *_ in AP_BARU:
        pr[k] = np.minimum(pr[k], PLAFON)
    sesudah = np.max(np.stack(list(pr.values())), axis=0)
    fig, axs = plt.subplots(1, 2, figsize=(22, 7.6))
    fig.subplots_adjust(left=0.01, right=0.9, top=0.86, bottom=0.02, wspace=0.03)
    for ax, z, judul, a_, pl, zt in ((axs[0], sebelum, "Model - kondisi sekarang", ap, plan_kini, t.rssi1),
                                     (axs[1], sesudah, "Model - setelah solusi", ap_s, plan_s, rssi1_s)):
        ax.imshow(img, zorder=1)
        z = np.where(masker, np.nan, z)
        m = ax.imshow(z, extent=(0, w, h, 0), cmap="RdYlGn", vmin=-90, vmax=-40, alpha=0.6, zorder=2)
        cs = ax.contour(gx, gy, z, levels=[-67], colors=["#1a9850"], linewidths=1.4, zorder=3)
        ax.clabel(cs, fmt="%d", fontsize=7)
        for tid in ["L4-005", "L4-006", "L4-007", "L4-008", "L4-003", "L4-203"]:
            ax.annotate("%s: %.0f" % (tid[3:], zt[tid]), (t.at[tid, "x_px"], t.at[tid, "y_px"]), fontsize=8,
                        xytext={"L4-003": (-48, -4), "L4-203": (6, 6)}.get(tid, (4, 4)), textcoords="offset points",
                        weight="bold", zorder=8, bbox=dict(fc="white", alpha=0.85, boxstyle="round,pad=0.15"))
        gambar_ap(ax, a_, pl, baru=[k for k, *_ in AP_BARU], label=False)
        ax.set_title(judul, fontsize=13)
        batas(ax, w, h)
    fig.colorbar(m, cax=fig.add_axes([0.915, 0.15, 0.012, 0.65]), label="RSSI prediksi AP terkuat (dBm)")
    fig.suptitle("Prediksi cakupan lantai 4 (model log-distance dari data survei: n = %.2f, RMSE = %.1f dB, tanpa redaman dinding).\n"
                 "Angka di titik lemah: kiri = terukur, kanan = terukur + AP baru (model)." % (n, rmse), fontsize=12)
    fig.savefig(os.path.join(OUT, "5_prediksi_sebelum_sesudah_L4.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---------- tabel ----------
    rows = []
    for k, a in ap_s.iterrows():
        rows.append(dict(ap=k, lokasi=a.ruang, x_px=round(a.x), y_px=round(a.y), status="baru" if k not in ap.index else "lama",
                         kanal_sekarang=plan_kini.get(k, ""), kanal_usulan=plan_s[k],
                         tx_power=("-%.0f dB" % TURUN_DAYA[k]) if k in TURUN_DAYA else "tetap"))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "rencana_AP_kanal_L4.csv"), index=False)
    banding = pd.DataFrame({"rssi_terukur": t.rssi1, "rssi_setelah_solusi": rssi1_s.round(1),
                            "cci_sekarang": pd.Series(det_kini), "cci_setelah": pd.Series(det_s)})
    banding.index.name = "titik_id"
    banding.to_csv(os.path.join(OUT, "banding_titik_L4.csv"))
    print("Model: n=%.2f RMSE=%.1f dB | P AP baru=%.1f" % (n, rmse, P_baru))
    print("Kanal sekarang:", plan_kini)
    print("Kanal usulan  :", plan_s)
    for nama, pl, ev in (("sekarang (8 AP)", plan_kini, ev_kini), ("+2 AP, kanal lama", plan_tetap, ev_tetap),
                         ("+2 AP, kanal baru non-DFS", plan_nd, ev_nd), ("+2 AP, kanal baru + DFS", plan_s, ev_s)):
        print("%-28s cci=%3d overlap=%3d dfs=%d  %s" % (nama, ev["cci"], ev["overlap"], ev["dfs"], pl))
    pd.DataFrame([dict(opsi=nama, cci_metode_analyze=ev["cci"], overlap_ap_sekanal=ev["overlap"], ap_di_dfs=ev["dfs"],
                       kanal=" ".join("%s:%d" % kv for kv in pl.items()))
                  for nama, pl, ev in (("sekarang (8 AP)", plan_kini, ev_kini), ("+2 AP, kanal lama", plan_tetap, ev_tetap),
                                       ("+2 AP, kanal baru non-DFS", plan_nd, ev_nd), ("+2 AP, kanal baru + DFS", plan_s, ev_s))]
                 ).to_csv(os.path.join(OUT, "opsi_kanal_L4.csv"), index=False)
    print("RSSI >= -67: %.0f%% -> %.0f%% | min %.1f -> %.1f" % (100 * (t.rssi1 >= -67).mean(), 100 * (rssi1_s >= -67).mean(),
                                                               t.rssi1.min(), rssi1_s.min()))
    print(banding.loc[["L4-005", "L4-006", "L4-007", "L4-008", "L4-003", "L4-203", "L4-000", "L4-101", "L4-102", "L4-206"]])
    print("Tersimpan di", OUT)


if __name__ == "__main__":
    main()
