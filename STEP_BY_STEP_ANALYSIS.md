# Survei Wi-Fi 5 GHz Lantai 4 FILKOM — Kelompok 6

**Target:** lantai 4 (gedung utama + Ext). Lantai 3 dan 5 cuma dicek buat lihat **bocor sinyal** dari/ke lantai 4.
**SSID:** `WiFi-UB.x` · **Semua perintah dijalankan dari folder `kelompok6/`.**

**Contekan cepat** (detail di §4):

| Mau ngapain | Perintah |
|---|---|
| Kalibrasi (1×, semua laptop barengan di titik merah `000` L4) | `python survei.py --kalibrasi` |
| Scan satu titik | `python survei.py --lantai 4 --point 001 --catatan "koridor, 5 orang"` |
| Cek titik yang udah / belum | `python survei.py --lantai 4 --rekap` |
| Petakan BSSID AP (berdiri di bawah AP) | `python survei.py --lantai 4 --ap F4.2` |
| Uji aktif (tersambung ke WiFi-UB.x) | `python active_point.py --titik L4-015 --out data\active_L4.csv` |
| Hitung offset antar-laptop (setelah semua push) | `python survei.py --offset` |

---

## 1. Pembagian tugas (per lantai)

**Aturan: 1 lantai = 1 laptop.** Semua scan satu lantai masuk ke satu file `data\passive_L{n}.csv`. Jangan ada 2 laptop nge-scan lantai yang sama, nanti filenya bentrok waktu push.

| | **Lantai 4: Ghazy + Alif** | **Lantai 3 & 5: Bagas + Auliya** |
|---|---|---|
| Titik | L4: 41 titik (gedung utama 000–022, Ext 101–109, tambahan 201–209) | L3: 13 titik, lalu L5: 13 titik |
| Tambahan | Petakan BSSID AP L4, uji aktif, uji roaming | Petakan BSSID AP L3 & L5 |
| Pegang laptop + jalanin skrip | Ghazy | Bagas |
| Foto AP, catat jumlah orang & fungsi ruang, tandai titik yang digeser | Alif | Auliya |
| Perkiraan waktu | ±80 menit | ±60 menit |

> Cuma ada 1 laptop? Kerjakan lantai satu per satu pakai laptop yang sama. Nggak ada yang perlu diubah.

**Setelah survei**

| Orang | Tugas |
|---|---|
| **Ghazy** | Jalanin `analyze.py` + `gabung_lantai.py`, tabel area lemah + akar masalah |
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
  - Lantai 4: `denah/peta_titik_L4_rev.png` (**versi `_rev`**, ada titik tambahan oranye)
  - Lantai 3 & 5: `denah/peta_titik_L3.png`, `denah/peta_titik_L5.png`
- Bawa: laptop dicas penuh + charger, pensil, papan jalan. Matikan *sleep* laptop.

---

## 3. Patokan jarak di lapangan

- Kolom bangunan (kotak hitam di peta) berjarak **7,2 m ≈ 10 langkah**. Titik koridor sengaja ditaruh **sejajar kolom**, jadi cari kolomnya, bukan ngukur.
- Titik ruang = **tengah ruangan**.
- Kalau titiknya kena dinding/meja/ruang terkunci: berdiri di tempat terdekat yang bisa (depan pintu/koridor), **tandai posisi sebenarnya di peta**, tulis di catatan.
- Lokasi titik + jarak ke titik terdekat muncul di layar waktu `survei.py` jalan.

**L4 gedung utama**: rute muter searah jarum jam dari hall

| Titik | Lokasi | Jarak dari titik sebelumnya |
|---|---|---|
| 000 | Hall sisi A (titik merah: tempat kalibrasi, scan 5×) | start |
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

**L4 Ext**: grid 3×3, jarak antar-titik **7,2 m** ke samping, **±6,6 m** ke atas/bawah

| | Barat (ujung) | Tengah | Timur (dekat hall) |
|---|---|---|---|
| Ruang atas | 101 F4.14 | 102 F4.12 | 103 F4.10 |
| Koridor | 106 | 105 | 104 |
| Ruang bawah | 107 F4.13 | 108 F4.11 | 109 F4.9 |

Urutan scan-nya ikut rute L4 di §4.2 (masuk Ext dari hall).

**Titik tambahan (oranye, kotak di `denah/peta_titik_L4_rev.png`)**: pojok terjauh dari AP di ruang tanpa AP menurut Ruckus, plus tangga. Cetak peta `_rev` ini, bukan yang lama.

| Titik | Lokasi |
|---|---|
| 201 / 202 / 203 / 204 | F4.1 pojok kiri-bawah / F4.4 sisi atas / F4.8 pojok kanan-atas / F4.7 pojok kanan-bawah |
| 205 / 206 | Ext F4.12 sisi atas / Ext F4.11 sisi bawah |
| 207 / 208 / 209 | Tangga kanan-atas / tangga kanan-bawah / tangga kiri-bawah (sebelah lift) |

**L3 & L5**: 13 titik, **posisinya persis di bawah/atas titik L4 bernomor sama**:
000, 007, 008, 009, 010, 013, 014, 015 (gedung utama) + 101, 103, 105, 107, 109 (Ext).
Cari posisinya pakai kolom yang sama seperti di L4. Di L5 beberapa titik (008, 009, 010, 013) jatuh di ruang Kaprodi/dinding, jadi berdiri di koridor terdekat dan tulis di catatan.

---

## 4. Hari H

Semua perintah dijalankan dari folder `kelompok6`. **Formatnya cuma satu:**
```powershell
python survei.py --lantai <3/4/5> --point <nomor di peta>
```
Nama laptop dicatat otomatis dari nama komputer, jadi nggak perlu `--device`.

### 4.1 Kalibrasi (10 menit, SEMUA laptop barengan, sebelum pencar)

Tujuannya: tiap kartu Wi-Fi membaca dBm sedikit beda. Selisih ini (**offset**) wajib masuk laporan.

1. Semua laptop kumpul di **titik merah `000` lantai 4** (hall sisi A).
2. Berdiri **bersebelahan**, laptop setinggi perut, **layar menghadap arah yang sama**.
3. Hitung 1-2-3, semua tekan Enter **barengan**:
   ```powershell
   python survei.py --kalibrasi
   ```
4. Tunggu ±40 detik (scan 5×) sampai muncul `>> Tersimpan: data\kalibrasi_<nama-laptop>.csv`.
5. Setelah semua laptop push (§4.5), salah satu orang jalankan:
   ```powershell
   git pull
   python survei.py --offset
   ```
   Hasilnya: offset tiap laptop dalam dB (median selisih BSSID yang sama), tersimpan di `data\offset_kalibrasi.csv`. Angka ini yang ditulis di laporan.

> Kalibrasi ≠ titik `000`. Pemegang lantai 4 **tetap** scan `--point 000` sebagai titik survei biasa (boleh langsung setelah kalibrasi, di tempat yang sama).

### 4.2 Capture titik (inti survei)

Di **setiap titik**:
1. Berdiri di titik sesuai peta. Kalau titiknya kena dinding/meja/ruang terkunci, berdiri di tempat terdekat yang bisa, lalu tulis di catatan.
2. Laptop setinggi perut, **layar selalu menghadap arah yang sama** di semua titik (misal ke arah hall). Jangan berdiri di antara laptop dan AP.
3. Jalankan:
   ```powershell
   python survei.py --lantai 4 --point 001 --catatan "koridor, 5 orang"
   ```
4. Tunggu ±25 detik sampai muncul `>> L4-001: -xx dBm (ch xx) -> tersimpan`. Baru pindah.
5. Titik berikutnya: tekan **↑ (panah atas)**, ganti nomor + catatan, Enter.

| Perintah | Gunanya |
|---|---|
| `python survei.py --lantai 4 --point 015 --catatan "kelas, 30 orang, pintu tutup"` | Scan 1 titik + catatan |
| `python survei.py --lantai 4 --point 015` | Scan ulang (data lama otomatis diganti). Pakai kalau angkanya aneh |
| `python survei.py --lantai 4 --rekap` | Lihat titik yang udah + dBm-nya, dan yang belum |

- **Isi catatan:** jenis ruang, perkiraan jumlah orang, pintu buka/tutup, titik digeser ke mana.
- **Nggak perlu nulis dBm di kertas.** Semua otomatis masuk `data\rekap_L4.csv` (bisa dibuka di Excel). Titik `000` otomatis scan 5×, titik lain 3×.
- Salah ketik nomor titik? Skrip nolak dan menampilkan daftar nomor yang ada.

**Rute L4 (Ghazy)**, muter searah jarum jam, titik tambahan diselipin. Titik `000` L4 **sudah discan** (11 Okt, 09:28), jadi mulai dari `001`:
```
000 → 001 → 207 → 002 → 003 → 203 → 004 → 005 → 006 → 007 → 008 → 009 → 202 → 010
→ 011 → 012 → 013 → 014 → 015 → 201 → 016 → 209 → 017 → 018 → 019 → 020 → 204
→ 021 → 208 → 022 → (lewat hall ke Ext) 104 → 103 → 205 → 102 → 101 → 106 → 105
→ 107 → 108 → 206 → 109
```

**L3 lalu L5 (Bagas):** `--lantai 3 --point 000`, `007`, `008`, `009`, `010`, `013`, `014`, `015`, `101`, `103`, `105`, `107`, `109`. Setelah itu sama untuk `--lantai 5`.

### 4.3 Petakan BSSID AP (±5 menit per lantai)

Berdiri **tepat di bawah** AP (plafon/dinding):
```powershell
python survei.py --lantai 4 --ap F4.2
```
Skrip menampilkan 3 kandidat BSSID. **Yang paling atas = AP di atas kepala lo**, tulis di samping AP di peta. Ganti `F4.2` sesuai ruangnya. Di L3/L5 pakai nomor: `--lantai 3 --ap 1`, `--ap 2`, dst. Semua masuk `data\map_bssid_L{n}.csv`.

### 4.4 Uji aktif + roaming (lantai 4, Ghazy + Alif)

**Uji aktif (±15 menit):** jalankan `python survei.py --lantai 4 --rekap`, lalu pilih 6–8 titik: **3 dBm terjelek, 2 terbagus, 1–3 yang ramai**. Laptop harus **tersambung** ke `WiFi-UB.x`:
```powershell
python active_point.py --titik L4-015 --out data\active_L4.csv
```

**Uji roaming (2 × 5 menit):** buka 2 jendela PowerShell di `kelompok6`:
```powershell
# Jendela 1
python roam_log.py --out raw\roaming_L4_R1.csv
# Jendela 2
ping -t filkom.ub.ac.id | ForEach-Object { "{0} {1}" -f (Get-Date -Format HH:mm:ss), $_ } | Tee-Object raw\roaming_ping_L4_R1.txt
```
- **R1:** jalan pelan 1 putaran koridor gedung utama.
- **R2:** koridor Ext ujung barat → hall → koridor gedung utama. **Ganti `R1` → `R2`** di dua perintah (nama sama = file lama ketimpa).

Tiap muncul **"PINDAH AP"**, Alif tandai lokasinya di peta. Selesai satu lintasan: Ctrl+C di dua jendela.

### 4.5 Selesai: upload data (5 menit, jangan pulang dulu)

1. Foto peta cetak + foto AP, simpan ke `denah/foto_AP/`.
2. Push dari tiap laptop:
   ```powershell
   cd ..                 # ke root repo wifi-scan-kel6
   git add kelompok6/data kelompok6/raw kelompok6/denah/foto_AP
   git commit -m "Data survei L<n> <nama>"
   git pull --rebase
   git push
   ```
   File tiap lantai dan file kalibrasi tiap laptop beda nama, jadi nggak bakal bentrok (asal 1 lantai = 1 laptop).

---

## 5. Olah data (Ghazy)

```powershell
cd kelompok6
git pull
python survei.py --offset
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

**Keterbatasan (wajib ditulis):** RSSI tergantung kartu Wi-Fi tiap laptop (lampirkan offset dari `data\offset_kalibrasi.csv`, §4.1); Windows nggak ngasih noise, jadi SNR nggak dianalisis; sinyal di `roam_log.py` versi Windows cuma perkiraan; survei cuma di satu rentang waktu; data Ruckus dari 2025.

---

## 8. Catatan file

| File | Keterangan |
|---|---|
| `kelompok6/denah/denah_L{3,4,5}.png` | Denah gedung utama + Ext dalam **satu sistem koordinat** (20 px/m, titik F/6 di piksel (580,100)). Titik bernomor sama di tiap lantai posisinya tumpuk vertikal |
| `kelompok6/data/titik_L{3,4,5}.csv` | Koordinat titik + jarak antar-titik (L4: 41 titik termasuk tambahan 201–209) |
| `kelompok6/denah/peta_titik_L4_rev.png` | Peta L4 buat dicetak (**pakai ini**, ada titik tambahan oranye). `peta_titik_L4.png` = versi lama |
| `kelompok6/denah/peta_titik_L{3,5}.png` | Peta L3 & L5 buat dicetak |
| `kelompok6/data/passive_L{n}.csv` | Data mentah hasil `survei.py --point`, 1 file per lantai. Input `analyze.py` |
| `kelompok6/data/rekap_L{n}.csv` | dBm terkuat, kanal, BSSID, catatan tiap titik (buka di Excel) |
| `kelompok6/data/kalibrasi_<laptop>.csv`, `offset_kalibrasi.csv` | Hasil `--kalibrasi` tiap laptop dan offset-nya (`--offset`) |
| `kelompok6/data/map_bssid_L{n}.csv` | Hasil `--ap`: BSSID tiap AP fisik |
| `kelompok6/survei.py` | Skrip utama survei. `gabung_data.py` sudah dihapus (nggak perlu lagi, malah bisa menimpa data) |
| `white version_Floor Plan F{3,4,5} + Ext.png` | Denah tanpa warna heatmap |
| `Floor Plan F4 + Ext.png` | ⚠ **Isinya denah lantai 1** (elevasi ±0.00, "Selasar Lantai 1"), bukan lantai 4. Denah L4 dibuat dari `F4 Main Floor Plan` + `F4 Side Floor Plan` |
| `RuckusAPList.csv` | Masuk `.gitignore` karena berisi IP/MAC internal kampus. Kirim lewat chat/Drive kalau ada yang butuh |
