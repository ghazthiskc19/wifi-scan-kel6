# Outline PPT: Survei Wi-Fi 5 GHz Lantai 4 FILKOM (Kelompok 6)

> **Wajib dibaca semua anggota sebelum bikin slide.** Dokumen ini panjang karena isinya bukan cuma "apa yang ditulis di slide", tapi juga **kenapa**, **angkanya dari mana**, dan **cara membuktikannya** kalau ditanya dosen.

## Daftar isi
- [Bagian A: Cerita besar presentasi (1 menit baca)](#bagian-a-cerita-besar-presentasi)
- [Bagian B: Konsep dasar yang harus dipahami semua anggota](#bagian-b-konsep-dasar-yang-harus-dipahami-semua-anggota)
- [Bagian C: Asal data & file bukti](#bagian-c-asal-data--file-bukti)
- [Bagian D: Slide per slide (12 slide)](#bagian-d-slide-per-slide)
- [Bagian E: Jawaban 16 pertanyaan Ghazy](#bagian-e-jawaban-16-pertanyaan-ghazy)
- [Bagian F: Persiapan tanya jawab](#bagian-f-persiapan-tanya-jawab)
- [Bagian G: Angka kunci & checklist gambar](#bagian-g-angka-kunci--checklist-gambar)

Aturan modul: **maks. 12 slide**, presentasi **15 menit** + tanya jawab 10 menit. Semua gambar ada di `kelompok6/output/solusi_L4/` kecuali disebut lain. Kalau datanya diubah, jalankan ulang (dari folder `kelompok6`):
```powershell
python analyze.py --passive data\passive_L4.csv --titik data\titik_L4.csv --ssid "WiFi-UB.x" --denah denah\denah_L4.png --scale 20 --out output\L4 --active data\active_L4.csv
python solusi_L4.py
python bukti_L4.py
```

---

## Bagian A: Cerita besar presentasi

Seluruh presentasi menceritakan **satu alur**. Semua slide harus mendukung alur ini:

1. **Sinyal di lantai 4 sebenarnya sudah kuat.** 97,4% titik ≥ −67 dBm dan tidak ada blank spot.
2. **Tapi pengguna tetap bisa lambat atau putus.** Uji aktif menemukan RTT > 50 ms dan packet loss, dan uji roaming menemukan koneksi mati ±3,5 menit setelah pindah AP.
3. **Penyebab utamanya bukan kekuatan sinyal, tapi *co-channel interference* (CCI)**, yaitu terlalu banyak radio berbagi kanal yang sama. Ditambah dua hal lain: sinyal dari lantai 5 "bocor" ke lantai 4, dan proses roaming yang tidak mulus.
4. **Solusinya bukan menambah daya, tapi mengatur ulang kanal**, menambah 2 AP di area yang memang lemah, menurunkan daya 1 AP yang terlalu kuat, dan mengaktifkan fitur roaming.
5. **Hasil hitungan:** CCI turun dari **43 → 2**, AP sekanal yang saling tumpang tindih turun dari **9 → 0** titik, dan semua titik ≥ −67 dBm.

> Kalimat kunci yang diulang di awal dan akhir: **"Masalah Wi-Fi lantai 4 bukan sinyal yang lemah, tapi kanal yang terlalu ramai."**

---

## Bagian B: Konsep dasar yang harus dipahami semua anggota

Baca bagian ini dulu. Hampir semua pertanyaan dosen akan berputar di konsep-konsep ini.

### B1. RSSI dan dBm
- **RSSI** adalah kekuatan sinyal yang diterima laptop, dalam satuan **dBm**. Nilainya negatif: **makin mendekati 0, makin kuat**. −40 dBm sangat kuat, −67 dBm cukup, −80 dBm hampir hilang.
- dBm itu skala logaritmik: **turun 3 dB = daya tinggal setengah**, dan turun 10 dB = tinggal sepersepuluh.
- **Ambang yang kita pakai** diambil dari modul §4.5, mengacu praktik desain WLAN enterprise:
  - ≥ −67 dBm: BAIK, aman untuk video call
  - −70 s.d. −67: PERHATIAN
  - < −70: BURUK
  - < −80: blank spot
- **Kenapa RSSI dirata-rata dalam mW, bukan dBm?** Karena dBm logaritmik. Contoh: rata-rata −40 dan −80 kalau dihitung langsung di dBm hasilnya −60, padahal secara daya hasilnya −43. Jadi skrip mengubah dBm ke mW dulu, merata-rata, lalu mengubah lagi ke dBm.

### B2. AP, radio, SSID, BSSID
- **AP** (access point): alat Wi-Fi yang menempel di plafon.
- Satu AP punya beberapa **radio** (2,4 GHz dan 5 GHz). Satu radio memancarkan beberapa **SSID** (nama jaringan), misalnya `WiFi-UB.x`, `eduroam`, dan `FILKOM EVENT`.
- **BSSID** adalah "alamat MAC" tiap SSID di tiap radio, unik per AP.
- Semua AP di kampus memakai SSID yang sama (`WiFi-UB.x`). Karena itu **satu-satunya cara membedakan AP adalah lewat BSSID**. Contoh: `c0:c7:0a:98:3a:52` = AP yang kita sebut **M1**.
- Di dokumen ini AP diberi kode supaya gampang:
  - **M1–M4**: AP gedung utama
  - **E1–E4**: AP gedung Ext
  - **N1–N2**: AP baru (usulan)

### B3. Kanal (channel) dan lebar kanal
- Wi-Fi memakai pita frekuensi yang dibagi menjadi **kanal**. Setiap kanal punya **lebar** 20, 40, 80, atau 160 MHz.
- **Rumus frekuensi tengah kanal:**
  - 2,4 GHz: `f = 2407 + 5 × nomor kanal` (MHz). Contoh: kanal 1 = 2412 MHz.
  - 5 GHz: `f = 5000 + 5 × nomor kanal` (MHz). Contoh: kanal 36 = 5180 MHz, kanal 40 = 5200 MHz.

**Kenapa di 2,4 GHz hanya ada 1/6/11?**
- Jarak antar-nomor kanal di 2,4 GHz cuma 5 MHz, padahal lebar sinyalnya ±20–22 MHz.
- Akibatnya kanal 1 dan 2 tumpang tindih, kanal 1 dan 3 juga tumpang tindih, dan seterusnya.
- Supaya tidak tumpang tindih, kanalnya harus terpisah ≥ 25 MHz, yaitu **kanal 1, 6, dan 11**.

**Bagaimana dengan 5 GHz?**
- Nomor kanal yang dipakai **meloncat 4**: 36, 40, 44, 48, …
- Loncatan 4 nomor = 4 × 5 MHz = **20 MHz**. Jadi untuk lebar 20 MHz, **setiap kanal 5 GHz yang berbeda tidak saling tumpang tindih**:

| Kanal | Frekuensi tengah | Rentang yang dipakai |
|---|---|---|
| 36 | 5180 MHz | 5170–5190 MHz |
| 40 | 5200 MHz | 5190–5210 MHz |

Kanal 36 dan 40 bersebelahan, tapi tidak tumpang tindih.

**Kanal 20 MHz yang boleh dipakai di Indonesia** (Permenkominfo No. 2 Tahun 2023, pita 5150–5350 MHz dan 5725–5825 MHz, dalam ruangan, maks. 200 mW / 23 dBm):

| Kelompok | Kanal | Keterangan |
|---|---|---|
| UNII-1 | 36, 40, 44, 48 | bebas dipakai |
| UNII-2 | 52, 56, 60, 64 | **DFS** (lihat B5) |
| UNII-3 | 149, 153, 157, 161 | bebas dipakai |
| | **total 12 kanal** | **8 non-DFS** |

- Kanal 100–144 berada di pita 5470–5725 MHz, yang tidak termasuk izin kelas di Indonesia.
- Kanal 165 (5815–5835 MHz) keluar dari batas 5825 MHz, jadi **tidak dipakai**.

**Lebar kanal lebih besar = "menggabungkan" beberapa kanal 20 MHz:**
- 40 MHz = 2 kanal, contoh 36+40
- 80 MHz = 4 kanal, contoh 36+40+44+48
- Jadi radio 80 MHz di kanal 36 juga "menduduki" kanal 40, 44, dan 48.

### B4. Co-channel interference (CCI): konsep paling penting
**Salah paham yang umum:** "CCI terjadi karena banyak *channel* yang berkomunikasi." **Ini kurang tepat.** CCI terjadi karena **banyak perangkat yang memakai *satu channel yang sama*** dan saling mendengar.

**Cara kerjanya (CSMA/CA, "dengar dulu baru bicara"):**
1. Sebelum mengirim, setiap perangkat Wi-Fi (AP maupun HP/laptop) **mendengarkan kanalnya dulu**.
2. Kalau ia mendengar perangkat lain sedang mengirim di kanal yang sama, dengan sinyal di atas ambang tertentu (standar 802.11: sekitar **−82 dBm** untuk 20 MHz), ia **wajib menunggu**.
3. Akibatnya, semua perangkat di kanal yang sama yang saling mendengar **berbagi waktu bicara (airtime)** secara bergiliran, walaupun mereka terhubung ke AP yang berbeda.

**Analogi:** satu ruang kelas, satu papan tulis, satu spidol.
- Kalau ada 2 dosen (2 AP) yang mengajar di ruang yang sama dan berbagi satu spidol (satu kanal), mereka harus bergantian menulis.
- Mahasiswa (klien) jadi lebih lama menunggu, walaupun suara dosennya keras (sinyal kuat).
- Kalau tiap dosen punya ruang sendiri (kanal berbeda), dua-duanya bisa mengajar bersamaan.

**Dampaknya:** sinyal bisa kuat (−50 dBm), tapi kecepatan turun, **latensi dan jitter naik**, dan ada **packet loss** karena tabrakan dan retransmisi. Ini persis yang kita temukan di titik 102: sinyal −49 dBm tapi loss 10%.

**Cara kita mengukur CCI** (aturan modul §4.5, dihitung oleh `analyze.py`):
- Di setiap titik ukur, cari dulu **AP pelayan**, yaitu AP `WiFi-UB.x` dengan sinyal terkuat.
- Lalu hitung **berapa radio lain (SSID apa pun) di kanal yang sama** yang terdengar **≥ −85 dBm**. Angka −85 diambil sedikit di bawah −82 sebagai margin.
- Angka itu adalah **CCI titik tersebut**. Kalau CCI > 2, titik itu masuk PERHATIAN.
- **Total CCI lantai 4 = jumlah CCI di 39 titik = 43.**

**Ukuran kedua, "tumpang tindih AP sekanal"** (dihitung oleh `solusi_L4.py`):
- Ada berapa titik di mana **dua AP lantai 4 yang memakai kanal sama** sama-sama terdengar ≥ −85 dBm.
- Kalau angka ini > 0, berarti sel kedua AP itu bersinggungan dan mereka **berebut airtime**.

### B5. Kanal DFS
- **DFS** = *Dynamic Frequency Selection*. Kanal 52–64 (dan 100–144) dipakai bersama dengan **radar** (radar cuaca, radar militer, radar bandara).
- Supaya Wi-Fi tidak mengganggu radar, AP di kanal DFS wajib:
  1. **Mendengarkan dulu ±60 detik** sebelum memakai kanal itu (*Channel Availability Check*).
  2. **Langsung pindah kanal** kalau mendeteksi radar. Saat pindah, klien bisa terputus beberapa detik.
- **Kelebihan:** kanal DFS biasanya **sepi**, karena banyak jaringan menghindarinya. Data kita membuktikannya: di lantai 4, kanal 60 dan 64 **tidak terdengar satu radio pun** (lihat gambar 7).
- **Kekurangan:**
  - Risiko pindah kanal mendadak kalau ada radar.
  - Sebagian perangkat lama tidak mendukung DFS.
- Fakta pendukung: **kampus sudah memakai kanal DFS di lantai 3** (kanal 52, 60, 64 terukur di data L3). Artinya controller dan mayoritas perangkat di FILKOM sudah terbukti bisa memakai DFS.

### B6. Lebar kanal: kenapa 20 MHz, bukan 40/80 MHz?
Kanal lebar memang membuat **satu perangkat lebih cepat**, tapi ada tiga harga yang harus dibayar.

**1. Jumlah kanal yang tidak tumpang tindih berkurang drastis** (hanya kanal non-DFS yang legal di Indonesia):

| Lebar | Jumlah kanal tidak tumpang tindih | Contoh |
|---|---|---|
| 20 MHz | **8** | 36, 40, 44, 48, 149, 153, 157, 161 |
| 40 MHz | **4** | 36-40, 44-48, 149-153, 157-161 |
| 80 MHz | **2** | 36-48, 149-161 |

Lantai 4 akan punya **10 AP**, dan kesepuluhnya saling mendengar (data: setiap pasangan AP L4 terdengar bersama di 9–37 titik). Konsekuensinya:
- Dengan 80 MHz, 10 AP harus berbagi 2 kanal, rata-rata **5 AP per kanal**. Kelima AP itu saling menunggu, jadi airtime tiap AP tinggal ±1/5.
- Dengan 20 MHz plus DFS, ada 12 kanal untuk 10 AP, jadi **setiap AP punya kanal sendiri**.

**2. Noise ikut membesar.**
- Derau termal = −174 dBm/Hz + 10·log₁₀(lebar). Hasilnya: 20 MHz ≈ −101 dBm, 40 MHz ≈ −98 dBm, 80 MHz ≈ −95 dBm.
- Setiap kali lebar kanal digandakan, noise naik 3 dB. SNR turun, sehingga modulasi cepat lebih susah dicapai.

**3. Butuh sinyal lebih kuat untuk kecepatan yang sama.**
- Contoh dari modul §4.3: MCS 9 butuh −57 dBm di 20 MHz, tapi −51 dBm di 80 MHz (6 dB lebih kuat).

**Kesimpulan:** di gedung padat yang banyak AP-nya (ruang kuliah), **banyak kanal sempit lebih baik daripada sedikit kanal lebar**. Analoginya jalan tol: 8 lajur kecil yang masing-masing dipakai 1 bus lebih lancar daripada 2 lajur besar yang masing-masing dipakai 5 bus bergantian.

**Bukti bahwa AP sekarang memang 20 MHz:**
- Kolom `width_mhz` di `data/passive_L4.csv` bernilai 20 untuk semua 8 AP.
- Link rate laptop di uji aktif selalu **286,5 Mbps**. Itu angka maksimum Wi-Fi 6 dengan 2 antena (2 spatial stream) di 20 MHz.

### B7. Daya pancar (Tx power): kenapa tidak "dinaikkan saja"?
Menaikkan daya **tidak menyelesaikan masalah kita**, malah memperparah.

1. **Sinyal sudah kuat** (97,4% titik ≥ −67 dBm). Yang kurang bukan kekuatan sinyal.
2. **Sel AP membesar.** Makin jauh sinyal AP terdengar, makin banyak AP sekanal yang saling dengar di atas −85 dBm. Akibatnya **CCI naik**.
3. **Link jadi asimetris.**
   - AP bisa memancar sampai 23 dBm (batas regulasi), tapi HP dan laptop biasanya hanya ±15 dBm.
   - Kalau daya AP dinaikkan, klien "mendengar" AP dari jauh, tapi AP **tidak bisa mendengar balasan klien dengan baik**. Akibatnya terjadi retransmisi dan kecepatan diturunkan.
4. **Sticky client.**
   - Laptop melihat AP jauh masih "kuat", jadi tidak mau pindah ke AP yang lebih dekat.
   - Contoh nyata: titik 007 di gedung utama justru dilayani **E1 (AP Ext F4.14)** dari seberang hall.
5. **Batas legal:** daya maksimum 200 mW / 23 dBm EIRP dalam ruangan (Permenkominfo 2/2023).

Karena itu solusinya justru **menurunkan** daya E1 sebanyak 6 dB. Sinyalnya −34 dBm di bawah AP, terlalu kuat, dan bocor ke gedung utama.

### B8. Roaming, sticky client, 802.11k/v/r
- **Roaming:** klien pindah dari satu AP ke AP lain saat berjalan.
  - Di Wi-Fi, **klien yang memutuskan** kapan pindah, bukan AP.
  - Klien sering terlambat pindah (*sticky*), atau malah pindah bolak-balik (*ping-pong*).
- **802.11k:** AP memberi tahu klien daftar AP tetangga, jadi klien tidak perlu scan semua kanal.
- **802.11v:** AP bisa "menyarankan" klien pindah ke AP yang lebih baik (*BSS transition*).
- **802.11r (Fast Transition):** mempercepat proses login ulang saat pindah AP.
  - Ini penting karena `WiFi-UB.x` memakai **WPA2/3-Enterprise** (login akun UB).
  - Tanpa 802.11r, setiap pindah AP harus login ulang ke server RADIUS, dan ini bisa makan waktu atau gagal.
- **Min-RSSI:** AP menolak atau melepas klien yang sinyalnya di bawah ambang (misal −72 dBm), supaya klien pindah ke AP yang lebih dekat.

### B9. Floor bleed (kebocoran antar-lantai)
- Sinyal AP di lantai 5 bisa menembus pelat beton dan terdengar di lantai 4.
- Karena SSID-nya sama, **laptop di lantai 4 bisa saja tersambung ke AP lantai 5**. Akibatnya beban AP lantai 5 bertambah dan roaming jadi kacau.
- **Redaman pelat lantai beton menurut pustaka: 20–30+ dB** (modul §4.2).
  - Kalau selisih sinyal antar-lantai jauh lebih kecil dari angka itu, berarti ada jalur bocor, misalnya void, tangga, atau shaft lift.

### B10. Kapasitas: berapa user yang bisa dilayani satu AP?
**Rumus sederhana:**

`jumlah AP yang dibutuhkan = (jumlah user × kebutuhan per user) ÷ kapasitas efektif per AP`

Asumsi yang kita pakai beserta sumbernya:

| Besaran | Nilai | Sumber |
|---|---|---|
| User per ruang kuliah saat penuh | **35** | asumsi kelompok (pengamatan kapasitas kursi, 30–40 orang) |
| Kebutuhan per user, skenario **normal** | **0,6 Mbps** | Zoom group video kualitas standar, unduh 600 kbps (Zoom Support) |
| Kebutuhan per user, skenario **berat** | **1,8 Mbps** | Zoom group video 720p HD, unduh 1,8 Mbps (Zoom Support) |
| Link rate laptop ke AP | **286,5 Mbps** | **terukur** di uji aktif (Wi-Fi 6, 2 stream, 20 MHz) |
| Kapasitas efektif per AP | **±100 Mbps** | asumsi konservatif ±35% dari link rate (overhead protokol, banyak klien, klien jauh memakai rate rendah). Bisa diverifikasi dengan iperf3. |
| Target beban maksimum | **≤ 70%** kapasitas | asumsi desain: sisakan ±30% untuk lonjakan dan retransmisi |

> Catatan jujur: angka **"25–30 klien per radio"** yang sempat ditulis di outline versi lama **tidak punya sumber yang bisa kita pertanggungjawabkan, jadi sudah dihapus** dan diganti perhitungan di atas.

---

## Bagian C: Asal data & file bukti

| Data | File | Isi |
|---|---|---|
| Survei pasif L4 / L3 / L5 | `data/passive_L4.csv`, `passive_L3.csv`, `passive_L5.csv` | Setiap baris = 1 BSSID terdengar di 1 titik pada 1 kali scan: SSID, BSSID, **kanal**, **lebar kanal**, RSSI |
| Rekap per titik | `data/rekap_L4.csv` | RSSI terkuat, kanal, BSSID terkuat per titik (bisa dibuka di Excel) |
| Pemetaan di bawah AP | `data/map_bssid_L4.csv` | Scan saat berdiri di bawah AP F4.4, F4.9, F4.10, F4.13, F4.14 (+F4.3) |
| Posisi AP | `data/ap_fisik_L4.csv` | Posisi AP yang dipakai di semua gambar + sumber posisinya. **Bisa diedit.** |
| Kalibrasi | `data/offset_kalibrasi.csv` | Laptop L3 −7,6 dB, laptop L5 −5,4 dB terhadap laptop L4 |
| Uji aktif | `data/active_L4.csv`, `raw/active/*.txt` | RSSI, link rate, RTT, jitter, loss per titik |
| Roaming | `raw/roaming_L4_R1.csv`, `raw/roaming_L4_R2.csv`, `raw/roaming_ping_*.txt` | AP tersambung per detik + log ping |
| Status & CCI per titik | `output/L4_titik.csv` | Kolom `cci`, `status`, `penyebab_utama` |
| **Bukti CCI** | `output/solusi_L4/bukti_cci_L4.csv` | **43 baris = 43 kejadian CCI**: titik, AP pelayan, kanal, radio pengganggu, SSID, RSSI, asal |
| Semua radio di L4 | `output/solusi_L4/radio_L4.csv` | 51 radio 5 GHz yang terdengar ≥ −85 dBm, beserta kanal, SSID, dan asal lantai |
| Floor bleed | `output/solusi_L4/floor_bleed_L4.csv`, `output/gedung_*.csv` | Radio L3/L5 yang terdengar di L4 + estimasi redaman lantai |
| Opsi kanal | `output/solusi_L4/opsi_kanal_L4.csv` | Perbandingan 4 opsi (sekarang, +AP saja, non-DFS, +DFS) |
| Validasi kanal | `output/solusi_L4/validasi_kanal_L4.csv` | Per kanal: AP mana yang memakai, tumpang tindih, radio lain |
| Prediksi | `output/solusi_L4/banding_titik_L4.csv` | RSSI & CCI per titik, sekarang vs setelah solusi |
| Spreadsheet vs survei | `output/solusi_L4/banding_spreadsheet_L4.csv` | Kanal di spreadsheet controller vs kanal terukur |

**Cara membuktikan kanal sebuah AP secara langsung (untuk demo/screenshot):**
1. Di Windows, buka PowerShell lalu jalankan `netsh wlan show networks mode=bssid`. Hasilnya menampilkan setiap BSSID beserta **Channel**, Signal, dan Radio type. Screenshot hasilnya saat berdiri di bawah AP.
2. Di Android, aplikasi **WiFiAnalyzer** (dipakai juga di modul) menampilkan grafik kanal. Screenshot tab "Channel Graph".
3. Di data kita, buka `data/map_bssid_L4.csv`, filter `ssid = WiFi-UB.x`, lalu lihat kolom `bssid`, `channel`, dan `width_mhz` untuk tiap AP.

---

## Bagian D: Slide per slide

Format tiap slide:
- **Di slide**: teks yang ditulis, singkat
- **Gambar**: file yang dimasukkan
- **Naskah lisan**: kalimat yang diucapkan, ±1–1,5 menit
- **Pendalaman**: wajib dipahami presenter, tapi tidak dibacakan
- **Bukti**: asal angka

| No | Bagian | Judul | Presenter | Waktu |
|---|---|---|---|---|
| 1 | Pembuka | Judul, tim & metodologi | Auliya | 1:00 |
| 2 | Latar belakang | Latar belakang & tujuan | Auliya | 1:00 |
| 3 | Deskripsi masalah | Fungsi ruang, jumlah user & kebutuhan kapasitas | Alif | 1:30 |
| 4 | Deskripsi masalah | Cakupan sinyal & posisi AP | Ghazy | 1:15 |
| 5 | Deskripsi masalah | **Temuan utama: co-channel interference** | Ghazy | 2:00 |
| 6 | Deskripsi masalah | Kepadatan kanal & asal radio | Ghazy | 1:00 |
| 7 | Deskripsi masalah | Kebocoran sinyal antar-lantai (L3/L5) | Bagas | 1:15 |
| 8 | Deskripsi masalah | Uji aktif & roaming: performa nyata | Alif | 1:30 |
| 9 | Desain solusi | Kriteria desain & alokasi sumber daya | Bagas | 1:45 |
| 10 | Desain solusi | Penempatan AP & rencana kanal di denah | Bagas | 1:00 |
| 11 | Pembahasan | Analisis, justifikasi feasible, keterbatasan | Ghazy | 1:30 |
| 12 | Kesimpulan | Kesimpulan & referensi | Auliya | 0:45 |
| | | | **Total** | **±15:30** |

---

### Slide 1: Judul, Tim & Metodologi

**Di slide**
- Judul: *Pemetaan Kualitas Sinyal Wi-Fi 5 GHz dan Usulan Penempatan AP, Lantai 4 Gedung FILKOM UB*
- Kelompok 6: Ghazy, Bagas, Alif, Auliya (+ NIM)
- Metodologi (ikon/diagram alur 4 kotak):
  **Survei pasif 65 titik** (L4: 39, L3: 13, L5: 13) → **Uji aktif 8 titik** → **Uji roaming 2 lintasan** → **Analisis** (heatmap, kanal, CCI, antar-lantai)
- Alat: 3 laptop Windows 11 (kartu Wi-Fi Realtek RTL8852AE), skrip Python (Windows Native WiFi API), dikalibrasi bersama

**Gambar:** `kelompok6/denah/peta_titik_L4_rev.png` (kecil, di kanan).

**Naskah lisan**
> "Kami Kelompok 6, memetakan Wi-Fi 5 GHz di lantai 4 FILKOM. Kami mengukur di 39 titik di lantai 4, ditambah 13 titik di lantai 3 dan 13 titik di lantai 5 untuk melihat kebocoran sinyal antar-lantai. Di tiap titik laptop men-scan semua sinyal Wi-Fi 3 kali. Setelah itu kami melakukan uji koneksi nyata di 8 titik dan uji berjalan sambil terhubung untuk melihat perpindahan AP. Semua laptop dikalibrasi bersama di satu titik supaya perbedaan antar-laptop bisa diketahui."

**Pendalaman**
- **Kenapa titik ditempatkan seperti itu?** Grid di tengah ruang dan koridor, ditambah titik "terjauh dari AP" (pojok ruang, tangga: titik 201–209) untuk mencari area terlemah. Titik 207/208 di tangga darurat tidak bisa dimasuki, jadi dihapus.
- **Titik L3/L5** berada tepat di atas/bawah titik L4 dengan nomor yang sama, supaya selisih sinyal antar-lantai bisa dibandingkan langsung.
- **Kalibrasi:** semua laptop men-scan bersamaan di hall L4. Selisih median bacaan untuk AP yang sama adalah offset laptop: **laptop L3 −7,6 dB, laptop L5 −5,4 dB** dibanding laptop L4. Offset ini dipakai saat membandingkan antar-lantai.
- **Keterbatasan Windows:** tidak memberikan *noise floor*, jadi SNR tidak bisa dihitung. Ini disebut di slide 11.

---

### Slide 2: Latar Belakang & Tujuan

**Di slide**
- Lantai 4 = ruang kuliah (12 kelas) dengan ratusan perangkat yang aktif bersamaan
- Semua AP memancarkan SSID yang sama (`WiFi-UB.x`), jadi pengguna tidak tahu tersambung ke AP mana, dan masalahnya tidak terlihat
- 5 GHz: kanal lebih banyak dan lebih cepat, tapi jangkauan lebih pendek, sehingga **penempatan AP dan pembagian kanal menjadi kritis**
- **Tujuan:**
  1. Memetakan kualitas sinyal 5 GHz lantai 4
  2. Menemukan area bermasalah dan **akar masalahnya**
  3. Mengusulkan jumlah AP, kanal, daya, dan penempatan berbasis data

**Gambar:** opsional, foto koridor atau AP di plafon.

**Naskah lisan**
> "Wi-Fi kampus memakai satu nama jaringan untuk semua AP. Dari sisi pengguna, yang terlihat hanya 'tersambung' atau 'lambat', tanpa tahu penyebabnya. Kami ingin menjawab tiga hal: di mana area bermasalah, apa akar masalahnya, dan bagaimana memperbaikinya dengan bukti data, bukan tebakan."

**Pendalaman**
- 5 GHz mengalami redaman jarak ±6,5 dB lebih besar daripada 2,4 GHz (rumus FSPL di modul §4.1), dan juga lebih teredam dinding. Jadi satu AP 5 GHz menjangkau area yang lebih kecil.
- Di sisi lain, 5 GHz punya 12 kanal 20 MHz yang legal, sedangkan 2,4 GHz praktis hanya 3. Inilah kenapa pembagian kanal di 5 GHz bisa (dan harus) direncanakan.

---

### Slide 3: Deskripsi Masalah: Fungsi Ruang, Jumlah User & Kebutuhan Kapasitas

**Di slide**

| Area | Fungsi | Perkiraan user saat penuh |
|---|---|---|
| F4.1–F4.6 (gedung utama) | Ruang kuliah | 6 kelas × 35 = **210** |
| F4.9–F4.14 (Ext) | Ruang kuliah | 6 kelas × 35 = **210** |
| F4.7, F4.8 | *[isi fungsi ruang]* | *[isi]* |
| Hall, R. Duduk, koridor | Menunggu kelas, lalu-lalang | ±10–20 |
| **Total** | | **±420+ user** |

Aplikasi: LMS, slide, browsing, video/kuliah daring.

Kebutuhan kapasitas (per gedung, 210 user):

| Skenario | Per user | Total | Beban dengan 4 AP | Beban dengan 6 AP |
|---|---|---|---|---|
| Normal (kualitas video standar) | 0,6 Mbps | 126 Mbps | 32% | 21% |
| Berat (semua video 720p) | 1,8 Mbps | 378 Mbps | **95%** ❌ | **63%** ✅ |

**Gambar:** foto suasana kelas (kalau ada).

**Naskah lisan**
> "Lantai 4 berisi 12 ruang kuliah. Kami asumsikan saat penuh tiap kelas diisi 35 orang, jadi ada sekitar 420 pengguna. Kalau semua menonton video kuliah 720p, kebutuhan per orang sekitar 1,8 Mbps, sesuai panduan resmi Zoom. Gedung utama sekarang punya 4 AP. Dengan kapasitas efektif sekitar 100 Mbps per AP, bebannya mencapai 95% pada skenario berat, terlalu mepet. Ini salah satu dasar usulan kami menambah AP."

**Pendalaman**
- **Hitungan:** 210 user × 1,8 Mbps = 378 Mbps. Dibagi (4 AP × 100 Mbps) = 95%. Dengan 6 AP: 378 ÷ 600 = 63%, di bawah target 70%.
- **Kenapa kapasitas efektif ±100 Mbps padahal link rate 286,5 Mbps?**
  - Link rate adalah kecepatan "mentah" di udara. Sebagian waktu habis untuk antre (CSMA/CA), header, ACK, dan retransmisi.
  - Klien yang jauh juga memakai kecepatan lebih rendah, sehingga memakan airtime lebih lama.
  - Kami ambil ±35% sebagai angka konservatif. Ini **asumsi**, dan bisa diverifikasi dengan uji iperf3.
- **Kapasitas efektif hanya berlaku kalau AP punya kanal sendiri.** Kalau 2 AP berbagi kanal dan saling dengar, kapasitas 100 Mbps itu dibagi berdua. Inilah hubungan masalah kapasitas dengan CCI (slide 5).
- **Ext juga 95% pada skenario berat dengan 4 AP.** Ini masuk rekomendasi tahap 3 (kondisional) di slide 9.
- **Data controller (spreadsheet) tidak dipakai sebagai angka utama**, karena data itu dari 26-08-2025 dan sudah tidak sesuai kondisi sekarang (lihat Bagian E no. 5). Hanya disebut sebagai pembanding kalau ditanya: dulu tercatat ±364 klien di 8 AP L4, sejalan dengan estimasi kita.
- Angka 35 orang per kelas adalah **asumsi kelompok**, bukan hasil hitung orang saat survei. Katakan itu terus terang.

---

### Slide 4: Cakupan Sinyal & Posisi AP

**Di slide**
- **97,4%** titik ≥ −67 dBm (baik), **100%** titik ≥ −70 dBm, **0 blank spot**
- Median −56 dBm. Titik terlemah **−69 dBm di L4-006** (pojok kiri-atas, dekat toilet)
- Semua titik punya AP cadangan ≥ −75 dBm (syarat roaming terpenuhi)
- **8 AP 5 GHz:** M1–M4 di gedung utama, E1–E4 di Ext, semua 20 MHz
- Pojok kiri-atas (F4.2) & F4.8 tidak punya AP di dekatnya
- **Kesimpulan: kekuatan sinyal BUKAN masalah utama**

**Gambar:** `1_heatmap_AP_L4.png` (besar). Opsional: `2_posisi_area_AP_L4.png` (area layanan tiap AP) sebagai gambar kecil atau slide cadangan.

**Naskah lisan**
> "Ini heatmap sinyal lantai 4. Hijau artinya kuat. Garis hijau adalah batas −67 dBm, yaitu batas aman untuk video call. Hampir seluruh lantai berada di atas batas itu, dan tidak ada blank spot. Segitiga adalah posisi 8 AP 5 GHz beserta kanalnya. Area paling lemah ada di pojok kiri-atas dekat toilet, −69 dBm, karena tidak ada AP di sana. Tapi secara umum sinyalnya bagus. Pertanyaannya: kalau sinyal bagus, kenapa masih lambat? Jawabannya di slide berikutnya."

**Pendalaman**
- **Cara baca heatmap:**
  - Warna dibuat dengan interpolasi antar-titik ukur, maksimal 6 m dari titik terdekat.
  - Area putih berarti **tidak ada titik ukur** di sana, bukan blank spot.
  - Angka di samping titik adalah RSSI AP terkuat.
- **Posisi AP (estimasi vs fisik, poin wajib modul):**
  - **Fisik / pemetaan langsung:** M1 (F4.4) dan E1–E4 (Ext F4.14, F4.10, F4.13, F4.9). Kami berdiri tepat di bawah AP dan men-scan. BSSID terkuat = AP itu.
  - **Estimasi:** M2, M3, dan M4. Posisinya dihitung dari rata-rata berbobot 3 titik dengan sinyal terkuat AP tersebut, karena AP ada di plafon ruang yang tidak bisa kami masuki.
  - Posisi bisa dikoreksi di `data/ap_fisik_L4.csv`.
- **Gambar area layanan (`2_posisi_area_AP_L4.png`)** menunjukkan titik L4-007 (gedung utama) **dilayani E1 di Ext**, dari seberang hall. Ini tanda E1 terlalu kuat dan ada celah AP di kiri-atas.
- **Bukti angka:** `output/L4_ringkasan.txt` dan `output/L4_titik.csv` (kolom `rssi1`, `rssi2`).

---

### Slide 5: Temuan Utama: Co-Channel Interference (CCI)

**Di slide**
- CCI = beberapa radio di **kanal yang sama** saling dengar, sehingga harus **bergiliran memakai airtime**. Akibatnya lambat dan loss walaupun sinyal kuat
- Aturan modul: radio sekanal ≥ −85 dBm; CCI > 2 = bermasalah
- **Total 43 kejadian CCI di 39 titik**; 6 titik CCI > 2
- **M2 & E3 sama-sama di kanal 153**, terdengar bersamaan di 9 titik
- Terparah: **hall (L4-000) dan L4-206: 6 radio sekanal**; L4-001: 5; L4-102: 4
- Pengganggu: AP kampus yang tidak memancarkan WiFi-UB.x, AP lantai 3, hotspot/jaringan lab

**Gambar:**
- Utama: `6_bukti_cci_L4.png` (spektrum di 4 titik terparah). Kalau terlalu ramai, crop panel **L4-000** saja.
- Pendamping kecil: `3_kanal_L4.png` (denah: kanal tiap AP + garis merah M2–E3 + lingkaran CCI per titik).

**Naskah lisan**
> "Ini temuan utama kami. Di Wi-Fi, perangkat di kanal yang sama harus bergiliran bicara: dengar dulu, kalau ada yang bicara, tunggu. Kalau banyak radio di satu kanal saling mendengar, waktu bicara dibagi-bagi. Akibatnya lambat, walaupun sinyalnya kuat.
> Grafik ini adalah 'spektrum' di 4 titik terparah. Sumbu bawah adalah kanal, sumbu kiri kekuatan sinyal. Bintang adalah AP yang melayani titik itu, pita kuning adalah kanalnya. Semua titik di pita kuning di atas garis putus-putus −85 dBm adalah pengganggu. Contohnya di hall, titik 000: AP pelayannya M2 di kanal 153, dan ada 6 radio lain di kanal 153 yang terdengar. Di seluruh lantai 4 kami menemukan 43 kejadian seperti ini. Kami juga menemukan dua AP lantai 4, M2 dan E3, memakai kanal yang sama, yaitu 153."

**Pendalaman: asal angka 43 (wajib paham)**
1. Buka `output/L4_titik.csv`, lalu jumlahkan kolom `cci`. Hasilnya **43**:
   - 000=6, 001=5, 003=1, 008=1, 010=2, 011=2, 101=3, 102=4
   - 104=2, 105=2, 106=1, 107=4, 108=2, 203=1, 205=1, 206=6
2. Rincian tiap kejadian ada di `output/solusi_L4/bukti_cci_L4.csv` (**43 baris**): titik, AP pelayan, kanalnya, radio pengganggu, SSID-nya, RSSI-nya, dan asalnya.
3. Asal 43 pengganggu itu:

| Asal pengganggu | Jumlah |
|---|---|
| Jaringan lain (lab, hotspot, fakultas lain) | 21 |
| AP kampus yang bukan 8 AP L4 (radio yang hanya memancarkan eduroam/FILKOM EVENT, atau dari area lain) | 17 |
| AP lantai 3 | 4 |
| AP L4 lain di kanal yang sama | 1 |

**Kenapa radio non-WiFi-UB.x ikut dihitung?** CSMA/CA tidak peduli nama jaringan. Semua perangkat Wi-Fi di kanal yang sama harus bergiliran.

**Apakah ada masalah pemilihan kanal? Ya, ada 3:**
- **(1)** M2 dan E3 memakai kanal yang sama (153) dan saling dengar.
- **(2)** AP L4 ditempatkan di kanal 149–161 (M2, M3, E1, E3), yang paling ramai jaringan lain.
- **(3)** Kanal 52–64 di lantai 4 kosong, tapi tidak dimanfaatkan.

**Bukti kanal yang dipakai tiap AP:**
- `data/map_bssid_L4.csv` dan `data/passive_L4.csv` (kolom `channel`, `width_mhz`)
- Bisa didemokan dengan `netsh wlan show networks mode=bssid` atau WiFiAnalyzer (Bagian C)

---

### Slide 6: Kepadatan Kanal & Asal Radio

**Di slide**
- 51 radio 5 GHz terdengar di lantai 4 (≥ −85 dBm). Hanya **8** yang AP WiFi-UB.x lantai 4
- Kanal **149–161 paling padat** (17–20 radio per kanal): kebanyakan jaringan lain dan radio kampus non-WiFi-UB.x
- Kanal **36–48 lebih sepi** (2–5 radio)
- Kanal **60 dan 64 (DFS) kosong**, belum dimanfaatkan
- Hotspot HP 80 MHz terdengar −35 dBm di Ext, menduduki 4 kanal sekaligus (149–161)

**Gambar:** `7_radio_per_kanal_L4.png` (grafik batang bertumpuk + tabel 14 radio pengganggu terkuat).

**Naskah lisan**
> "Grafik ini menghitung berapa radio yang terdengar di tiap kanal di lantai 4, dan dari mana asalnya. Biru adalah AP kita sendiri, abu-abu jaringan lain seperti lab atau hotspot HP, ungu AP kampus lain. Kanal 149 sampai 161 sangat padat, 17–20 radio per kanal, padahal 4 AP lantai 4 ditaruh di sana. Sebaliknya, kanal 60 dan 64 kosong sama sekali. Ini dasar rencana kanal baru kami."

**Pendalaman**
- **Cara grafik dibuat:** dari `data/passive_L4.csv`, ambil semua radio 5 GHz yang pernah terdengar ≥ −85 dBm di salah satu titik L4, lalu hitung kanal yang didudukinya. Radio 40/80 MHz dihitung di setiap kanal yang ditempatinya. Daftar lengkap ada di `output/solusi_L4/radio_L4.csv`.
- **Klasifikasi asal radio:**
  - "AP WiFi-UB.x L4": 8 AP yang dipetakan.
  - "AP lantai 3/5": sinyalnya ≥ 3 dB lebih kuat di lantai itu daripada di L4, setelah koreksi offset laptop.
  - "AP kampus lain": memancarkan SSID kampus (eduroam/FILKOM EVENT/WiFi-UB), tapi bukan 8 AP L4 dan tidak jelas dari lantai lain. Modul §4.4 menyebut ada radio kampus yang hanya memancarkan eduroam dan FILKOM EVENT tanpa WiFi-UB.x. Radio ini tidak membantu pengguna WiFi-UB.x, tapi tetap memakan airtime.
  - "Jaringan lain": SSID non-kampus (ROBOTIIK, AP-HOST, FKUB, FEB-UB, hotspot HP).
- **Kenapa 149–161 padat?** Banyak router atau hotspot rumahan memakai UNII-3 dan lebar 80 MHz secara default. Satu hotspot 80 MHz di kanal 149 menduduki 149, 153, 157, dan 161 sekaligus.
- **Nama SSID pribadi disamarkan** di gambar dan CSV (privasi).

---

### Slide 7: Kebocoran Sinyal Antar-Lantai (Lantai 3 & 5)

**Di slide**
- **10 dari 39 titik L4** mendengar AP lantai 5/3 dengan sinyal ≥ −75 dBm
- Di **6 titik**, AP lantai 5 hanya kalah ≤ 6 dB dari AP lantai 4, sehingga laptop bisa tersambung ke AP lantai 5. Contoh **L4-010: AP L5 −53 vs AP L4 −52 dBm (selisih 1,5 dB)**
- Kebocoran dari **lantai 5 dominan**; dari lantai 3 lemah (maks. −81 dBm di L4)
- Estimasi redaman pelat lantai (titik tegak lurus, sudah dikoreksi offset laptop): **26 dB dan 30 dB**, sesuai pustaka 20–30 dB. **Anomali: 9 dB** di atas F4.6 (L5-010 → L4-010)
- Belum ada titik L4 yang **paling kuat** dilayani AP lantai lain

**Gambar:** `8_floor_bleed_L4.png` (denah L4 dengan sinyal AP L5/L3 + grafik redaman lantai). Pendukung: `output/gedung_floor_bleed.csv`.

**Naskah lisan**
> "Kami juga mengukur lantai 3 dan 5 untuk melihat apakah sinyal antar-lantai saling bocor. Lingkaran merah adalah sinyal AP lantai 5 yang terdengar di lantai 4. Di 6 titik, sinyal AP lantai 5 hampir sama kuat dengan AP lantai 4. Di titik 010 selisihnya hanya 1,5 dB, jadi laptop di sana bisa saja tersambung ke AP lantai 5. Redaman pelat lantai rata-rata 26–30 dB, sesuai literatur, kecuali di atas F4.6 yang hanya 9 dB. Ini kemungkinan ada jalur bocor seperti void atau tangga. Sinyal dari lantai 3 lemah, jadi tidak bermasalah."

**Pendalaman**
- **Cara menghitung redaman lantai:**
  1. Ambil AP lantai 5 di titik L5 tempat sinyalnya paling kuat (contoh: L5-007 = −38,6 dBm setelah koreksi).
  2. Ukur AP yang sama di titik L4 dengan nomor sama, yang posisinya tepat di bawahnya (L4-007 = −68,6 dBm).
  3. Selisihnya, **30 dB**, adalah perkiraan redaman pelat lantai.
- **Koreksi offset:** laptop L5 membaca 5,4 dB lebih lemah, jadi nilai L5 ditambah 5,4 dB sebelum dibandingkan. Laptop L3 ditambah 7,6 dB.
- **Kenapa ini penting?**
  - SSID semua lantai sama, jadi laptop bebas pindah ke AP lantai 5. AP lantai 5 jadi menanggung beban lantai 4, dan roaming makin acak.
  - Sinyal bocor yang sekanal juga menambah CCI. Kanal L5 yang bocor adalah 40, 48, dan 161. Rencana kanal baru sudah memperhitungkan sinyal ini.
- **Keterbatasan:** L3 dan L5 hanya 13 titik, dan banyak ruang dosen tertutup. Jadi titik "terkuat" di L5 belum tentu tepat di bawah AP, dan nilai redaman adalah perkiraan kasar. Ini sesuai catatan modul §9.5.
- **Kolom file:**
  - `gedung_floor_bleed.csv`: `lantai_asal` (lantai tempat radio paling kuat), `rssi_asal`, `rssi_tetangga`, `selisih_db`
  - `gedung_titik_lantai_lain.csv`: setiap titik dengan `dari_lantai_lain = True/False`. Untuk L4, semuanya False.

---

### Slide 8: Uji Aktif & Roaming: Performa Nyata

**Di slide**

Uji aktif (8 titik; batas modul: RTT ≤ 50 ms, loss ≤ 2%):

| Titik | RSSI | RTT | Jitter | Loss | Catatan |
|---|---|---|---|---|---|
| 102 (Ext) | −49 | 30 ms | 2 ms | **10%** ❌ | sinyal kuat tapi loss, CCI 4 |
| 203 (F4.8) | −64 | **108 ms** | **97 ms** | **5%** ❌ | pojok tanpa AP |
| 007 | −70 | **72 ms** | 59 ms | **5%** ❌ | dilayani AP Ext |
| 000 (hall) | −65 | **118 ms** | 60 ms | 0% | CCI 6 |
| 017 | −58 | **132 ms** | 76 ms | 0% | latensi tinggi |
| 101 / 106 / 006 | −43 / −53 / −65 | 55 / 42 / 39 ms | | 0% | relatif baik |

Roaming:
- **R1** (keliling gedung utama): pindah AP 1× (M1→M3), ping putus ±4 detik
- **R2** (Ext ↔ gedung utama): pindah AP **12×**, termasuk ping-pong M3→E2→M3 dalam 10 detik
- ⚠️ **Setelah pindah AP, laptop tetap "tersambung" tapi internet mati**: 69% ping gagal selama 3,5 menit, 6 uji aktif gagal, dan baru pulih setelah **reconnect manual**

**Gambar:** `9_timeline_roaming_L4.png` (utama). Opsional: `output/L4_status.png`.

**Naskah lisan**
> "Untuk membuktikan dampaknya, kami melakukan uji koneksi nyata. Tabel ini menunjukkan titik 102 di Ext: sinyalnya sangat kuat, −49 dBm, tapi 10% paket hilang. Ini ciri khas interferensi, bukan sinyal lemah. Lima dari delapan titik punya latensi di atas 50 ms.
> Temuan paling serius ada di grafik ini. Garis atas menunjukkan AP mana yang dipakai laptop dari waktu ke waktu, dan grafik bawah adalah hasil ping. Setelah laptop berpindah AP, terutama setelah bolak-balik M3–E2 pukul 11:21, laptop tetap terlihat tersambung, tapi 69% ping gagal selama sekitar 3,5 menit. Uji aktif di 6 titik juga gagal karena alamat server tidak bisa ditemukan. Koneksi baru normal setelah kami putus dan sambung ulang secara manual. Setelah itu, uji ulang di semua titik berhasil."

**Pendalaman: arti tiap kolom**
- **RTT** (*round-trip time*): waktu bolak-balik paket dari laptop ke server dan kembali. > 50 ms terasa lambat untuk video call (batas modul).
- **Jitter:** seberapa berubah-ubah RTT. Jitter tinggi membuat video call patah-patah.
- **Loss:** persentase paket yang hilang. > 2% = BURUK (modul). Satu titik diuji 20 paket, jadi **loss 5% = 1 paket hilang** (indikatif) dan 10% = 2 paket.
- RTT diukur ke internet (filkom.ub.ac.id lewat Cloudflare, atau 1.1.1.1). Jadi angkanya termasuk jaringan kampus ke internet, bukan hanya Wi-Fi. Perbandingan antar-titik tetap bermakna karena jalurnya sama.

**Apa yang terjadi saat koneksi putus?** (kronologi dari `raw/roaming_L4_R2.csv` + `raw/roaming_ping_L4_R2.txt`):

| Jam | Kejadian |
|---|---|
| 11:19:03 | Laptop pindah ke M2 |
| 11:19:47–11:21:10 | Uji aktif di 203, 006, 007 (2×) **gagal**: "Ping request could not find host filkom.ub.ac.id" |
| 11:21:42–11:21:52 | Ping-pong M3 → E2 → M3 |
| 11:22:09–11:25:31 | **38 dari 55 ping gagal** (69%). Laptop tetap tersambung ke AP (BSSID ada di log). Uji aktif 101 & 106 gagal |
| 11:25:31 | **Reconnect manual** (di log terlihat BSSID 00:00:00…, artinya laptop sempat lepas sebentar) |
| 11:25:32 | Tersambung ke E1, ping normal lagi |
| 11:34–11:39 | Uji aktif diulang (target 1.1.1.1), **semua berhasil** |

**Interpretasinya:**
- Sambungan radio (layer 2) masih ada, tapi **jalur data/IP (layer 3) tidak jalan**: DNS tidak bisa diakses dan ping tidak dibalas.
- Kemungkinan penyebab, dari yang paling mungkin:
  - **(a)** Proses login ulang 802.1X / WPA2-Enterprise setelah pindah AP gagal atau macet. Jaringan tanpa 802.11r/OKC harus login ulang penuh setiap pindah AP.
  - **(b)** Masalah DHCP/DNS di sisi jaringan kampus.
  - **(c)** Driver kartu Wi-Fi laptop.
- **Kami tidak bisa memastikan yang mana** dari data kami. Ini yang perlu dilaporkan ke admin. Polanya konsisten: gangguan muncul **setelah pindah AP** dan hilang **setelah sambung ulang**.

**Catatan metode:**
- Uji 000 dan 017 memakai TCP port 443 ke filkom.ub.ac.id, karena ping ICMP tidak dibalas.
- 6 titik lain memakai ICMP ke 1.1.1.1, karena DNS sempat gagal.
- Keduanya server Cloudflare, jadi hasilnya masih sebanding.
- RSSI di log roaming Windows adalah perkiraan dari persentase kualitas sinyal.

---

### Slide 9: Desain Solusi: Kriteria & Alokasi Sumber Daya

**Di slide**

**Kriteria desain** (ditentukan dulu, baru solusi dirancang):

| No | Kriteria | Target | Sumber |
|---|---|---|---|
| K1 | Cakupan | ≥ 95% titik ≥ −67 dBm, tanpa blank spot | modul §4.5 |
| K2 | Roaming | AP cadangan ≥ −75 dBm di semua titik | modul §4.5 |
| K3 | Interferensi | CCI ≤ 2 per titik; **tidak ada 2 AP L4 sekanal yang saling dengar** | modul §4.5 |
| K4 | Kapasitas | beban ≤ 70% pada skenario berat | perhitungan slide 3 |
| K5 | Regulasi | kanal & daya sesuai Permenkominfo 2/2023 | regulasi |
| K6 | Biaya | maksimalkan AP yang ada; ubah lewat controller dulu | praktis |

**Alokasi sumber daya:**

| Komponen | Sekarang | Usulan | Alasan |
|---|---|---|---|
| Jumlah AP | 8 | **10** (+N1 di F4.2, +N2 di F4.8) | K1 & K4 |
| Lebar kanal | 20 MHz | **20 MHz** | K3: lebar = kanal sedikit = CCI |
| Kanal | 36, 40, 44, 48, 153×2, 157, 161 | **12 kanal legal, 1 kanal = 1 AP** (2 AP di DFS) | K3 |
| Daya | default | **E1 −6 dB** | sinyal −34 dBm, bocor ke 007 |
| Roaming | – | **802.11k/v/r + min-RSSI ±−72 dBm** | temuan putus koneksi |

Rencana kanal:

| AP | M1 | M2 | M3 | M4 | E1 | E2 | E3 | E4 | N1 | N2 |
|---|---|---|---|---|---|---|---|---|---|---|
| Lama | 36 | 153 | 161 | 44 | 157 | 40 | 153 | 48 | – | – |
| **Baru** | 36 | **64** | **149** | 44 | **60** | **157** | **40** | **153** | **161** | **48** |

**Gambar:** tabel saja. Boleh tambah tabel kecil "4 opsi kanal" (lihat Pendalaman).

**Naskah lisan**
> "Sebelum merancang, kami tetapkan enam kriteria: cakupan, roaming, interferensi, kapasitas, regulasi, dan biaya. Dari kriteria itu, kami mengusulkan tiga hal.
> Pertama, tambah dua AP di pojok yang lemah, sehingga gedung utama punya 6 AP dan beban skenario berat turun dari 95 ke 63%.
> Kedua, semua AP tetap di lebar 20 MHz. Kanal ditata ulang supaya **setiap AP lantai 4 punya kanal sendiri**. Dengan 10 AP, 8 kanal non-DFS tidak cukup, jadi 2 AP kami tempatkan di kanal DFS 60 dan 64, yang di lantai 4 kosong sama sekali.
> Ketiga, turunkan daya AP Ext F4.14 sebanyak 6 dB, dan aktifkan fitur roaming 802.11k/v/r."

**Pendalaman: arti tabel "Kanal"**
- **Kolom "Sekarang"** berisi 8 AP di 7 kanal berbeda. Kanal 153 dipakai 2 AP (M2 dan E3), itulah yang dimaksud "153×2".
- **Kolom "Usulan" berarti:**
  - Pakai **ke-12 kanal 20 MHz yang legal** di Indonesia: 36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161.
  - Setiap AP mendapat kanal yang **berbeda** dari 9 AP lainnya.
  - Dua AP (M2 dan E1) memakai kanal DFS 60/64.

**Cara rencana kanal dicari** (`solusi_L4.py`):
1. Data yang dipakai: sinyal setiap AP di 39 titik (terukur), sinyal 2 AP baru (diprediksi model, slide 11), dan semua radio lain yang terukur (lantai 3/5, jaringan lain, beserta kanalnya).
2. **Skor sebuah rencana** = CCI (cara modul) + jumlah titik tumpang tindih AP sekanal + 3 × jumlah AP di DFS. Penalti DFS supaya DFS hanya dipakai kalau benar-benar membantu.
3. Komputer mencoba mengganti kanal satu AP sekali waktu. Kalau skornya turun, perubahan disimpan. Proses diulang sampai tidak bisa turun lagi, dari 30 titik awal acak, lalu diambil yang terbaik (*local search*).

**Perbandingan 4 opsi** (`opsi_kanal_L4.csv`):

| Opsi | CCI (metode modul) | Titik tumpang tindih AP sekanal | AP di DFS |
|---|---|---|---|
| Sekarang (8 AP) | 43 | 9 | 0 |
| +2 AP, kanal lama dibiarkan | 43 | **36** ⬆️ (makin parah) | 0 |
| +2 AP, kanal baru, hanya non-DFS | 10 | 32 | 0 |
| **+2 AP, kanal baru + DFS (usulan)** | **2** | **0** | 2 |

- **Menambah AP tanpa mengatur kanal justru memperparah** (tumpang tindih 9 → 36).
- Tanpa DFS, tumpang tindih tetap tinggi (32), karena 10 AP > 8 kanal non-DFS, jadi pasti ada 2 pasang AP berbagi kanal. Padahal semua AP L4 saling dengar.

**Cara mengecek rencana kanal valid** (`validasi_kanal_L4.csv`), dengan 3 syarat:
1. **Legal:** semua kanal ada di daftar 12 kanal (B3). ✅
2. **Tidak ada AP L4 sekanal:** setiap kanal di rencana usulan dipakai **tepat 1 AP L4**, jadi tumpang tindih = 0. ✅
3. **Radio lain di kanal itu lemah atau tidak ada:** di kanal 60/64 tidak ada radio lain sama sekali. Di 149–161 masih ada radio lain, tapi pada titik-titik yang dilayani AP tersebut sisa CCI hanya 2.

Lalu cek ulang di lapangan setelah diterapkan: survei ulang, bandingkan dengan `banding_titik_L4.csv`.

**Bedanya dengan 2,4 GHz:** di 2,4 GHz pilihan aman hanya 1/6/11 (3 kanal), karena kanal yang bersebelahan tumpang tindih. Di 5 GHz dengan 20 MHz, **semua kanal berbeda pasti tidak tumpang tindih**. Tugas kita hanya memastikan **AP yang saling dengar tidak memakai kanal yang sama**.

**Rekomendasi bertahap:**

| Tahap | Isi | Biaya |
|---|---|---|
| **Tahap 1** | Ubah kanal, turunkan daya E1, aktifkan 802.11k/v/r + min-RSSI | 0, cukup lewat controller |
| **Tahap 2** | Pasang N1 dan N2 | 2 AP + kabel/PoE |
| **Tahap 3** (kondisional) | Kalau utilisasi kanal di controller Ext > 50% saat jam sibuk, tambah 1 AP di Ext F4.11/F4.12 | hitungan kapasitas Ext juga 95% pada skenario berat |

**Kalau dosen menolak DFS:** pakai rencana non-DFS (CCI 10, tumpang tindih 32). Ini tetap lebih baik dari sekarang soal CCI, tapi ada 2 pasang AP yang berbagi kanal.

---

### Slide 10: Penempatan AP & Rencana Kanal di Denah

**Di slide**
- ★ **N1 di F4.2 (kiri-atas), kanal 161:** menutup 005/006/007/008. Sekarang titik terlemah −69 dBm, dan 007 dilayani AP Ext
- ★ **N2 di F4.8 (kanan-atas), kanal 48:** menutup 003/203. Sekarang −63 dBm, jitter 97 ms, loss 5%
- Label tiap AP: kanal lama → baru
- Panah oranye: sinyal E1 bocor sampai 007, sehingga daya E1 diturunkan 6 dB
- Pemasangan di plafon, di tengah ruang, menjauhi kolom beton dan shaft lift

**Gambar:** `4_solusi_L4.png` (penuh). Kotak teks kanan boleh di-crop karena sudah ada di slide 9.

**Naskah lisan**
> "Ini posisi usulan. Bintang adalah AP baru. N1 di F4.2, pojok kiri-atas yang sekarang paling lemah dan terhalang lift dan toilet. N2 di F4.8, ruang yang menonjol di sisi atas, tempat kami mengukur jitter 97 ms. AP lama tidak perlu dipindah, cukup diganti kanalnya lewat controller. Panah oranye menunjukkan sinyal AP Ext yang terlalu kuat sampai menyeberang ke gedung utama, sehingga dayanya kami turunkan."

**Pendalaman**
- **Kenapa di dalam ruang, bukan di koridor?** Modul §9.4: AP di koridor yang melayani ruang kelas akan teredam dinding dan pintu (bata 8–15 dB, pintu 4–6 dB). AP di dalam ruang langsung melayani penggunanya.
- **Kenapa pojok kiri-atas lemah?** Ada inti lift, toilet, dan tangga. Material beton/bata dan logam lift meredam lebih dari 20 dB. Selain itu tidak ada AP di sisi kiri-atas.
- **Kenapa N2 di F4.8, bukan menggeser M1?** M1 sudah melayani F4.4 dengan baik (−53 dBm). Kalau digeser ke F4.8, F4.4 jadi lemah. Menambah AP juga menambah kapasitas (slide 3).
- Posisi N1/N2 adalah usulan berdasarkan denah. Saat pemasangan, cek ketersediaan kabel/PoE dan jalur plafon ke admin.

---

### Slide 11: Pembahasan: Analisis, Justifikasi & Keterbatasan

**Di slide**

| Indikator | Sekarang | Setelah solusi (prediksi) | Kriteria |
|---|---|---|---|
| Titik ≥ −67 dBm | 97,4% | **100%** | K1 ✅ |
| RSSI terlemah | −69,2 dBm | **−60,8 dBm** | K1 ✅ |
| CCI total (metode modul) | 43 | **2** | K3 ✅ |
| Tumpang tindih AP sekanal | 9 titik | **0** | K3 ✅ |
| CCI hall (000) | 6 | **0** | K3 ✅ |
| Beban gedung utama (skenario berat) | 95% | **63%** | K4 ✅ |

Contoh per titik: 006: −69 → −56 · 007: −64 → −56 · 203: −63 → −49 dBm

**Feasible karena:**
- Tahap 1 gratis (konfigurasi controller)
- Hanya +2 AP dari model yang sama
- Kanal & daya sesuai regulasi (izin kelas, maks. 23 dBm)
- DFS sudah dipakai di lantai 3

**Keterbatasan:**
- Tidak ada SNR (Windows)
- Prediksi = model tanpa dinding
- Posisi M2–M4 hasil estimasi
- 1 slot waktu survei
- 20 paket per uji aktif

**Gambar:** `5_prediksi_sebelum_sesudah_L4.png`.

**Naskah lisan**
> "Bagaimana kami tahu solusinya berhasil? Kami membuat model penurunan sinyal dari data survei kami sendiri, lalu menghitung ulang kondisi setelah solusi. Hasilnya: semua titik di atas −67 dBm, CCI turun dari 43 menjadi 2, dan tidak ada lagi dua AP lantai 4 yang berbagi kanal. Solusinya juga realistis: tahap pertama hanya konfigurasi tanpa biaya, dan tahap kedua cuma dua AP. Tapi ini prediksi model, jadi perlu divalidasi dengan survei ulang setelah diterapkan."

**Pendalaman: model prediksi**
- **Rumus log-distance** (modul §4.1): `RSSI(d) = P − 10·n·log₁₀(d)`.
  - `P` = sinyal pada jarak 1 m (dihitung per AP).
  - `n` = eksponen redaman, dicari dari data kita: **n = 2,47**. Ruang bebas n = 2, gedung penuh dinding 3,5–4. Jadi n = 2,47 cocok untuk gedung dengan koridor cincin yang cukup terbuka.
  - **Galat model (RMSE) = 5,6 dB**, artinya rata-rata meleset ±5,6 dB dibanding hasil ukur.
  - Model **tidak menghitung dinding**, jadi bisa terlalu optimis. Karena itu sinyal AP baru **dibatasi maksimal −48,8 dBm**, yaitu sinyal terbaik yang pernah terukur dari AP gedung utama.
- **Cara menghitung "setelah solusi":**
  - AP lama: memakai **data terukur** (dikurangi 6 dB untuk E1).
  - AP baru: memakai model.
  - CCI dihitung ulang dengan rencana kanal baru dan semua radio lain yang terukur.
  - Hasil per titik ada di `banding_titik_L4.csv`.
- **Kenapa angka CCI turun dari 43 ke 2?**
  - Kebanyakan dari 43 kejadian terjadi karena AP pelayan berada di kanal yang ramai (153/157/161).
  - Dengan rencana baru, AP yang melayani titik-titik itu pindah ke kanal yang sepi (60, 64, 40, 36), atau titiknya dilayani AP baru di kanal yang tidak ada pengganggunya.
  - Sisa 2 kejadian adalah radio lain yang tetap terdengar di kanal AP pelayan.
- **Kenapa tidak "tambah daya saja"?** Lihat B7. Sinyal sudah kuat. Menaikkan daya memperbesar sel dan CCI, membuat link asimetris dan klien makin sticky, dan dibatasi regulasi 23 dBm.
- **Kenapa tidak "pakai 80 MHz biar cepat"?** Lihat B6. Kanal non-DFS 80 MHz hanya ada 2 blok, padahal ada 10 AP yang saling dengar. Rata-rata 5 AP per kanal, jadi airtime tiap AP tinggal ±1/5. Noise juga naik 6 dB dan butuh sinyal 6 dB lebih kuat untuk kecepatan yang sama.

---

### Slide 12: Kesimpulan & Referensi

**Di slide**

Kesimpulan:
1. Cakupan sinyal lantai 4 **sudah baik**: 97,4% ≥ −67 dBm, tanpa blank spot
2. **Masalah utamanya co-channel interference**: 43 kejadian, AP sekanal saling tumpang tindih, kanal 149–161 padat, kanal DFS tidak dimanfaatkan
3. Sinyal lantai 5 bocor ke lantai 4 (6 titik nyaris tersaingi); roaming tidak mulus sampai koneksi mati ±3,5 menit
4. Solusi: **atur ulang kanal (1 AP = 1 kanal, 2 di DFS), +2 AP, E1 −6 dB, 802.11k/v/r**. Prediksi: CCI 43 → 2, semua titik ≥ −67 dBm

Referensi (font kecil):
1. Modul *Hands-on: Pemetaan Kualitas Sinyal Wi-Fi 5 GHz Gedung FILKOM*
2. IEEE Std 802.11-2020, *Wireless LAN MAC and PHY Specifications*
3. Permenkominfo No. 2 Tahun 2023 tentang Penggunaan Spektrum Frekuensi Radio Berdasarkan Izin Kelas
4. Coleman & Westcott, *CWNA Study Guide*, Sybex
5. Cisco, *High Density Experience (HDX) Deployment Guide*
6. ITU-R P.1238, *Propagation data for indoor radiocommunication systems*
7. Zoom Support, *Zoom system requirements: bandwidth* (KB0060748)
8. Microsoft Learn, *Native Wifi API*

**Naskah lisan**
> "Kesimpulannya: masalah Wi-Fi lantai 4 bukan sinyal yang lemah, tapi kanal yang terlalu ramai. Solusi terpenting justru yang paling murah, yaitu mengatur ulang kanal dan memperbaiki roaming lewat controller, lalu menambah dua AP di pojok yang lemah. Terima kasih."

---

## Bagian E: Jawaban 16 pertanyaan Ghazy

**1. Perlu analisis bocor dari lantai 3 & 5? Datanya ada?**
- **Perlu, dan sudah jadi slide 7.** Modul §9.5 memang meminta analisis lintas lantai.
- Datanya ada di:
  - `output/gedung_floor_bleed.csv`, `gedung_titik_lantai_lain.csv`, dan `gedung_ap_per_lantai.csv` (dari `gabung_lantai.py`)
  - Versi yang sudah dikoreksi offset laptop: `output/solusi_L4/floor_bleed_L4.csv` + gambar `8_floor_bleed_L4.png`
- **Temuannya:**
  - Lantai 5 bocor cukup kuat ke lantai 4 (6 titik nyaris tersaingi, L4-010 hanya selisih 1,5 dB).
  - Lantai 3 lemah.
  - Redaman lantai 26–30 dB, dengan 1 anomali 9 dB.

**2. Outline terlalu singkat?** Sudah ditulis ulang. Setiap slide sekarang punya naskah lisan, pendalaman, dan bukti, ditambah Bagian B (konsep dasar).

**3. "25–30 klien per radio" dari mana?**
- **Itu kesalahan gw.** Angka itu rule of thumb yang gw tulis tanpa sumber yang bisa dipertanggungjawabkan, jadi **sudah dihapus**.
- Sekarang diganti perhitungan kapasitas di B10 dan slide 3. Setiap angkanya punya sumber jelas:
  - 35 orang/kelas: asumsi kelompok
  - 0,6 dan 1,8 Mbps per user: panduan resmi Zoom
  - 286,5 Mbps: terukur
  - 100 Mbps per AP: asumsi konservatif, disebut terang-terangan sebagai asumsi
- Kalau ditanya: *"Kebutuhan per user kami ambil dari panduan bandwidth resmi Zoom; kapasitas AP adalah asumsi konservatif ±35% dari link rate yang kami ukur; jumlah user adalah estimasi kapasitas kelas."*

**4. Isi 35 orang untuk F4.1–F4.6 dan F4.9–F4.14.**
- Sudah dimasukkan di slide 3 (12 kelas × 35 = 420), dan ditandai sebagai **asumsi kelompok**.
- **F4.7 dan F4.8 belum ada datanya. Tolong isi fungsi ruangnya.**
- Data CSV survei tidak diubah, supaya data ukur tetap murni.

**5. Posisi AP beda dari spreadsheet?**
- **Setuju, spreadsheet itu data lama.** Buktinya ada di `banding_spreadsheet_L4.csv`:
  - Tanggal "Last Seen" semua AP: **26-08-2025**, lebih dari 1 tahun lalu.
  - AP **F4-Ext-4.13 dan F4-Ext-4.14 tidak ditemukan** saat survei. AP yang sekarang terpasang di sana punya MAC berbeda (`c8:a6:08:…`), kemungkinan sudah diganti.
  - **Kanal keenam AP yang cocok semuanya berbeda** dengan kanal terukur. Contoh: F4.3 di spreadsheet ch 149, terukur ch 161.
  - Nama AP juga tidak cocok dengan ruang tempat sinyalnya terkuat. Contoh: "F4.6-R650" paling kuat di F4.4.
- **Gambar kita tidak memakai posisi dari spreadsheet.** Posisi diambil dari pemetaan di bawah AP (M1, E1–E4) dan estimasi dari data (M2–M4). Semuanya tercatat di `data/ap_fisik_L4.csv`.
- **Kalau lo tahu posisi fisik M2/M3/M4** (dari foto atau catatan waktu survei): ganti `x_px` dan `y_px` di file itu (koordinat pixel denah, 20 px = 1 m; lihat `denah/peta_titik_L4_rev.png` untuk acuan), lalu jalankan `python solusi_L4.py` dan `python bukti_L4.py`. Semua gambar akan ikut berubah.

**6. Penjelasan lisan kurang?** Sudah dibuat naskah lengkap per slide (Bagian D) dan konsep dasar dengan analogi (Bagian B).

**7. Bukti CCI & bukti kanal tiap AP?**
- **Bukti CCI:**
  - Gambar `6_bukti_cci_L4.png` (spektrum per titik)
  - `bukti_cci_L4.csv` (43 baris = 43 kejadian)
  - Kolom `cci` di `output/L4_titik.csv`
- **Masalah pemilihan kanal ada 3:** M2 & E3 sekanal; AP ditaruh di kanal paling ramai; kanal DFS kosong tidak dipakai (slide 5).
- **Bukti kanal tiap AP:**
  - `data/map_bssid_L4.csv` dan `data/passive_L4.csv` (kolom `channel` & `width_mhz`)
  - Bisa didemokan dengan `netsh wlan show networks mode=bssid` atau WiFiAnalyzer

**8. Bukti "149–161 paling padat"?**
- Gambar baru `7_radio_per_kanal_L4.png` (grafik batang per kanal, berwarna sesuai asal radio, + tabel 14 radio pengganggu terkuat).
- Daftar lengkap di `radio_L4.csv`.
- Masuk slide 6.

**9. Apa itu DFS?** Lihat B5. Singkatnya: kanal 52–64 dipakai bersama radar, jadi AP wajib mengecek radar dulu dan pindah kanal kalau ada radar. Kanal ini biasanya sepi; di lantai 4, kanal 60/64 kosong.

**10. Slide 8 (dulu 7) menjelaskan apa? Dan soal koneksi yang putus?**
- Itu justru temuan penting, dan **sekarang jadi bagian utama slide 8** dengan gambar timeline `9_timeline_roaming_L4.png`.
- Penjelasan dan kronologinya ada di slide 8 bagian Pendalaman.
- Intinya: setelah pindah AP, laptop tetap tersambung secara radio, tapi internet/DNS mati sampai di-reconnect manual. Itu alasan solusi menyertakan 802.11r dan rekomendasi pengecekan ke admin.

**11. Kriteria desain?** Slide 9, kriteria K1–K6. Kriteria ditetapkan dulu, baru solusi dirancang dan diuji terhadap kriteria itu di slide 11.

**12. Arti "36, 40, 44, 48, 153×2…" dan cara tahu kanal valid?**
- Lihat slide 9 Pendalaman dan B3.
- Ringkasnya: di 5 GHz dengan 20 MHz, kanal yang berbeda **tidak pernah tumpang tindih** (beda dengan 2,4 GHz yang harus 1/6/11).
- Rencana valid kalau:
  - **(1)** semua kanal legal
  - **(2)** tidak ada dua AP yang saling dengar memakai kanal sama
  - **(3)** radio lain di kanal itu sedikit atau lemah
- Bukti cek ada di `validasi_kanal_L4.csv`.

**13. Kenapa 20 MHz membuat CCI tidak naik?**
- Koreksi konsep: CCI bukan "banyak channel bicara", tapi "**banyak perangkat di satu channel yang sama**".
- Dengan 20 MHz kita punya 12 kanal untuk 10 AP, jadi setiap AP bisa punya kanal sendiri.
- Dengan 80 MHz hanya ada 2–3 kanal, jadi 3–5 AP terpaksa berbagi satu kanal dan saling menunggu.
- Lengkapnya di B4 dan B6.

**14. Slide 8 lama (alokasi) tidak dimengerti?** Sudah ditulis ulang jadi slide 9, dengan kriteria, tabel alasan, cara mencari kanal, perbandingan 4 opsi, dan cara validasi.

**15. Asal angka "43 → 7"?**
- Angka **43** = jumlah kolom `cci` di `output/L4_titik.csv` (hasil `analyze.py`), dengan rincian di `bukti_cci_L4.csv`.
- Angka **7** di versi lama **sudah diganti**:
  - Setelah gw cek ulang, cara optimasi lama hanya melihat AP pelayan, jadi rencana kanal lama ternyata masih menaruh 2 AP L4 yang saling dengar di kanal yang sama.
  - Sekarang ukurannya ditambah "tumpang tindih AP sekanal". Hasil rencana baru: **CCI 43 → 2, tumpang tindih 9 → 0**.
  - Cara hitungnya di slide 11 Pendalaman.
- **Setuju, CCI adalah temuan utama kita**, dan presentasi sekarang dibangun di sekitar temuan itu (Bagian A).

**16. Kenapa "tambah daya" dan "80 MHz" bukan solusi?**
- Lihat B6 (lebar kanal) dan B7 (daya). Penjelasannya dari konsep dasar, lengkap dengan analogi dan angka.

---

## Bagian F: Persiapan Tanya Jawab

| Pertanyaan | Jawaban |
|---|---|
| Kenapa tidak ada SNR? | Windows Native WiFi API tidak memberikan *noise floor*. Sudah ditulis di keterbatasan. Sebagai gantinya kami memakai CCI dan uji aktif. |
| Kenapa RSSI dirata-rata dalam mW? | dBm itu logaritmik. Rata-rata langsung di dBm bias ke nilai lemah (B1). |
| Bagaimana tahu AP mana yang melayani? | Dari BSSID dengan sinyal WiFi-UB.x terkuat. Satu radio memancarkan beberapa SSID, dan BSSID-nya digabung per radio oleh `analyze.py`. |
| Kenapa batas CCI −85 dBm? | Aturan modul §4.5. Perangkat 802.11 wajib menunggu kalau mendeteksi sinyal Wi-Fi ≥ −82 dBm (20 MHz); −85 diambil sebagai margin. |
| Kenapa L3 terlihat lebih buruk dari L4? | Laptop L3 membaca 7,6 dB lebih lemah (hasil kalibrasi). Setelah dikoreksi, kondisinya mirip L4. |
| Apakah DFS legal di Indonesia? | Pita 5250–5350 MHz (kanal 52–64) termasuk izin kelas untuk dalam ruangan (Permenkominfo 2/2023). DFS adalah mekanisme menghindari radar yang dijalankan AP. Lantai 3 FILKOM sudah memakai kanal 52/60/64. |
| Kalau ada radar dan AP DFS pindah kanal? | Klien di AP itu putus beberapa detik. Karena itu DFS hanya dipakai 2 AP, dan ada rencana cadangan non-DFS. |
| Kenapa kanal 165 tidak dipakai? | Kanal 165 (5815–5835 MHz) melewati batas atas 5825 MHz di regulasi. |
| Seberapa yakin prediksinya? | Galat model 5,6 dB, tanpa dinding. Jadi itu arah perbaikan, bukan angka pasti. Sinyal AP baru sudah dibatasi supaya tidak optimis. Harus divalidasi dengan survei ulang. |
| Kenapa tidak geser AP saja? | Menggeser tidak menambah kapasitas. Di skenario berat gedung utama 95%, dan menggeser M1 ke F4.8 membuat F4.4 lemah. |
| Kenapa 802.11r? | WiFi-UB.x memakai WPA2/3-Enterprise (login akun). Tanpa 802.11r, setiap pindah AP harus login ulang penuh. Kami menemukan koneksi mati setelah pindah AP. |
| Apakah koneksi putus pasti salah jaringan? | Tidak pasti. Bisa juga driver laptop. Polanya konsisten setelah pindah AP. Kami rekomendasikan admin memeriksa log RADIUS/DHCP dan mengulang uji dengan perangkat lain. |
| Kenapa angka spreadsheet (klien, kanal) tidak dipakai? | Data dari Agustus 2025. 2 AP sudah tidak ada, dan kanal semua AP sudah berbeda. Kami memakai hasil ukur sendiri. |
| Dari mana 35 orang per kelas? | Asumsi kelompok berdasarkan kapasitas kelas 30–40 kursi, bukan hasil hitung saat survei. |
| Kalau anggaran hanya cukup 1 AP? | Prioritaskan Tahap 1 (gratis), lalu **N1 di F4.2**, karena area itu paling lemah dan 007 bermasalah. |

---

## Bagian G: Angka kunci & checklist gambar

**Angka kunci (hafalkan):**
- **Survei:** 65 titik (L4 39 · L3 13 · L5 13), 8 titik uji aktif, 2 lintasan roaming
- **Cakupan L4:** 97,4% ≥ −67 dBm, median −56, terlemah −69 (006), 0 blank spot
- **CCI:**
  - 43 kejadian di 39 titik; terparah hall 000 dan 206 (6 radio)
  - M2 & E3 sekanal (153), tumpang tindih di 9 titik
  - 51 radio terdengar di L4, hanya 8 AP WiFi-UB.x L4; kanal 149–161 berisi 17–20 radio; 60/64 kosong
- **Floor bleed:**
  - 10 titik L4 mendengar AP L3/L5 ≥ −75; 6 titik selisih ≤ 6 dB (010: 1,5 dB)
  - Redaman lantai 26–30 dB (anomali 9 dB)
- **Uji aktif:** 5 dari 8 titik RTT > 50 ms; 3 titik loss > 2% (102: 10%)
- **Roaming:** R2 12× pindah AP; 69% ping gagal selama ±3,5 menit sampai reconnect manual
- **Offset laptop:** L3 −7,6 dB, L5 −5,4 dB
- **Solusi:**
  - +2 AP (N1 F4.2 ch161, N2 F4.8 ch48), 1 AP = 1 kanal (M2 ch64 & E1 ch60 di DFS), E1 −6 dB, 802.11k/v/r
  - CCI 43 → 2, tumpang tindih 9 → 0, terlemah −69 → −61 dBm, beban berat 95% → 63%

**Checklist gambar:**

| Slide | File |
|---|---|
| 1 | `kelompok6/denah/peta_titik_L4_rev.png` |
| 4 | `output/solusi_L4/1_heatmap_AP_L4.png` (+ opsional `2_posisi_area_AP_L4.png`) |
| 5 | `output/solusi_L4/6_bukti_cci_L4.png` + `3_kanal_L4.png` |
| 6 | `output/solusi_L4/7_radio_per_kanal_L4.png` |
| 7 | `output/solusi_L4/8_floor_bleed_L4.png` |
| 8 | `output/solusi_L4/9_timeline_roaming_L4.png` (+ opsional `output/L4_status.png`) |
| 10 | `output/solusi_L4/4_solusi_L4.png` |
| 11 | `output/solusi_L4/5_prediksi_sebelum_sesudah_L4.png` |
| Cadangan (Q&A) | `output/L3_heatmap.png`, `output/L5_heatmap.png`, `output/L4_kanal.png` |

**Yang masih perlu diisi tim:**
1. Fungsi ruang F4.7 dan F4.8 (slide 3).
2. Posisi fisik M2, M3, M4 kalau diketahui → edit `data/ap_fisik_L4.csv`, lalu jalankan ulang skrip.
3. Screenshot `netsh wlan show networks mode=bssid` atau WiFiAnalyzer di bawah satu AP, sebagai bukti kanal (opsional, bagus untuk slide 5).
