#!/usr/bin/env python3
"""
bukti_L4.py - gambar + tabel BUKTI untuk presentasi lantai 4 (jalankan setelah analyze.py dan solusi_L4.py):

  6_bukti_cci_L4.png          spektrum 5 GHz di 4 titik CCI terparah: radio apa saja yang sekanal
  7_radio_per_kanal_L4.png    kepadatan tiap kanal + asal radionya (AP L4, AP L3/L5, jaringan lain)
  8_floor_bleed_L4.png        sinyal AP lantai 3/5 yang terdengar di lantai 4 + estimasi redaman pelat lantai
  bukti_cci_L4.csv            daftar lengkap tiap kejadian CCI (sumber angka 43)
  radio_L4.csv                semua radio 5 GHz yang terdengar di L4 (kanal, SSID, asal lantai)
  floor_bleed_L4.csv          radio lintas lantai + selisih RSSI (sudah dikoreksi offset laptop)
  validasi_kanal_L4.csv       pasangan AP sekanal pada rencana lama vs baru
  banding_spreadsheet_L4.csv  kanal di daftar AP controller (spreadsheet) vs kanal terukur

  python bukti_L4.py
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

import analyze as A
import solusi_L4 as S

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = S.OUT
KAMPUS = {"WiFi-UB.x", "eduroam", "FILKOM EVENT", "WiFi-FILKOM", "WiFi-UB"}
KATEGORI = {"ap_l4": ("AP WiFi-UB.x lantai 4", "#1f77b4"),
            "ap_l5": ("AP kampus dari lantai 5", "#d62728"),
            "ap_l3": ("AP kampus dari lantai 3", "#ff7f0e"),
            "ap_lain": ("AP kampus lain (bukan 8 AP L4)", "#9467bd"),
            "non": ("Jaringan lain (lab, hotspot, fakultas lain)", "#7f7f7f")}
SEMUA_KANAL = [36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161, 165]
# SSID organisasi boleh ditampilkan; SSID lain (hotspot HP, nama orang) disamarkan
SSID_TAMPIL = KAMPUS | {"ROBOTIIK", "FKUB_HotSpot", "FKUB_HotSpot_Backup", "FEB-UB", "AP-HOST", "APCobaX"}


def samarkan(ss):
    return [x if x in SSID_TAMPIL else "(hotspot/SSID pribadi)" for x in ss]


def offset_laptop():
    """Offset kalibrasi (dB) per laptop: positif = membaca lebih kuat dari laptop acuan."""
    p = os.path.join(HERE, "data", "offset_kalibrasi.csv")
    return {r["laptop"]: float(r["offset_db_median"]) for r in csv.DictReader(open(p, encoding="utf-8-sig"))}


def rssi_lantai(n, off):
    """Maks RSSI per BSSID per titik di lantai n, dikoreksi offset laptop (dibuat setara laptop acuan)."""
    df = A.muat_passive(os.path.join(HERE, "data", "passive_L%d.csv" % n), "5", os.path.join(HERE, "data", "titik_L%d.csv" % n))
    lap = df.device.mode().iloc[0]
    k = off.get(lap, 0.0)
    df["rssi_kor"] = df.rssi_dbm - k
    per = df.groupby(["bssid", "titik_id"]).rssi_kor.max().unstack()
    return per, lap, k


def main():
    off = offset_laptop()
    df = A.muat_passive(os.path.join(HERE, "data", "passive_L4.csv"), "5", os.path.join(HERE, "data", "titik_L4.csv"))
    df["radio"] = A.kelompok_radio(df, S.SSID)
    t, pb = A.metrik_titik(df, S.SSID)
    t = t.set_index("titik_id")
    st = pd.read_csv(os.path.join(HERE, "output", "L4_titik.csv")).set_index("titik_id")
    _, rssi, rssi_all, xy, kanal, est, _ = S.muat()
    ap = S.posisi_ap(est)
    kode = {a.radio: k for k, a in ap.iterrows()}
    bss_radio = df.drop_duplicates("bssid").set_index("bssid").radio

    # ---------- tabel radio + asal lantai ----------
    l3, lap3, k3 = rssi_lantai(3, off)
    l5, lap5, k5 = rssi_lantai(5, off)
    def maks_lain(per, radio):
        b = [x for x in bss_radio[bss_radio == radio].index if x in per.index]
        return per.loc[b].max().max() if b else np.nan
    ssid_radio = pb.groupby("radio").ssid.agg(lambda s: sorted(set(samarkan(set(s)))))
    rows = []
    for r in rssi_all.columns:
        m4 = rssi_all[r].max()
        if not m4 >= S.DENGAR:
            continue
        ss = ssid_radio[r]
        m3, m5 = maks_lain(l3, r), maks_lain(l5, r)
        if r in kode:
            kat = "ap_l4"
        elif not (set(ss) & KAMPUS):
            kat = "non"
        elif m5 >= m4 + 3 and not (m3 > m5):
            kat = "ap_l5"
        elif m3 >= m4 + 3:
            kat = "ap_l3"
        else:
            kat = "ap_lain"
        rows.append(dict(radio=r, kode_ap=kode.get(r, ""), ssid=" / ".join(ss), kanal=int(kanal.at[r, "ch"]),
                         lebar_mhz=int(kanal.at[r, "lebar"]), kanal_terpakai=" ".join(map(str, sorted(A.kanal_terpakai(kanal.at[r, "ch"], kanal.at[r, "lebar"])))),
                         rssi_maks_L4=round(m4, 1), titik_L4=rssi_all[r].idxmax(),
                         n_titik_L4_terdengar=int((rssi_all[r] >= S.DENGAR).sum()),
                         rssi_maks_L3_kor=round(m3, 1) if m3 == m3 else "", rssi_maks_L5_kor=round(m5, 1) if m5 == m5 else "",
                         kategori=KATEGORI[kat][0], kat=kat))
    rad = pd.DataFrame(rows).sort_values(["kanal", "rssi_maks_L4"], ascending=[True, False])
    rad.drop(columns="kat").to_csv(os.path.join(OUT, "radio_L4.csv"), index=False)
    kat_of = rad.set_index("radio").kat

    # ---------- bukti CCI per titik (logika sama dengan analyze.py) ----------
    tg = pb[pb.ssid == S.SSID].sort_values("rssi", ascending=False).drop_duplicates(["titik_id", "radio"])
    per_radio = pb.sort_values("rssi", ascending=False).groupby(["titik_id", "radio"]).first().reset_index()
    kej = []
    for tid, g in per_radio.groupby("titik_id"):
        p = tg[tg.titik_id == tid].iloc[0]
        occ = A.kanal_terpakai(p.channel, p.width)
        for _, o in g[(g.radio != p.radio) & (g.rssi >= A.CCI_RSSI)].iterrows():
            if occ & A.kanal_terpakai(o.channel, o.width):
                kej.append(dict(titik_id=tid, ap_pelayan=kode.get(p.radio, p.radio), kanal_pelayan=int(p.channel),
                                rssi_pelayan=round(p.rssi, 1), radio_pengganggu=o.radio,
                                kode_pengganggu=kode.get(o.radio, ""), ssid_pengganggu=ssid_radio[o.radio][0] if len(ssid_radio[o.radio]) == 1 else " / ".join(ssid_radio[o.radio]),
                                kanal_pengganggu=int(o.channel), lebar_pengganggu=int(o.width), rssi_pengganggu=round(o.rssi, 1),
                                asal_pengganggu=KATEGORI[kat_of.get(o.radio, "non")][0]))
    kej = pd.DataFrame(kej)
    kej.to_csv(os.path.join(OUT, "bukti_cci_L4.csv"), index=False)
    total = len(kej)
    assert total == int(st.cci.sum()), (total, st.cci.sum())

    # ---------- 6. spektrum di titik CCI terparah ----------
    top = st.cci.sort_values(ascending=False).head(4).index
    fig, axs = plt.subplots(2, 2, figsize=(17, 10), sharey=True)
    xpos = {c: i for i, c in enumerate(SEMUA_KANAL)}
    for ax, tid in zip(axs.ravel(), top):
        g = per_radio[per_radio.titik_id == tid]
        p = tg[tg.titik_id == tid].iloc[0]
        occ = A.kanal_terpakai(p.channel, p.width)
        for c in occ:
            if c in xpos:
                ax.axvspan(xpos[c] - 0.45, xpos[c] + 0.45, color="#ffe8a3", zorder=0)
        ax.axhline(A.CCI_RSSI, ls="--", color="black", lw=1)
        ax.text(len(SEMUA_KANAL) - 0.5, A.CCI_RSSI + 0.8, "batas dengar %d dBm" % A.CCI_RSSI, ha="right", fontsize=8)
        for _, o in g.iterrows():
            kat = kat_of.get(o.radio, "non")
            ch = sorted(A.kanal_terpakai(o.channel, o.width))
            xs = [xpos[c] for c in ch if c in xpos]
            if not xs:
                continue
            jitter = (hash(o.radio) % 7 - 3) * 0.05
            pelayan = o.radio == p.radio
            if len(xs) > 1:
                ax.plot([min(xs) - 0.3, max(xs) + 0.3], [o.rssi, o.rssi], color=KATEGORI[kat][1], lw=2.5, alpha=0.8, zorder=2)
            ax.scatter(np.mean(xs) + jitter, o.rssi, marker="*" if pelayan else "o", s=380 if pelayan else 55,
                       color=KATEGORI[kat][1], edgecolors="black", linewidths=1 if pelayan else 0.5, zorder=4)
            sekanal = (not pelayan) and o.rssi >= A.CCI_RSSI and occ & set(ch)
            if pelayan or sekanal:
                lab = kode.get(o.radio) or ssid_radio[o.radio][0]
                ax.annotate("%s %.0f" % (lab, o.rssi), (np.mean(xs) + jitter, o.rssi), xytext=(7, -3), textcoords="offset points",
                            fontsize=7.5, weight="bold" if pelayan else None, zorder=5)
        ax.set_xticks(range(len(SEMUA_KANAL)), [str(c) for c in SEMUA_KANAL])
        ax.set_xlim(-0.6, len(SEMUA_KANAL) - 0.4)
        ax.set_ylim(-95, -35)
        ax.grid(axis="y", alpha=0.3)
        ax.set_title("%s (%s)\ndilayani %s ch %d, %.0f dBm -> %d radio lain sekanal >= %d dBm = CCI %d"
                     % (tid, S.A.judul(str(pd.read_csv(os.path.join(HERE, "data", "titik_L4.csv")).set_index("titik_id").at[tid, "keterangan"]))[:38],
                        kode.get(p.radio, "?"), p.channel, p.rssi, int(st.at[tid, "cci"]), A.CCI_RSSI, int(st.at[tid, "cci"])), fontsize=10)
        ax.set_xlabel("kanal 5 GHz (pita kuning = kanal yang dipakai AP pelayan)")
    for ax in axs[:, 0]:
        ax.set_ylabel("RSSI terukur (dBm)")
    fig.legend(handles=[Line2D([], [], marker="*", ls="", color="#1f77b4", mec="black", ms=16, label="AP pelayan (terkuat)")] +
               [Line2D([], [], marker="o", ls="", color=c, mec="black", ms=8, label=l) for l, c in KATEGORI.values()] +
               [Line2D([], [], color="#555", lw=2.5, label="garis = radio 40/80 MHz (menduduki beberapa kanal)")],
               loc="lower center", ncol=4, fontsize=9, frameon=False)
    fig.suptitle("Bukti co-channel interference: semua radio 5 GHz yang terdengar di 4 titik CCI terparah lantai 4 (data passive_L4.csv)\n"
                 "Total kejadian CCI di 39 titik = %d (jumlah kolom cci di output/L4_titik.csv; rincian di bukti_cci_L4.csv)" % total, fontsize=12)
    fig.tight_layout(rect=(0, 0.06, 1, 0.93))
    fig.savefig(os.path.join(OUT, "6_bukti_cci_L4.png"), dpi=150)
    plt.close(fig)

    # ---------- 7. radio per kanal ----------
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(18, 6.5), gridspec_kw=dict(width_ratios=[1.35, 1]))
    xs = np.arange(len(SEMUA_KANAL))
    bawah = np.zeros(len(SEMUA_KANAL))
    for kat, (lab, warna) in KATEGORI.items():
        nilai = np.array([sum(1 for _, r in rad[rad.kat == kat].iterrows() if str(c) in r.kanal_terpakai.split()) for c in SEMUA_KANAL])
        ax.bar(xs, nilai, bottom=bawah, color=warna, edgecolor="black", label=lab)
        bawah += nilai
    for i, v in enumerate(bawah):
        ax.text(i, v + 0.15, str(int(v)), ha="center", fontsize=9, weight="bold")
    ax.axvspan(3.5, 7.5, color="#eeeeee", zorder=0)
    ax.text(5.5, max(bawah) * 0.92, "UNII-2 (DFS)\n52-64", ha="center", fontsize=9, color="#555")
    ax.axvspan(11.5, 12.5, color="#fde0dd", zorder=0)
    ax.text(12, max(bawah) * 0.92, "165\n(di luar\n5725-5825)", ha="center", fontsize=8, color="#a50026")
    ax.set_xticks(xs, [str(c) for c in SEMUA_KANAL])
    ax.set_xlabel("kanal 5 GHz (20 MHz)")
    ax.set_ylabel("jumlah radio yang terdengar >= %d dBm di lantai 4" % S.DENGAR)
    ax.set_title("Kepadatan kanal di lantai 4 dan asal radionya", fontsize=12)
    ax.legend(fontsize=9, loc="upper left")
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    # tabel radio non-L4 terkuat
    lain = rad[rad.kat != "ap_l4"].sort_values("rssi_maks_L4", ascending=False).head(14)
    ax2.axis("off")
    sel = [[r.kanal if r.lebar_mhz == 20 else "%d (%d MHz)" % (r.kanal, r.lebar_mhz), r.ssid[:30], "%.0f" % r.rssi_maks_L4,
            r.titik_L4[3:], KATEGORI[r.kat][0].replace("AP kampus ", "").replace("Jaringan lain (lab, hotspot, fakultas lain)", "jaringan lain")]
           for _, r in lain.iterrows()]
    tb = ax2.table(cellText=sel, colLabels=["kanal", "SSID", "RSSI maks L4", "di titik", "asal"], loc="upper center",
                   colWidths=[0.14, 0.38, 0.14, 0.1, 0.3])
    tb.auto_set_font_size(False)
    tb.set_fontsize(8)
    tb.scale(1, 1.35)
    ax2.set_title("14 radio non-AP-L4 terkuat yang terdengar di L4 (lengkap: radio_L4.csv)", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "7_radio_per_kanal_L4.png"), dpi=150)
    plt.close(fig)

    # ---------- 8. floor bleed ----------
    asing = rad[rad.kat.isin(["ap_l3", "ap_l5"])]
    fb = []
    for _, r in asing.iterrows():
        lantai = 5 if r.kat == "ap_l5" else 3
        per = l5 if lantai == 5 else l3
        b = [x for x in bss_radio[bss_radio == r.radio].index if x in per.index]
        s_asal = per.loc[b].max()
        p_asal = s_asal.idxmax()
        p4 = "L4-" + p_asal[3:]
        di4_sama = rssi_all.at[p4, r.radio] if p4 in rssi_all.index else np.nan
        fb.append(dict(radio=r.radio, ssid=r.ssid, kanal=r.kanal, lantai_asal=lantai, titik_terkuat_asal=p_asal,
                       rssi_asal_kor=round(s_asal.max(), 1), rssi_L4_titik_tegak_lurus=round(di4_sama, 1) if di4_sama == di4_sama else "",
                       redaman_lantai_db=round(s_asal.max() - di4_sama, 1) if di4_sama == di4_sama else "",
                       rssi_maks_L4=r.rssi_maks_L4, titik_maks_L4=r.titik_L4, n_titik_L4_terdengar=r.n_titik_L4_terdengar,
                       ikut_cci_L4=int((kej.radio_pengganggu == r.radio).sum()) if len(kej) else 0))
    fb = pd.DataFrame(fb).sort_values("rssi_maks_L4", ascending=False)
    fb.to_csv(os.path.join(OUT, "floor_bleed_L4.csv"), index=False)
    # titik L4 yang AP lantai lain-nya hampir menyaingi AP pelayan
    saingan = []
    for tid in t.index:
        cols = [c for c in asing.radio if c in rssi_all.columns]
        if not cols:
            continue
        r_l = rssi_all.loc[tid, cols]
        if r_l.max() >= S.DENGAR:
            saingan.append((tid, r_l.idxmax(), r_l.max(), t.at[tid, "rssi1"]))
    fig = plt.figure(figsize=(18, 8.5))
    ax = fig.add_axes([0.0, 0.0, 0.6, 0.9])
    img = plt.imread(S.DENAH)
    h, w = img.shape[:2]
    ax.imshow(img)
    lantai_of = dict(zip(fb.radio, fb.lantai_asal))
    top6 = {x[0] for x in sorted(saingan, key=lambda x: -x[2])[:6]}
    for tid, rr, v, srv in saingan:
        x, y = t.at[tid, "x_px"], t.at[tid, "y_px"]
        warna = KATEGORI["ap_l5" if lantai_of.get(rr) == 5 else "ap_l3"][1]
        ax.scatter(x, y, s=max(20, (v + 95) * 9), color=warna, alpha=0.55, edgecolors="black", zorder=4)
        if v >= -75:
            ax.annotate("%s: L%d ch%d %.0f\n(AP L4 %.0f, selisih %.0f dB)" % (tid[3:], lantai_of.get(rr, 0), kanal.at[rr, "ch"], v, srv, srv - v),
                        (x, y), xytext=(10, 6), textcoords="offset points", fontsize=8, weight="bold", zorder=6,
                        bbox=dict(fc="white", ec=warna, alpha=0.9, boxstyle="round,pad=0.2"))
    S.gambar_ap(ax, ap, {k: int(kanal.at[a.radio, "ch"]) for k, a in ap.iterrows()}, ukuran=10)
    S.batas(ax, w, h)
    ax.set_title("Sinyal AP lantai 3 (oranye) dan lantai 5 (merah) yang terdengar di titik lantai 4\n"
                 "ukuran lingkaran = kekuatan sinyal; label = 6 titik dengan sinyal lantai lain terkuat (lengkap: floor_bleed_L4.csv)", fontsize=11)
    ax2 = fig.add_axes([0.63, 0.12, 0.36, 0.72])
    v = fb[fb.redaman_lantai_db != ""].copy()
    v["redaman_lantai_db"] = v.redaman_lantai_db.astype(float)
    v = v.sort_values("redaman_lantai_db")
    lbl = ["L%d ch%d (%s)" % (r.lantai_asal, r.kanal, r.titik_terkuat_asal) for _, r in v.iterrows()]
    ax2.barh(range(len(v)), v.redaman_lantai_db, color=[KATEGORI["ap_l5" if l == 5 else "ap_l3"][1] for l in v.lantai_asal], edgecolor="black")
    ax2.set_yticks(range(len(v)), lbl, fontsize=8)
    ax2.axvspan(20, 30, color="#d9f0d3", zorder=0)
    ax2.text(25, len(v) - 0.6, "pustaka:\npelat beton 20-30+ dB", ha="center", fontsize=8, va="top")
    for i, r in enumerate(v.itertuples()):
        ax2.text(r.redaman_lantai_db + 0.5, i, "%.0f" % r.redaman_lantai_db, va="center", fontsize=8)
    ax2.set_xlabel("selisih RSSI lantai asal - lantai 4 di titik yang tegak lurus (dB)")
    ax2.set_title("Estimasi redaman pelat lantai\n(RSSI L3/L5 sudah dikoreksi offset laptop: L3 +%.1f dB, L5 +%.1f dB)" % (-k3, -k5), fontsize=10)
    fig.savefig(os.path.join(OUT, "8_floor_bleed_L4.png"), dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---------- validasi rencana kanal ----------
    rencana = pd.read_csv(os.path.join(OUT, "rencana_AP_kanal_L4.csv")).set_index("ap")
    P, n, _ = S.pasang_model(rssi, xy, ap)
    P_baru = float(np.median([P[k] for k in ap.index if k in S.UTAMA]))
    plafon = float(max(rssi[a.radio].max() for k, a in ap.iterrows() if k in S.UTAMA))
    tabel = pd.DataFrame({k: rssi_all[a.radio] for k, a in ap.iterrows()}).fillna(-100)
    for k, _, x, y in S.AP_BARU:
        d = np.maximum(np.hypot(xy.x_px - x, xy.y_px - y) / S.SCALE, 1.0)
        tabel[k] = np.minimum(P_baru - 10 * n * np.log10(d), plafon).reindex(tabel.index)
    val = []
    for nama, kol in (("sekarang", "kanal_sekarang"), ("usulan", "kanal_usulan")):
        pl = rencana[kol].dropna().astype(int).to_dict()
        for ch in sorted(set(pl.values())):
            anggota = [k for k, c in pl.items() if c == ch]
            lain = rad[(rad.kat != "ap_l4") & rad.kanal_terpakai.str.split().apply(lambda s: str(ch) in s)]
            bareng = 0
            if len(anggota) > 1:
                cols = tabel[anggota]
                bareng = int(((cols >= S.DENGAR).sum(axis=1) >= 2).sum())
            val.append(dict(rencana=nama, kanal=ch, ap_L4=" + ".join(anggota),
                            titik_AP_sekanal_terdengar_bersama=bareng,
                            radio_lain_di_kanal_ini=len(lain), radio_lain_terkuat_dbm=round(lain.rssi_maks_L4.max(), 1) if len(lain) else ""))
    pd.DataFrame(val).to_csv(os.path.join(OUT, "validasi_kanal_L4.csv"), index=False)

    # ---------- spreadsheet controller vs survei (tanpa IP/MAC) ----------
    sp = os.path.join(HERE, "..", "RuckusAPList.csv")
    if os.path.exists(sp):
        def kunci(m):
            b = [int(x, 16) for x in m.split(":")]
            return (b[0], b[1], b[2], b[3] & 0x3F, b[4], b[5] & 0xF0)
        idx = {kunci(r): r for r in rad.radio}
        bs = []
        for r in csv.DictReader(open(sp, encoding="utf-8-sig")):
            if not r["AP Name"].upper().startswith("F4"):
                continue
            m = idx.get(kunci(r["AP MAC"]))
            bs.append(dict(nama_di_spreadsheet=r["AP Name"], kanal_5g_spreadsheet=r["Channel (5G)"],
                           klien_spreadsheet=r["Clients"], airtime_5g_pct=r["Airtime Utilization (5G)"],
                           terakhir_terlihat=r["Last Seen"],
                           ditemukan_saat_survei="ya" if m else "TIDAK",
                           kode_ap_survei=kode.get(m, "") if m else "",
                           kanal_terukur=int(kanal.at[m, "ch"]) if m else "",
                           titik_terkuat=rad.set_index("radio").at[m, "titik_L4"] if m else ""))
        pd.DataFrame(bs).sort_values("nama_di_spreadsheet").to_csv(os.path.join(OUT, "banding_spreadsheet_L4.csv"), index=False)

    # ---------- 9. timeline roaming R2 + uji aktif ----------
    timeline(kode)

    print("Total CCI:", total, "| radio terdengar di L4:", len(rad), rad.kat.value_counts().to_dict())
    print(kej.groupby("asal_pengganggu").size().to_string())
    print(fb.to_string(index=False))
    print(pd.DataFrame(val).to_string(index=False))
    print("Tersimpan di", OUT)


def timeline(kode):
    import re
    from datetime import datetime
    raw = os.path.join(HERE, "raw")
    jam = lambda x: datetime.strptime("2026-10-11 " + x, "%Y-%m-%d %H:%M:%S")
    roam = pd.read_csv(os.path.join(raw, "roaming_L4_R2.csv"))
    roam["t"] = roam.waktu.map(jam)
    teks = open(os.path.join(raw, "roaming_ping_L4_R2.txt"), encoding="utf-16").read().splitlines()
    ok, rto = [], []
    for l in teks:
        m = re.match(r"(\d\d:\d\d:\d\d) (.*)", l)
        if not m:
            continue
        r = re.search(r"time[=<]([\d.]+)ms", m.group(2))
        if r:
            ok.append((jam(m.group(1)), float(r.group(1))))
        elif re.search("timed out|unreachable|failure", m.group(2), re.I):
            rto.append(jam(m.group(1)))
    akt = pd.read_csv(os.path.join(HERE, "data", "active_L4.csv"))
    # uji aktif yang gagal (DNS) sudah dihapus dari active_L4.csv; jamnya dicatat di sini dari log uji pertama
    gagal_dns = [("11:19:47", "203"), ("11:20:40", "006"), ("11:20:53", "007"), ("11:21:10", "007"),
                 ("11:24:41", "101"), ("11:25:18", "106")]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(17, 8), sharex=True, gridspec_kw=dict(height_ratios=[1.1, 1]))
    nama = roam.bssid.map(lambda b: kode.get(str(b).lower(), "putus" if str(b).startswith("00:00") else "lain"))
    urut = sorted(set(nama), key=lambda x: (not x.startswith("AP-"), x in S.UTAMA, x))
    ypos = {n: i for i, n in enumerate(urut)}
    a1.step(roam.t, nama.map(ypos), where="post", color="#1f77b4", lw=2)
    for _, r in roam[roam.pindah == "YA"].iterrows():
        a1.axvline(r.t, color="#999", lw=0.8, ls=":")
    a1.set_yticks(range(len(urut)), urut)
    a1.set_ylabel("AP yang dipakai laptop")
    a1.set_title("Uji roaming R2 + uji aktif lantai 4 (11:13-11:40): AP yang tersambung, ping, dan uji aktif", fontsize=12)
    for j, tt in gagal_dns:
        a1.scatter(jam(j), len(urut) - 0.4, marker="x", color="red", s=70, zorder=5)
        a1.annotate(tt, (jam(j), len(urut) - 0.4), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8, color="red")
    for _, r in akt.iterrows():
        tm = datetime.strptime(r.timestamp, "%Y-%m-%dT%H:%M:%S")
        if tm.hour == 11:
            a1.scatter(tm, len(urut) - 0.4, marker="o", color="green", s=50, zorder=5)
            a1.annotate(r.titik_id[3:], (tm, len(urut) - 0.4), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=8, color="green")
    a1.set_ylim(-0.6, len(urut) + 0.3)
    if ok:
        a2.scatter([x for x, _ in ok], [y for _, y in ok], s=12, color="green", label="ping berhasil (RTT)")
    a2.scatter(rto, [1100] * len(rto), marker="x", color="red", s=30, label="ping gagal (Request timed out)")
    if rto:
        a2.axvspan(min(r for r in rto if r.minute >= 22), jam("11:25:31"), color="#fdd0c8", alpha=0.6, zorder=0)
        a2.text(jam("11:23:50"), 900, "38 dari 55 ping gagal (69%), 11:22-11:25\n(laptop masih tersambung ke AP)", ha="center", fontsize=9, color="#a50026")
        a2.axvline(jam("11:25:31"), color="black", lw=1.2)
        a2.text(jam("11:25:31"), 1150, " reconnect manual", fontsize=9)
    a2.axvspan(jam("11:19:47"), jam("11:21:10"), color="#fdd0c8", alpha=0.35, zorder=0)
    a2.set_ylabel("RTT ping (ms)")
    a2.set_ylim(0, 1250)
    a2.legend(loc="upper left", fontsize=9)
    a2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M"))
    a1.legend(handles=[Line2D([], [], marker="x", ls="", color="red", label="uji aktif gagal (DNS tidak ditemukan, loss 100%)"),
                       Line2D([], [], marker="o", ls="", color="green", label="uji aktif berhasil")], loc="lower right", fontsize=9)
    fig.text(0.01, 0.005, "Ping R2 baru dimulai 11:21:57. Uji aktif pertama (x merah) gagal saat laptop tersambung ke AP-F4.6/AP-F4.13; "
             "diulang 11:34-11:39 (o hijau) setelah reconnect dan berhasil semua.", fontsize=9)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "9_timeline_roaming_L4.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
