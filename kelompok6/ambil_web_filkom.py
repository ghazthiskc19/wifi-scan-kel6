#!/usr/bin/env python3
"""
ambil_web_filkom.py - ambil data publik dashboard Wi-Fi FILKOM (https://filkom.ub.ac.id/wifi/) sebagai data primer
dari sisi controller kampus.

Endpoint publik yang dipakai halaman itu sendiri:
  api/public/recommend           kondisi per AP (rating, jumlah perangkat, airtime %) + rata-rata perangkat per jam (7 hari)
  api/public/wifimodel           daftar AP di peta 3D (model, kanal, EIRP, posisi). Peta ini BELUM diperbarui:
                                 hanya diarsipkan, tidak dipakai di analisis (kanal & posisi tetap dari survei)
  api/public/wifimodel/clients   perangkat tersambung: AP, RSSI, SNR, rate, generasi Wi-Fi, jenis perangkat

Field `id` perangkat TIDAK disimpan (privasi). Peta jangkauan (wifimodel/coverage, ±11 MB) tidak diambil.

  python ambil_web_filkom.py                     sekali ambil  -> data/web_filkom/<tanggal_jam>/
  python ambil_web_filkom.py --poll 5 --jam 8    ambil tiap 5 menit selama 8 jam (jalankan saat jam kuliah)
                                                 -> juga menambah baris ke data/web_filkom/poll_ap.csv & poll_klien.csv
"""
import argparse
import csv
import datetime as dt
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "web_filkom")
BASE = "https://filkom.ub.ac.id/wifi/api/public/"
WIB = dt.timezone(dt.timedelta(hours=7))


def ambil(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 (survei Wi-Fi Kelompok 6)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def tambah_csv(path, rows, kolom):
    baru = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=kolom)
        if baru:
            w.writeheader()
        w.writerows(rows)


def sekali():
    rec = ambil("recommend")
    model = ambil("wifimodel")
    kl = ambil("wifimodel/clients")
    for c in kl.get("clients", []):
        c.pop("id", None)
    waktu = dt.datetime.fromtimestamp(rec["updated_ts"], WIB)
    d = os.path.join(OUT, waktu.strftime("%Y-%m-%d_%H%M"))
    os.makedirs(d, exist_ok=True)
    for nama, isi in (("recommend", rec), ("wifimodel", model), ("clients", kl)):
        with open(os.path.join(d, nama + ".json"), "w", encoding="utf-8") as f:
            json.dump(isi, f, ensure_ascii=False, indent=1)

    jam = waktu.strftime("%Y-%m-%d %H:%M")
    tambah_csv(os.path.join(OUT, "poll_ap.csv"),
               [dict(waktu=jam, area=a["area"], ap=x["name"], rating=x["rating"], klien=x["clients"], airtime=x["airtime"])
                for a in rec["areas"] for x in a["aps"]],
               ["waktu", "area", "ap", "rating", "klien", "airtime"])
    tambah_csv(os.path.join(OUT, "poll_klien.csv"),
               [dict(waktu=jam, ap=c["ap"], rssi=c["rssi"], snr=c["snr"], rate=c["rate"], wifi=c["wifi"], jenis=c["kind"])
                for c in kl.get("clients", [])],
               ["waktu", "ap", "rssi", "snr", "rate", "wifi", "jenis"])
    l4 = sum(x["clients"] for a in rec["areas"] if a["area"] == "Lantai 4" for x in a["aps"])
    print("%s WIB  tersimpan di %s  (perangkat L4: %d, total klien 5 GHz: %d)" % (jam, d, l4, len(kl.get("clients", []))))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--poll", type=float, help="ambil berulang tiap N menit")
    p.add_argument("--jam", type=float, default=8, help="lama polling (jam), default 8")
    a = p.parse_args()
    if not a.poll:
        sekali()
        return
    selesai = time.time() + a.jam * 3600
    while time.time() < selesai:
        try:
            sekali()
        except Exception as e:  # jaringan putus sesaat: lanjut ke putaran berikutnya
            print("gagal:", e)
        time.sleep(a.poll * 60)


if __name__ == "__main__":
    main()
