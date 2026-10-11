#!/usr/bin/env python3
"""
survei.py - scan Wi-Fi per titik sesuai nomor di peta (data/titik_L{n}.csv).
Nama laptop diambil otomatis dari nama komputer (dipakai untuk offset kalibrasi).

  python survei.py --kalibrasi                            # semua laptop barengan di hall L4 (titik merah 000)
  python survei.py --offset                               # hitung offset antar-laptop (setelah semua push)
  python survei.py --lantai 4 --point 001                 # scan satu titik
  python survei.py --lantai 4 --point 015 --catatan "kelas, 30 orang, pintu tutup"
  python survei.py --lantai 4 --ap F4.2                   # berdiri di bawah AP: petakan BSSID-nya
  python survei.py --lantai 4 --rekap                     # titik yang sudah / belum

Hasil:  data/passive_L{n}.csv   (data mentah, dipakai analyze.py)
        data/rekap_L{n}.csv     (RSSI terkuat per titik, bisa dibuka di Excel)
        data/map_bssid_L{n}.csv, data/kalibrasi_<laptop>.csv, data/offset_kalibrasi.csv
Titik yang di-scan ulang otomatis menggantikan data lamanya.
"""
import argparse
import csv
import glob
import math
import os
import socket
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
LAPTOP = (os.environ.get("COMPUTERNAME") or socket.gethostname()).lower()


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


def rata_linear(vs):
    return 10 * math.log10(sum(10 ** (v / 10) for v in vs) / len(vs))


def rssi_per_bssid(rows, ssid=None):
    """{(bssid, kanal): rata-rata linear RSSI} untuk radio 5 GHz (opsional: hanya SSID tertentu)."""
    kumpul = {}
    for r in rows:
        if r["band"] == "5" and (ssid is None or r["ssid"] == ssid):
            kumpul.setdefault((r["bssid"], r["channel"]), []).append(float(r["rssi_dbm"]))
    return {k: rata_linear(vs) for k, vs in kumpul.items()}


def scan(tid, lantai, out, n, catatan, slot, ssid):
    cmd = [sys.executable, os.path.join(HERE, "scan_point.py"), "--titik", tid, "--lantai", lantai,
           "--slot", slot, "--device", LAPTOP, "--out", out, "--n", str(n), "--ssid", ssid, "--catatan", catatan]
    if subprocess.call(cmd) != 0:
        print("!! Scan %s gagal. Jalankan perintah yang sama sekali lagi." % tid)
        return False
    return True


def tulis_rekap(out, rekap, titik, ssid):
    semua = baca(out)
    per_titik = {}
    for r in semua:
        per_titik.setdefault(r["titik_id"], []).append(r)
    baris = []
    for t in titik:
        tid = t["titik_id"]
        rows = per_titik.get(tid)
        if not rows:
            baris.append([tid, t["keterangan"], "", "", "", "", "", "", "", "BELUM DISCAN"])
            continue
        urut = sorted(rssi_per_bssid(rows, ssid).items(), key=lambda kv: kv[1], reverse=True)
        if urut:
            (b1, ch1), r1 = urut[0]
            r2 = "%.0f" % urut[1][1] if len(urut) > 1 else ""
            baris.append([tid, t["keterangan"], "%.0f" % r1, ch1, b1, r2, len(urut),
                          rows[0]["catatan"], rows[0]["device"], rows[0]["timestamp"]])
        else:
            baris.append([tid, t["keterangan"], "TIDAK TERDETEKSI", "", "", "", 0,
                          rows[0]["catatan"], rows[0]["device"], rows[0]["timestamp"]])
    with open(rekap, "w", encoding="utf-8-sig", newline="") as fh:  # utf-8-sig: aman dibuka di Excel
        w = csv.writer(fh)
        w.writerow(["titik_id", "lokasi", "rssi_terkuat_dbm", "kanal", "bssid_terkuat", "rssi_cadangan_dbm",
                    "jumlah_radio_" + ssid, "catatan", "laptop", "waktu"])
        w.writerows(baris)
    return baris


def kalibrasi(a):
    out = os.path.join(DATA, "kalibrasi_%s.csv" % LAPTOP)
    if os.path.exists(out):
        print("Kalibrasi laptop ini sudah ada -> diganti dengan scan baru.")
        os.remove(out)
    print("KALIBRASI di L4-000 (hall sisi A) | laptop: %s | scan 5x (+-40 detik)\n" % LAPTOP)
    if scan("L4-000", "4", out, 5, a.catatan or "kalibrasi", a.slot, a.ssid):
        print("\n>> Tersimpan: %s" % os.path.relpath(out, HERE))
        print(">> Setelah semua laptop kalibrasi dan push: python survei.py --offset")


def offset():
    files = sorted(glob.glob(os.path.join(DATA, "kalibrasi_*.csv")))
    data = {}
    for f in files:
        rows = baca(f)
        if rows:
            data[rows[0]["device"]] = rssi_per_bssid(rows)
    if len(data) < 2:
        sys.exit("Butuh minimal 2 file data/kalibrasi_*.csv (ada %d). git pull dulu." % len(data))
    acuan = LAPTOP if LAPTOP in data else sorted(data)[0]
    hasil = []
    for dev in sorted(data):
        sama = sorted(set(data[dev]) & set(data[acuan]))
        selisih = [data[dev][k] - data[acuan][k] for k in sama]
        med = statistics.median(selisih) if selisih else float("nan")
        hasil.append([dev, acuan, "%.1f" % med, len(sama)])
    out = os.path.join(DATA, "offset_kalibrasi.csv")
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["laptop", "acuan", "offset_db_median", "jumlah_bssid_sama"])
        w.writerows(hasil)
    print("Offset RSSI terhadap laptop acuan '%s' (median selisih BSSID 5 GHz yang sama):" % acuan)
    for dev, _, med, n in hasil:
        print("  %-20s %+6s dB  (%d BSSID)" % (dev, med, n))
    print("Positif = laptop itu membaca sinyal lebih kuat. Tersimpan: %s" % os.path.relpath(out, HERE))


def petakan_ap(a):
    nama = a.ap.strip().upper()
    out = os.path.join(DATA, "map_bssid_L%s.csv" % a.lantai)
    tid = "L%s-AP-%s" % (a.lantai, nama)
    hapus_titik(out, tid)
    print("Petakan BSSID %s | berdiri tepat di bawah AP\n" % tid)
    if not scan(tid, a.lantai, out, 3, a.catatan, a.slot, a.ssid):
        return
    urut = sorted(rssi_per_bssid([r for r in baca(out) if r["titik_id"] == tid], a.ssid).items(),
                  key=lambda kv: kv[1], reverse=True)[:3]
    print("\n>> Kandidat BSSID AP %s (yang paling kuat = AP di atas kepala):" % nama)
    for (b, ch), r in urut:
        print("     %s  ch %-4s %.0f dBm" % (b, ch, r))
    print(">> Tulis BSSID teratas di samping AP di peta.")


def main():
    p = argparse.ArgumentParser(description="Survei Wi-Fi per titik. Contoh: python survei.py --lantai 4 --point 001")
    p.add_argument("--lantai", choices=["3", "4", "5"])
    p.add_argument("--point", help="nomor titik di peta, mis. 001, 105, 201")
    p.add_argument("--catatan", default="", help='mis. "kelas, 30 orang, pintu tutup"')
    p.add_argument("--rekap", action="store_true", help="tampilkan titik yang sudah / belum discan")
    p.add_argument("--kalibrasi", action="store_true", help="scan kalibrasi di L4-000 (semua laptop barengan)")
    p.add_argument("--offset", action="store_true", help="hitung offset antar-laptop dari data/kalibrasi_*.csv")
    p.add_argument("--ap", help="petakan BSSID AP, mis. --ap F4.2 (berdiri di bawah AP)")
    p.add_argument("--slot", default="T1", help="T2 untuk survei ulang jam sibuk")
    p.add_argument("--ssid", default="WiFi-UB.x")
    a = p.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace", line_buffering=True)  # urutan cetak = urutan kejadian

    if a.kalibrasi:
        return kalibrasi(a)
    if a.offset:
        return offset()
    if not a.lantai:
        p.error("isi --lantai (3/4/5). Contoh: python survei.py --lantai 4 --point 001")
    if a.ap:
        return petakan_ap(a)

    akhiran = "" if a.slot == "T1" else "_" + a.slot
    out = os.path.join(DATA, "passive_L%s%s.csv" % (a.lantai, akhiran))
    rekap = os.path.join(DATA, "rekap_L%s%s.csv" % (a.lantai, akhiran))
    titik = baca(os.path.join(DATA, "titik_L%s.csv" % a.lantai))

    if a.point:
        tid = id_titik(a.point, a.lantai)
        t = next((t for t in titik if t["titik_id"] == tid), None)
        if t is None:
            p.error("titik %s tidak ada di peta lantai %s. Titik yang ada: %s"
                    % (tid, a.lantai, ", ".join(x["titik_id"][3:] for x in titik)))
        if tid in sudah_discan(out):
            print("%s sudah pernah discan -> data lamanya diganti dengan scan ini." % tid)
            hapus_titik(out, tid)
        print("%s  -  %s  | laptop: %s\n" % (tid, t["keterangan"], LAPTOP))
        n = 5 if tid.endswith("-000") else 3
        if scan(tid, a.lantai, out, n, a.catatan, a.slot, a.ssid):
            b = next(b for b in tulis_rekap(out, rekap, titik, a.ssid) if b[0] == tid)
            print("\n>> %s: %s dBm (ch %s) -> tersimpan. Pindah ke titik berikutnya." % (tid, b[2], b[3]))
    elif not a.rekap:
        p.error("isi --point. Contoh: python survei.py --lantai %s --point 001" % a.lantai)

    baris = tulis_rekap(out, rekap, titik, a.ssid)
    if a.rekap:
        print("Rekap lantai %s (%s):" % (a.lantai, os.path.relpath(rekap, HERE)))
        for b in baris:
            if b[-1] != "BELUM DISCAN":
                print("  %-7s %-6s ch %-4s %s" % (b[0][3:], b[2] if b[2] != "TIDAK TERDETEKSI" else "-", b[3], b[1]))
    belum = [b[0][3:] for b in baris if b[-1] == "BELUM DISCAN"]
    print("Belum discan (%d): %s" % (len(belum), ", ".join(belum) if belum else "tidak ada - LANTAI %s SELESAI" % a.lantai))


if __name__ == "__main__":
    main()
