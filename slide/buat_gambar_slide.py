"""Potong gambar hasil analisis (kelompok6/output) menjadi versi slide di slide/img/.

Judul matplotlib dibuang (judul sudah ada di slide) dan gambar gabungan dipisah per panel.
Jalankan ulang setiap kali solusi_L4.py / bukti_L4.py dijalankan ulang:
    python slide/buat_gambar_slide.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SOL = ROOT / "kelompok6" / "output" / "solusi_L4"
DENAH = ROOT / "kelompok6" / "denah"
IMG = ROOT / "slide" / "img"
FOTO = ROOT / "slide" / "foto"

# nama_output: (file sumber, (x0, y0, x1, y1) dalam pecahan lebar/tinggi gambar sumber)
POTONG = {
    "peta_titik": (DENAH / "peta_titik_L4_rev.png", (0, 0.045, 1, 1)),
    "heatmap": (SOL / "1_heatmap_AP_L4.png", (0, 0.05, 1, 1)),
    "area_ap": (SOL / "2_posisi_area_AP_L4.png", (0, 0.06, 1, 1)),
    "kanal_peta": (SOL / "3_kanal_L4.png", (0, 0.063, 0.675, 1)),
    "solusi_peta": (SOL / "4_solusi_L4.png", (0, 0.092, 0.705, 1)),
    "prediksi": (SOL / "5_prediksi_sebelum_sesudah_L4.png", (0, 0.123, 1, 1)),
    "bukti_cci": (SOL / "6_bukti_cci_L4.png", (0, 0.066, 1, 1)),
    "radio_kanal": (SOL / "7_radio_per_kanal_L4.png", (0, 0.044, 0.57, 1)),
    "floor_peta": (SOL / "8_floor_bleed_L4.png", (0, 0.07, 0.575, 1)),
    "timeline_roaming": (SOL / "9_timeline_roaming_L4.png", (0, 0.04, 1, 0.955)),
    "web_pengguna": (SOL / "10_web_pengguna_L4.png", (0, 0, 1, 1)),
    "web_airtime": (SOL / "11_web_airtime_L4.png", (0, 0, 1, 1)),
}


def rapikan(im, pad=12, ambang=245):
    """Buang tepi putih, sisakan margin `pad` piksel."""
    a = np.asarray(im.convert("L"))
    ys, xs = np.where(a < ambang)
    if len(xs) == 0:
        return im
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, im.width)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, im.height)
    return im.crop((x0, y0, x1, y1))


def potong():
    IMG.mkdir(parents=True, exist_ok=True)
    for nama, (src, (x0, y0, x1, y1)) in POTONG.items():
        im = Image.open(src).convert("RGB")
        w, h = im.size
        im = rapikan(im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h))))
        im.save(IMG / f"{nama}.png", optimize=True)
        print(f"{nama:18s} {im.size}")


def redaman():
    """Gambar ulang grafik redaman pelat lantai (panel kanan gambar 8) dengan huruf besar untuk slide."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    import pandas as pd

    for f in (ROOT / "slide" / "fonts").glob("Poppins-*.ttf"):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({"font.family": "Poppins", "font.size": 15})

    v = pd.read_csv(SOL / "floor_bleed_L4.csv").dropna(subset=["redaman_lantai_db"])
    v = v.sort_values("redaman_lantai_db")
    lbl = ["L%d ch%d\n%s ke L4-%s" %(r.lantai_asal, r.kanal, r.titik_terkuat_asal, r.titik_terkuat_asal[3:])
           for r in v.itertuples()]
    fig, ax = plt.subplots(figsize=(7, 4.6), dpi=200)
    ax.axvspan(20, 30, color="#e7e7e2", zorder=0)
    ax.text(25, len(v) - 0.28, "pustaka: 20–30 dB", ha="center", va="center", fontsize=12, color="#555")
    ax.set_ylim(-0.5, len(v) - 0.1)
    warna = ["#e30613" if x < 20 else "#111111" for x in v.redaman_lantai_db]
    ax.barh(range(len(v)), v.redaman_lantai_db, color=warna, height=0.6)
    for i, x in enumerate(v.redaman_lantai_db):
        ax.text(x + 0.6, i, "%.0f dB" % x, va="center", fontsize=15, fontweight="bold")
    ax.set_yticks(range(len(v)), lbl, fontsize=13)
    ax.set_xlim(0, 36)
    ax.set_xlabel("redaman pelat lantai (dB, sudah dikoreksi offset laptop)", fontsize=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(IMG / "floor_redaman.png", facecolor="white")
    plt.close(fig)
    print("floor_redaman      (digambar ulang)")


def titik_data():
    """Denah L4 + 39 titik ukur: nomor titik, RSSI AP terkuat, warna status, dan titik uji aktif."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.lines import Line2D
    import pandas as pd

    for f in (ROOT / "slide" / "fonts").glob("Poppins-*.ttf"):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({"font.family": "Poppins"})

    K = ROOT / "kelompok6"
    img = plt.imread(K / "denah" / "denah_L4.png")
    h, w = img.shape[:2]
    t = pd.read_csv(K / "output" / "L4_titik.csv")
    ap = pd.read_csv(K / "data" / "ap_fisik_L4.csv")
    aktif = set(pd.read_csv(K / "data" / "active_L4.csv").titik_id)
    warna = {"BAIK": "#1a9850", "PERHATIAN": "#f2a900", "BURUK": "#e30613"}

    fig, ax = plt.subplots(figsize=(12, 6.9), dpi=200)
    ax.imshow(img, alpha=0.55)
    for a in ap.itertuples():
        ax.scatter(a.x_px, a.y_px, marker="^", s=190, c="#121212", zorder=4)
        ax.annotate(a.ap_id, (a.x_px, a.y_px), xytext=(-34, 8) if a.ap_id == "AP-F4.4" else (0, -17), textcoords="offset points",
                    ha="center", fontsize=9, color="#121212", zorder=4)
    for r in t.itertuples():
        if r.titik_id in aktif:
            ax.scatter(r.x_px, r.y_px, s=420, facecolors="none", edgecolors="#121212", linewidths=1.8, zorder=5)
        ax.scatter(r.x_px, r.y_px, s=150, c=warna[r.status], edgecolors="white", linewidths=1, zorder=6)
        ax.annotate("%s\n%.0f" % (r.titik_id[3:], r.rssi1), (r.x_px, r.y_px), xytext=(8, 2), textcoords="offset points",
                    fontsize=10.5, fontweight="bold", va="center", linespacing=0.95, zorder=7,
                    bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.8))
    n = t.status.value_counts()
    ax.legend(handles=[Line2D([], [], marker="o", ls="", mfc=warna[s], mec="white", ms=10, label="%s (%d)" % (s, n.get(s, 0)))
                       for s in warna] +
                      [Line2D([], [], marker="o", ls="", mfc="none", mec="#121212", mew=1.6, ms=14, label="uji aktif (8 titik)"),
                       Line2D([], [], marker="^", ls="", mfc="#121212", mec="#121212", ms=10, label="AP 5 GHz")],
              loc="lower left", fontsize=10.5, title="nomor titik / RSSI (dBm)", title_fontsize=10.5, frameon=True, framealpha=0.95, edgecolor="#121212", fancybox=False)
    ax.set_xlim(60, w - 40)
    ax.set_ylim(h - 60, 70)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(IMG / "titik_data.png", facecolor="white", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("titik_data         (digambar)")


def foto_placeholder():
    """Kotak abu-abu 3:4 untuk foto anggota yang belum ada (file *anggotaN.* apa pun dianggap sudah ada)."""
    FOTO.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype(str(ROOT / "slide" / "fonts" / "BebasNeue-Regular.ttf"), 90)
    except OSError:
        font = ImageFont.load_default()
    for i in range(1, 5):
        p = FOTO / f"anggota{i}.jpg"
        if p.exists() or any(FOTO.glob(f"*anggota{i}.*")):
            continue
        im = Image.new("RGB", (600, 800), "#d9d9d4")
        d = ImageDraw.Draw(im)
        d.text((300, 400), f"FOTO\nANGGOTA {i}", fill="#8c8c8c", font=font, anchor="mm", align="center", spacing=4)
        im.save(p, quality=90)
        print("placeholder", p.name)


if __name__ == "__main__":
    potong()
    redaman()
    titik_data()
    foto_placeholder()
