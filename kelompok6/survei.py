#!/usr/bin/env python3
"""
survei.py - pemandu survei pasif: jalan dari titik ke titik sesuai data/titik_L{n}.csv
dan memanggil scan_point.py di setiap titik.

  python survei.py --lantai 4 --device ghazy --bagian main   # L4 gedung utama, urut titik
  python survei.py --lantai 4 --device bagas --bagian ext    # L4 gedung Ext
  python survei.py --lantai 3 --device bagas                 # semua titik L3
  python survei.py --lantai 4 --device ghazy --slot T2       # survei ulang jam sibuk
  python survei.py --lantai 4 --device ghazy --point 001     # scan satu titik (nomor di peta)
  python survei.py --lantai 4 --device ghazy --point 001 --catatan "kelas, 30 orang"
  python survei.py --lantai 4 --device ghazy --rekap         # lihat rekap saja, tanpa scan

Hasil: data/passive_L{n}_{device}.csv (slot T2: data/passive_L{n}_{device}_T2.csv).
Rekap otomatis (RSSI terkuat per titik, bisa dibuka di Excel):
       data/rekap_L{n}_{device}.csv (slot T2: data/rekap_L{n}_{device}_T2.csv).
Mode urut: Enter = scan, ketik catatan lalu Enter = scan + catatan,
s = lewati titik, q = berhenti (jalankan lagi untuk melanjutkan).
Mode --point: titik yang sudah pernah discan akan di-scan ulang (data lamanya diganti).
"""
import argparse
import csv
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def baca(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def sudah_discan(path):
    return {r["titik_id"] for r in baca(path)}


def hapus_titik(path, tid):
    """Buang data lama satu titik supaya scan ulang tidak dobel."""
    rows = baca(path)
    sisa = [r for r in rows if r["titik_id"] != tid]
    if len(sisa) == len(rows):
        return
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(sisa)


def id_titik(point, lantai):
    """'1' / '001' / 'L4-001' -> 'L4-001'."""
    point = point.strip().upper()
    if point.startswith("L"):
        return point
    return "L%s-%03d" % (lantai, int(point)) if point.isdigit() else "L%s-%s" % (lantai, point)


def tulis_rekap(out, rekap, titik, ssid):
    """RSSI terkuat SSID kampus (5 GHz) per titik, rata-rata linear antar-scan per BSSID."""
    per_titik = {}
    for r in baca(out):
        if r["ssid"] != ssid or r["band"] != "5":
            continue
        d = per_titik.setdefault(r["titik_id"], {"bssid": {}, "catatan": r["catatan"], "waktu": r["timestamp"]})
        d["bssid"].setdefault((r["bssid"], r["channel"]), []).append(float(r["rssi_dbm"]))
    semua = {r["titik_id"]: r for r in baca(out)}
    baris = []
    for t in titik:
        tid = t["titik_id"]
        d = per_titik.get(tid)
        if d:
            rata = {k: 10 * math.log10(sum(10 ** (v / 10) for v in vs) / len(vs)) for k, vs in d["bssid"].items()}
            urut = sorted(rata.items(), key=lambda kv: kv[1], reverse=True)
            (b1, ch1), r1 = urut[0]
            r2 = "%.0f" % urut[1][1] if len(urut) > 1 else ""
            baris.append([tid, t["keterangan"], "%.0f" % r1, ch1, b1, r2, len(urut), d["catatan"], d["waktu"]])
        elif tid in semua:
            baris.append([tid, t["keterangan"], "TIDAK TERDETEKSI", "", "", "", 0,
                          semua[tid]["catatan"], semua[tid]["timestamp"]])
        else:
            baris.append([tid, t["keterangan"], "", "", "", "", "", "", "BELUM DISCAN"])
    with open(rekap, "w", encoding="utf-8-sig", newline="") as fh:  # utf-8-sig: aman dibuka di Excel
        w = csv.writer(fh)
        w.writerow(["titik_id", "lokasi", "rssi_terkuat_dbm", "kanal", "bssid_terkuat",
                    "rssi_cadangan_dbm", "jumlah_radio_" + ssid, "catatan", "waktu"])
        w.writerows(baris)
    return baris


def cetak_rekap(baris, rekap):
    print("\nRekap (%s):" % os.path.relpath(rekap, HERE))
    print("  %-8s %-6s %-4s %s" % ("titik", "dBm", "ch", "lokasi"))
    for b in baris:
        if b[-1] != "BELUM DISCAN":
            print("  %-8s %-6s %-4s %s" % (b[0], b[2] if b[2] != "TIDAK TERDETEKSI" else "-", b[3], b[1]))


def scan(t, a, out, catatan):
    tid = t["titik_id"]
    n = 5 if tid.endswith("-000") else 3
    cmd = [sys.executable, os.path.join(HERE, "scan_point.py"), "--titik", tid, "--lantai", a.lantai,
           "--slot", a.slot, "--device", a.device.lower(), "--out", out, "--n", str(n),
           "--ssid", a.ssid, "--catatan", catatan]
    if subprocess.call(cmd) != 0:
        print("!! Scan %s gagal. Ulangi titik ini.\n" % tid)
        return False
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lantai", required=True, choices=["3", "4", "5"])
    p.add_argument("--device", required=True, help="nama pemegang laptop, mis. ghazy / bagas")
    p.add_argument("--bagian", default="semua", choices=["main", "ext", "semua"])
    p.add_argument("--slot", default="T1")
    p.add_argument("--ssid", default="WiFi-UB.x")
    p.add_argument("--point", help="scan satu titik saja, nomor sesuai peta (mis. 001, 105, L4-001)")
    p.add_argument("--catatan", default="", help="catatan untuk --point (mis. \"kelas, 30 orang, pintu tutup\")")
    p.add_argument("--rekap", action="store_true", help="tampilkan rekap saja, tanpa scan")
    a = p.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    titik_csv = os.path.join(HERE, "data", "titik_L%s.csv" % a.lantai)
    akhiran = "" if a.slot == "T1" else "_" + a.slot
    nama = "L%s_%s%s.csv" % (a.lantai, a.device.lower(), akhiran)
    out = os.path.join(HERE, "data", "passive_" + nama)
    rekap = os.path.join(HERE, "data", "rekap_" + nama)

    semua = baca(titik_csv)
    titik = [t for t in semua if a.bagian in ("semua", t["jenis_area"])]

    if a.rekap:
        cetak_rekap(tulis_rekap(out, rekap, semua, a.ssid), rekap)
        return

    if a.point:
        tid = id_titik(a.point, a.lantai)
        t = next((t for t in semua if t["titik_id"] == tid), None)
        if t is None:
            p.error("titik %s tidak ada di %s. Titik yang ada: %s"
                    % (tid, os.path.relpath(titik_csv, HERE), ", ".join(x["titik_id"] for x in semua)))
        if tid in sudah_discan(out):
            print("%s sudah pernah discan -> data lamanya diganti dengan scan ini." % tid)
            hapus_titik(out, tid)
        print("%s  -  %s" % (tid, t["keterangan"]))
        ok = scan(t, a, out, a.catatan)
        baris = tulis_rekap(out, rekap, semua, a.ssid)
        if ok:
            b = next(b for b in baris if b[0] == tid)
            print(">> %s: %s dBm (ch %s) -> tersimpan di %s" % (tid, b[2], b[3], os.path.relpath(rekap, HERE)))
        belum = [x["titik_id"] for x in titik if x["titik_id"] not in sudah_discan(out)]
        print("Sisa titik (%s): %s" % (a.bagian, ", ".join(belum) if belum else "tidak ada - SEMUA SELESAI"))
        return

    selesai = sudah_discan(out)
    sisa = [t for t in titik if t["titik_id"] not in selesai]
    print("Lantai %s (%s) | file %s | %d titik, %d sudah, %d sisa\n"
          % (a.lantai, a.bagian, os.path.relpath(out, HERE), len(titik), len(titik) - len(sisa), len(sisa)))

    try:
        for i, t in enumerate(sisa, 1):
            tid = t["titik_id"]
            jarak = t.get("jarak_dari_sebelumnya_m") or "-"
            print("=" * 64)
            print("[%d/%d] %s  -  %s  (jarak dari titik sebelumnya: %s m)" % (i, len(sisa), tid, t["keterangan"], jarak))
            jawab = input("Berdiri di titik. Enter=scan | ketik catatan+Enter | s=lewati | q=berhenti: ").strip()
            if jawab.lower() == "q":
                break
            if jawab.lower() == "s":
                print("Dilewati: %s (tulis alasannya di kertas)\n" % tid)
                continue
            if scan(t, a, out, jawab):
                tulis_rekap(out, rekap, semua, a.ssid)
                print(">> Tersimpan. Pindah ke titik berikutnya.\n")
    except (KeyboardInterrupt, EOFError):
        print("\nDihentikan. Titik yang sudah discan tetap tersimpan.")

    cetak_rekap(tulis_rekap(out, rekap, semua, a.ssid), rekap)
    belum = [t["titik_id"] for t in titik if t["titik_id"] not in sudah_discan(out)]
    print("Belum discan: %s" % (", ".join(belum) if belum else "tidak ada - SEMUA TITIK SELESAI"))


if __name__ == "__main__":
    main()
