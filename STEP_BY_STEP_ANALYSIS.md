# Survei Wi-Fi 5 GHz Lantai 4 FILKOM — Kelompok 6

**Target:** lantai 4 (gedung utama + Ext). Lantai 3 dan 5 cuma dicek buat lihat **bocor sinyal** dari/ke lantai 4.
**SSID:** `WiFi-UB.x` · **Semua perintah dijalankan dari folder `kelompok6/`.**

---

## 1. Pembagian tugas

| | **Tim 1: Ghazy + Alif** | **Tim 2: Bagas + Auliya** |
|---|---|---|
| Laptop | Ghazy (`--device ghazy`) | Bagas (`--device bagas`) |
| Area | **L4 gedung utama**: 23 titik | **L4 Ext** 9 titik → **L3** 13 titik → **L5** 13 titik |
| Tambahan | Petakan BSSID AP L4, uji aktif, uji roaming | Petakan BSSID AP L3 & L5 |
| Pegang laptop + jalanin skrip | Ghazy | Bagas |
| Tulis dBm di peta cetak, catat jumlah orang & fungsi ruang, foto AP | Alif | Auliya |
| Perkiraan waktu | ±75 menit | ±75 menit |

> Cuma ada 1 laptop? Tim 2 jalan **setelah** Tim 1 selesai, pakai laptop yang sama dan nama `--device` yang sama.

**Setelah survei**

| Orang | Tugas |
|---|---|
| **Ghazy** | Gabung data, jalanin `analyze.py` + `gabung_lantai.py`, tabel area lemah + akar masalah |
| **Bagas** | Denah final di draw.io (AP fisik, material dinding), `ap_fisik_L4.csv`, gambar denah usulan solusi |
| **Alif** | Tabel uji aktif + roaming, hitung kebutuhan kapasitas per ruang |
| **Auliya** | Susun laporan + slide, latar belakang, referensi (termasuk regulasi kanal 5 GHz Kominfo/Komdigi) |

---

## 2. Persiapan (malam ini)

**Ghazy, sekali saja: push ke repo kelompok** (`github.com/ghazthiskc19/wifi-scan-kel6`)
1. Di folder `wifi-scan-kel6` lokal:
   ```powershell
   git add .
   git commit -m "Kelompok 6: titik survei L3-L5, denah, skrip survei"
   git push
   ```
2. Repo → *Settings → Collaborators* → undang Bagas, Alif, Auliya, supaya mereka bisa push data.

**Semua anggota yang bawa laptop**
```powershell
git clone https://github.com/ghazthiskc19/wifi-scan-kel6.git
cd wifi-scan-kel6\kelompok6
pip install pandas numpy scipy matplotlib
python cek_laptop.py          # harus SEMUA LULUS, dalam keadaan konek WiFi-UB.x
```

- **Windows 11:** *Settings → Privacy & security → Location* → On + **"Let desktop apps access your location"** → On. Tanpa ini scan ditolak.
- Catat **model laptop + kartu Wi-Fi** (*Device Manager → Network adapters*). Laptop Ghazy: Realtek RTL8852AE WiFi 6 802.11ax PCIe.
- **Cetak peta** (A3 kalau bisa):
  - Tim 1: `denah/peta_titik_L4.png`
  - Tim 2: `denah/peta_titik_L4.png`, `denah/peta_titik_L3.png`, `denah/peta_titik_L5.png`
- Bawa: laptop dicas penuh + charger, pensil, papan jalan. Matikan *sleep* laptop.

---

## 3. Patokan jarak di lapangan

- Kolom bangunan (kotak hitam di peta) berjarak **7,2 m ≈ 10 langkah**. Titik koridor sengaja ditaruh **sejajar kolom**, jadi cari kolomnya, bukan ngukur.
- Titik ruang = **tengah ruangan**.
- Kalau titiknya kena dinding/meja/ruang terkunci: berdiri di tempat terdekat yang bisa (depan pintu/koridor), **tandai posisi sebenarnya di peta**, tulis di catatan.
- Jarak ke titik sebelumnya juga muncul di layar waktu `survei.py` jalan.

**L4 gedung utama (Tim 1)**: rute muter searah jarum jam dari hall

| Titik | Lokasi | Jarak dari titik sebelumnya |
|---|---|---|
| 000 | Hall sisi A (**kalibrasi**, scan 5×) | start |
| 001 | Sudut koridor kanan-atas | 9,7 m |
| 002 | Koridor atas, sejajar kolom C | 8,4 m |
| 003 | F4.8 tengah | 5,7 m |
| 004 | Koridor atas, sejajar kolom D | 5,7 m |
| 005 | R. Duduk atas | 4,5 m |
| 006 | Sudut koridor kiri-atas (dekat toilet) | 5,0 m |
| 007 | Koridor kiri, depan lift atas | 6,0 m |
| 008 / 009 / 010 | F4.2 / F4.4 / F4.6 tengah | 4,9 / 7,2 / 7,2 m |
| 011 / 012 | Koridor kanan, sejajar baris 4 / baris 3 | 4,9 / 7,2 m |
| 013 / 014 / 015 | F4.5 / F4.3 / F4.1 tengah | 4,8 / 7,2 / 7,2 m |
| 016 | Koridor kiri, depan lift bawah | 4,8 m |
| 017 | Sudut koridor kiri-bawah | 5,9 m |
| 018 | R. Duduk bawah | 5,1 m |
| 019 | Koridor bawah, sejajar kolom D | 4,6 m |
| 020 | F4.7 tengah | 5,8 m |
| 021 | Koridor bawah, sejajar kolom C | 5,8 m |
| 022 | Sudut koridor kanan-bawah | 8,4 m |

**L4 Ext (Tim 2)**: grid 3×3, jarak antar-titik **7,2 m** ke samping, **±6,6 m** ke atas/bawah

| | Barat (ujung) | Tengah | Timur (dekat hall) |
|---|---|---|---|
| Ruang atas | 101 F4.14 | 102 F4.12 | 103 F4.10 |
| Koridor | 106 | 105 | 104 |
| Ruang bawah | 107 F4.13 | 108 F4.11 | 109 F4.9 |

Urutannya: 101 → 102 → 103 → 104 → 105 → 106 → 107 → 108 → 109.

**L3 & L5 (Tim 2)**: 13 titik, **posisinya persis di bawah/atas titik L4 bernomor sama**:
000, 007, 008, 009, 010, 013, 014, 015 (gedung utama) + 101, 103, 105, 107, 109 (Ext).
Cari posisinya pakai kolom yang sama seperti di L4. Di L5 beberapa titik (008, 009, 010, 013) jatuh di ruang Kaprodi/dinding, jadi berdiri di koridor terdekat dan tulis di catatan.

---

## 4. Hari H

### 4.1 Mulai bareng (10 menit): kalibrasi 2 laptop di L4-000 (hall sisi A)

Dua laptop **berdiri bersebelahan**, scan barengan:
```powershell
# Ghazy: langsung jalankan survei, titik pertama = L4-000 (scan 5x)
python survei.py --lantai 4 --device ghazy --bagian main
# Bagas: scan L4-000 sekali, lalu Ctrl+C / lanjut ke tugasnya
python scan_point.py --titik L4-000 --lantai 4 --slot T1 --device bagas --out data\passive_L4_bagas.csv --n 5 --ssid "WiFi-UB.x"
```
Tulis angka dBm dua laptop ini. Selisihnya = **offset antar-laptop**, wajib masuk laporan.

### 4.2 Tim 1: Ghazy + Alif

**a. Survei L4 gedung utama (±40 menit)**: lanjutkan `survei.py` yang tadi:
```powershell
python survei.py --lantai 4 --device ghazy --bagian main
```
Di tiap titik:
1. Berdiri di titik, laptop setinggi perut, **layar selalu menghadap arah yang sama**.
2. Ketik catatan singkat (`kelas, 30 orang, pintu tutup`) → Enter. Nggak ada catatan? Langsung Enter.
3. Tunggu ±20 detik. Angka dBm otomatis masuk `data\rekap_L4_ghazy.csv`.
4. Pindah ke titik berikutnya.

`s` = lewati titik, `q` = berhenti. Jalanin lagi perintah yang sama buat lanjut; titik yang udah di-scan otomatis dilewati.

**Alternatif: scan per nomor titik di peta** (bebas urutan, scan ulang otomatis ganti data lama):
```powershell
python survei.py --lantai 4 --device ghazy --point 001
python survei.py --lantai 4 --device ghazy --point 015 --catatan "kelas, 30 orang, pintu tutup"
python survei.py --lantai 4 --device ghazy --rekap      # lihat titik yang udah/belum
```
dBm terkuat, kanal, BSSID, dan catatan tiap titik otomatis masuk ke `data\rekap_L4_ghazy.csv` (bisa dibuka di Excel), jadi **nggak wajib nulis dBm di kertas**. Kertas cukup buat tandai AP fisik, titik yang digeser, dan jumlah kursi.

Sambil jalan, **Alif foto setiap AP** di plafon/dinding (tandai ■ di peta), dan catat **fungsi + jumlah kursi tiap ruang**.

**b. Petakan BSSID AP L4 (±5 menit)**: berdiri tepat di bawah tiap AP yang ketemu (menurut Ruckus ada di F4.2, F4.3, F4.5, F4.6):
```powershell
python scan_point.py --titik L4-AP-F4.2 --lantai 4 --slot T1 --device ghazy --out data\map_bssid_L4_ghazy.csv --n 1 --ssid "WiFi-UB.x"
```
Ganti `F4.2` sesuai ruangnya. Tulis BSSID + kanal yang muncul di samping AP di peta.

**c. Uji aktif (±15 menit)**: pilih 6–8 titik dari angka di peta: **3 terjelek, 2 terbagus, 1–3 yang ramai/mencurigakan**. Laptop harus **tersambung** ke `WiFi-UB.x`:
```powershell
python active_point.py --titik L4-015 --out data\active_L4.csv
```

**d. Uji roaming (2 × 5 menit)**: buka 2 jendela PowerShell di `kelompok6`:
```powershell
# Jendela 1
python roam_log.py --out raw\roaming_L4_R1.csv
# Jendela 2
ping -t filkom.ub.ac.id | ForEach-Object { "{0} {1}" -f (Get-Date -Format HH:mm:ss), $_ } | Tee-Object raw\roaming_ping_L4_R1.txt
```
- **R1:** jalan pelan 1 putaran koridor gedung utama.
- **R2:** koridor Ext ujung barat → hall → koridor gedung utama.

Tiap muncul **"PINDAH AP"**, Alif tandai lokasinya di peta. Selesai satu lintasan: Ctrl+C di dua jendela. Lintasan kedua **ganti `R1` → `R2`** (nama sama = file lama ketimpa).

### 4.3 Tim 2: Bagas + Auliya

**a. L4 Ext (±15 menit)**
```powershell
python survei.py --lantai 4 --device bagas --bagian ext
```
**b. Turun ke L3 (±20 menit)**
```powershell
python survei.py --lantai 3 --device bagas
```
**c. Naik ke L5 (±20 menit)**
```powershell
python survei.py --lantai 5 --device bagas
```
Cara kerja tiap titik sama kayak Tim 1. **Auliya tulis angka dBm** di peta + catat kondisi ruang.

**d. Petakan BSSID AP L3 & L5 (±10 menit)**: lingkaran merah putus-putus di `peta_titik_L3.png` / `peta_titik_L5.png` = posisi AP. Berdiri di bawahnya:
```powershell
python scan_point.py --titik L3-AP-1 --lantai 3 --slot T1 --device bagas --out data\map_bssid_L3_bagas.csv --n 1 --ssid "WiFi-UB.x"
```
Nomori `AP-1`, `AP-2`, … dan tulis nomornya di peta. Di L5 pakai `L5-AP-1` dan file `map_bssid_L5_bagas.csv`.

### 4.4 Selesai: upload data (5 menit, jangan pulang dulu)

1. Foto semua peta cetak yang udah ada angkanya, simpan ke `denah/foto_AP/` bareng foto AP.
2. Push data dari tiap laptop:
   ```powershell
   cd ..                 # ke root repo wifi-scan-kel6
   git add kelompok6/data kelompok6/raw kelompok6/denah/foto_AP
   git commit -m "Data survei L4 <nama>"
   git pull --rebase
   git push
   ```
   Nama file tiap laptop beda (`_ghazy`, `_bagas`), jadi nggak bakal bentrok.

---

## 5. Olah data (Ghazy)

```powershell
cd kelompok6
git pull
python gabung_data.py                     # passive_L{n}_*.csv -> passive_L{n}.csv
python analyze.py --passive data\passive_L4.csv --titik data\titik_L4.csv --ssid "WiFi-UB.x" --denah denah\denah_L4.png --scale 20 --out output\L4 --active data\active_L4.csv
python analyze.py --passive data\passive_L3.csv --titik data\titik_L3.csv --ssid "WiFi-UB.x" --denah denah\denah_L3.png --scale 20 --out output\L3
python analyze.py --passive data\passive_L5.csv --titik data\titik_L5.csv --ssid "WiFi-UB.x" --denah denah\denah_L5.png --scale 20 --out output\L5
python gabung_lantai.py --ap 3:output\L3_ap.csv 4:output\L4_ap.csv 5:output\L5_ap.csv --titik 3:output\L3_titik.csv 4:output\L4_titik.csv 5:output\L5_titik.csv --ringkasan output\L3_ringkasan.txt output\L4_ringkasan.txt output\L5_ringkasan.txt --out output\gedung
```
Tambahkan `--ap-fisik data\ap_fisik_L4.csv` ke analyze L4 setelah Bagas bikin file AP fisiknya.

> Ada titik yang digeser di lapangan? Betulin `x_px,y_px` di `data/titik_L{n}.csv` (**20 px = 1 m**) sebelum jalanin `analyze.py`.

| File hasil | Isinya | Dipakai buat |
|---|---|---|
| `output/L4_heatmap.png` | Peta RSSI | Slide cakupan |
| `output/L4_status.png` | Status titik + area lemah + estimasi AP | **Slide utama** |
| `output/L4_area_lemah.csv` | Area lemah + penyebab | Deskripsi masalah |
| `output/L4_kanal.png` | Pemakaian kanal | Alokasi kanal |
| `output/gedung_ap_per_lantai.csv` | Lantai asal tiap AP | Bukti bocor antar-lantai |
| `output/gedung_titik_lantai_lain.csv` | Titik L4 yang AP terkuatnya dari L3/L5 | Bukti bocor antar-lantai |
| `output/gedung_floor_bleed.csv` | Selisih RSSI antar-lantai (≈ redaman pelat lantai) | Pembahasan |

---

## 6. Analisis → solusi

Untuk **setiap area lemah**, cocokkan gejala di data dengan tabel ini:

| Yang terlihat di data | Artinya | Solusi yang diusulkan |
|---|---|---|
| RSSI < −75 dBm, AP terdekat jauh | AP kurang (coverage gap) | Tambah AP / pindah AP ke tengah area |
| RSSI rendah padahal AP dekat, terhalang dinding | Redaman dinding | Pindah AP ke dalam ruang |
| RSSI bagus tapi RTT/loss jelek, banyak AP sekanal (CCI > 2) | Interferensi kanal sama | Atur ulang kanal, tetap 20 MHz, kurangi daya |
| RSSI bagus, utilisasi > 50%, klien banyak | Kepenuhan (kapasitas) | Tambah AP kapasitas, batasi klien, band steering |
| AP terkuat di L4 berasal dari L3/L5 | Bocor antar-lantai | Turunkan daya AP L3/L5, hindari kanal sama di posisi tumpuk |
| Nggak ada AP cadangan ≥ −75, ping hilang pas pindah AP | Overlap kurang | Rapatkan AP, aktifkan 802.11k/v/r |

**Biar solusinya kuat (bukan "tambah AP" doang):**
- **Jumlah AP** = yang terbesar antara kebutuhan *cakupan* (luas area / jangkauan 1 AP sampai −67 dBm) dan *kapasitas* (kursi × 1,5 perangkat × faktor aktif 0,5–0,7 × Mbps per orang ÷ throughput 1 AP). Asumsinya wajib pakai sumber.
- **Kanal:** di gambar denah, kasih label kanal tiap AP. AP bersebelahan **dan** yang tumpuk vertikal (L3/L5) jangan sekanal.
- **Prediksi sesudah perbaikan:** pakai jarak & RSSI hasil ukur, hitung RSSI di titik-titik lemah kalau AP dipindah/ditambah, lalu bandingkan % titik ≥ −67 dBm **sebelum vs sesudah**.

Info awal dari Ruckus (Agustus 2025, data lama, cuma pembanding):

| AP L4 | Kanal 5G | Klien | Util 5G | Catatan |
|---|---|---|---|---|
| F4.2 | 40 | 40 | 18% | |
| F4.3 | 149 | 66 | 54% | sekanal dgn Ext-F4.9 |
| F4.5 | 161 | 63 | 52% | sekanal dgn Ext-F4.10 |
| F4.6 | 153 | 49 | **77%** | sekanal dgn Ext-4.13 |
| Ext-F4.9 / F4.10 / 4.13 / 4.14 | 149 / 161 / 153 / 157 | 49 / 40 / 18 / 39 | 56 / 40 / **85** / 40% | |

Ruang yang nggak ada AP-nya menurut Ruckus: F4.1, F4.4, F4.7, F4.8, F4.11, F4.12. Kandidat spot lemah, buktikan pakai data.

---

## 7. Isi PPT → siapa → datanya dari mana

| Bagian PPT | PJ | Sumber |
|---|---|---|
| Latar belakang | Auliya | Denah, data Ruckus, kondisi L4 |
| Deskripsi masalah | Ghazy | `L4_status.png`, `L4_area_lemah.csv` |
| Jumlah user aktif | Alif | Hitungan orang di lapangan, klien per AP (Ruckus / BSS Load) |
| Fungsi ruangan | Alif | Catatan fungsi + kursi tiap ruang |
| Desain solusi: jumlah AP, kanal, daya | Ghazy + Alif | §6 |
| Desain solusi: penempatan | Bagas | Denah usulan (□ AP lama, ■ AP baru, label kanal) |
| Pembahasan | Ghazy | Uji aktif, roaming, bocor antar-lantai, sebelum vs sesudah |
| Kesimpulan | Auliya | 3–5 poin + prioritas solusi |
| Referensi | Auliya | Panduan §14 + regulasi kanal |

**Keterbatasan (wajib ditulis):** RSSI tergantung kartu Wi-Fi tiap laptop (lampirkan offset dari §4.1); Windows nggak ngasih noise, jadi SNR nggak dianalisis; sinyal di `roam_log.py` versi Windows cuma perkiraan; survei cuma di satu rentang waktu; data Ruckus dari 2025.

---

## 8. Catatan file

| File | Keterangan |
|---|---|
| `kelompok6/denah/denah_L{3,4,5}.png` | Denah gedung utama + Ext dalam **satu sistem koordinat** (20 px/m, titik F/6 di piksel (580,100)). Titik bernomor sama di tiap lantai posisinya tumpuk vertikal |
| `kelompok6/data/titik_L{3,4,5}.csv` | Koordinat titik + jarak antar-titik |
| `kelompok6/denah/peta_titik_L{3,4,5}.png` | Peta buat dicetak |
| `white version_Floor Plan F{3,4,5} + Ext.png` | Denah tanpa warna heatmap |
| `Floor Plan F4 + Ext.png` | ⚠ **Isinya denah lantai 1** (elevasi ±0.00, "Selasar Lantai 1"), bukan lantai 4. Denah L4 dibuat dari `F4 Main Floor Plan` + `F4 Side Floor Plan` |
| `RuckusAPList.csv` | Masuk `.gitignore` karena berisi IP/MAC internal kampus. Kirim lewat chat/Drive kalau ada yang butuh |
