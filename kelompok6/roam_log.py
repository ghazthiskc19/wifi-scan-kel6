#!/usr/bin/env python3
"""
roam_log.py - catat BSSID, sinyal, dan ping setiap detik selama uji roaming (jalan sepanjang koridor).
Hentikan dengan Ctrl+C. Satu perintah saja, ping sudah ikut dicatat.

  Windows: python roam_log.py --out raw\\roaming_L4_R2.csv
  Linux  : python3 roam_log.py --iface wlan0 --out raw/roaming_L4_R2.csv

Setiap pindah AP otomatis dicatat: AP lama -> AP baru (nama dari data/map_bssid_L*.csv) dan
perkiraan lokasi (titik survei tempat AP baru paling kuat, dari data/passive_L*.csv).
Ringkasan perpindahan + RTO ditulis ke <out>_ringkasan.txt saat Ctrl+C.

Windows hanya memberi kualitas sinyal (%) tanpa scan; kolom rssi_dbm diisi aproksimasi
(persen/2 - 100) dan ditandai 'aprox' di kolom sumber.
"""
import argparse
import csv
import glob
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime

OS = os.environ.get("SURVEY_OS", sys.platform)  # "linux" / "win32" / "darwin"
HERE = os.path.dirname(os.path.abspath(__file__))

from active_point import parse_link


def baca():
    if OS == "win32":
        import wlan_win
        bssid, q = wlan_win.link_quick()
        return bssid, (q / 2.0 - 100 if q is not None else ""), "aprox"
    if OS == "darwin":
        import wlan_mac
        bssid, rssi = wlan_mac.link_quick()
        return bssid, rssi, "corewlan"
    from scan_point import iface_otomatis
    out = subprocess.run(["iw", "dev", iface_otomatis(A.iface), "link"], capture_output=True, text=True).stdout
    l = parse_link(out)
    return l["bssid"], l["rssi"], "iw"


def _rata_per(pola, kunci):
    """{bssid: {kunci: [rssi..]}} dari file survei (hanya SSID yang diuji)."""
    hasil = {}
    for f in glob.glob(os.path.join(HERE, "data", pola)):
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("ssid") == A.ssid and r.get("rssi_dbm"):
                    hasil.setdefault(r["bssid"].lower(), {}).setdefault(r[kunci], []).append(float(r["rssi_dbm"]))
    return hasil


def _terkuat(d):
    return max(d.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))[0]


def muat_peta():
    """bssid -> nama AP, bssid -> titik terdekat. Kosong kalau file survei belum ada."""
    ap = {b: _terkuat(d).split("-AP-")[-1] for b, d in _rata_per("map_bssid_L*.csv", "titik_id").items()}
    titik = {b: _terkuat(d) for b, d in _rata_per("passive_L*.csv", "titik_id").items()}
    ket = {}
    for f in glob.glob(os.path.join(HERE, "data", "titik_L*.csv")):
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                ket[r["titik_id"]] = r.get("keterangan", "")
    return ap, titik, ket


def cari(tabel, bssid):
    """Cocokkan persis; kalau tidak ada, cocokkan radio yang sama (5 oktet pertama)."""
    if not bssid:
        return ""
    b = bssid.lower()
    if b in tabel:
        return tabel[b]
    return next((v for k, v in tabel.items() if k[:14] == b[:14]), "")


class Ping(threading.Thread):
    """Jalankan ping terus-menerus; simpan RTT terakhir ('RTO' kalau timeout)."""
    def __init__(self, host):
        super().__init__(daemon=True)
        self.host, self.rtt, self.n_rto, self.proc = host, "", 0, None

    def run(self):
        cmd = ["ping", "-t", self.host] if OS == "win32" else ["ping", self.host]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace")
        for line in self.proc.stdout:
            m = re.search(r"[=<]\s*([\d.]+)\s*ms", line)
            if m:
                self.rtt = m.group(1)
            elif re.search(r"timed out|unreachable|failure|tidak", line, re.I):
                self.rtt = "RTO"
                self.n_rto += 1


def main():
    global A
    p = argparse.ArgumentParser()
    p.add_argument("--iface", default="auto", help="interface Wi-Fi Linux (default: deteksi otomatis)")
    p.add_argument("--out", required=True)
    p.add_argument("--interval", type=float, default=1.0)
    p.add_argument("--ping", default="filkom.ub.ac.id", help="host ping; 'off' untuk mematikan")
    p.add_argument("--ssid", default="WiFi-UB.x")
    A = p.parse_args()
    os.makedirs(os.path.dirname(A.out) or ".", exist_ok=True)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace", line_buffering=True)

    peta_ap, peta_titik, ket = muat_peta()
    ping = None
    if A.ping != "off":
        ping = Ping(A.ping)
        ping.start()
    print("Uji roaming -> %s | %d BSSID dikenal | ping %s | Ctrl+C untuk selesai\n" % (A.out, len(peta_ap), A.ping))

    prev, mulai, kejadian = None, time.time(), []
    with open(A.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["waktu", "bssid", "rssi_dbm", "sumber", "pindah", "ap", "ping_ms",
                    "ap_lama", "ap_baru", "lokasi_perkiraan"])
        try:
            while True:
                bssid, rssi, src = baca()
                pindah = "YA" if prev and bssid and bssid != prev else ""
                waktu = datetime.now().strftime("%H:%M:%S")
                ap = cari(peta_ap, bssid)
                rtt = ping.rtt if ping else ""
                lama = baru = lokasi = ""
                if pindah:
                    lama, baru = cari(peta_ap, prev) or prev, ap or bssid
                    t = cari(peta_titik, bssid)
                    lokasi = ("dekat %s (%s)" % (t, ket.get(t, ""))) if t else "tidak diketahui"
                    kejadian.append((waktu, lama, baru, rssi, lokasi))
                w.writerow([waktu, bssid, rssi, src, pindah, ap, rtt, lama, baru, lokasi])
                fh.flush()
                print("%s %-17s %-8s %6s dBm  ping %-5s %s" % (
                    waktu, bssid or "(tidak terhubung)", ap, rssi, rtt,
                    "<-- PINDAH AP %s -> %s, %s" % (lama, baru, lokasi) if pindah else ""))
                prev = bssid or prev
                time.sleep(A.interval)
        except KeyboardInterrupt:
            pass
    if ping and ping.proc:
        ping.proc.terminate()

    ringkas = os.path.splitext(A.out)[0] + "_ringkasan.txt"
    with open(ringkas, "w", encoding="utf-8") as fh:
        fh.write("Uji roaming %s, durasi %.0f detik\n" % (os.path.basename(A.out), time.time() - mulai))
        fh.write("Jumlah pindah AP: %d\n" % len(kejadian))
        for k in kejadian:
            fh.write("  %s  %s -> %s  (%s dBm)  %s\n" % k)
        if ping:
            fh.write("Ping RTO selama uji: %d\n" % ping.n_rto)
    print("\nSelesai. Log: %s\nRingkasan: %s" % (A.out, ringkas))
    print(open(ringkas, encoding="utf-8").read())


if __name__ == "__main__":
    main()
