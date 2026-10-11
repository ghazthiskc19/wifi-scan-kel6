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
2. **Tapi pengguna tetap bisa lambat atau putus.** Uji aktif menemukan RTT > 50 ms dan packet loss, dan uji roaming menemukan laptop pindah AP 12× termasuk ping-pong dalam 10 detik. (Sempat ada anomali "tersambung tanpa internet", tapi penyebabnya belum bisa disimpulkan, lihat slide 8.)
3. **Penyebab utamanya bukan kekuatan sinyal, tapi *co-channel interference* (CCI)**, yaitu terlalu banyak radio berbagi kanal yang sama. Ditambah dua hal lain: sinyal dari lantai 5 "bocor" ke lantai 4, dan proses roaming yang tidak mulus.
4. **Solusinya bukan menambah daya, tapi mengatur ulang kanal**, menambah 2 AP (F4.2 yang lemah dan F4.5 untuk kapasitas, sehingga setiap ruang kuliah punya AP sendiri), menurunkan daya 1 AP yang terlalu kuat, dan mengaktifkan fitur roaming.
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
- Semua AP di kampus memakai SSID yang sama (`WiFi-UB.x`). Karena itu **satu-satunya cara membedakan AP adalah lewat BSSID**. Contoh: `c0:c7:0a:98:3a:52` = AP yang kita sebut **AP-F4.4**.
- Di dokumen, gambar, dan laporan, **setiap AP dinamai sesuai ruangan tempat AP terpasang: `AP-F4.x`**:

| Nama | Lokasi | Kanal sekarang | Keterangan |
|---|---|---|---|
| AP-F4.1 | dekat pintu F4.1 (estimasi) | 44 | gedung utama |
| AP-F4.3 | di dalam F4.3, di atas pintu | 161 | gedung utama |
| AP-F4.4 | di dalam F4.4 | 36 | gedung utama |
| AP-F4.6 | pojok kanan-atas dekat F4.6 (estimasi) | 153 | gedung utama |
| AP-F4.9 / AP-F4.10 / AP-F4.13 / AP-F4.14 | di dalam ruang Ext tersebut | 48 / 40 / 153 / 157 | gedung Ext |
| **AP-F4.2**, **AP-F4.5** | usulan AP **baru** | – | solusi |

- **Nama ini berdasarkan lokasi fisik, bukan nama di controller kampus.** Nama di controller (spreadsheet) ternyata banyak yang tidak cocok dengan ruangannya. Contoh: AP yang di controller bernama "F4.6-R650" ternyata ada di F4.4 (lihat Bagian E no. 5).

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
   - Contoh nyata: titik 007 di gedung utama justru dilayani **AP-F4.14** (di gedung Ext) dari seberang hall.
5. **Batas legal:** daya maksimum 200 mW / 23 dBm EIRP dalam ruangan (Permenkominfo 2/2023).

Karena itu solusinya justru **menurunkan** daya AP-F4.14 sebanyak 6 dB. Sinyalnya −34 dBm di bawah AP, terlalu kuat, dan bocor ke gedung utama.

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

Kebutuhan kapasitas per AP (skenario berat: 35 user × 1,8 Mbps = **63 Mbps per kelas**, kapasitas efektif ±100 Mbps per AP):

| AP | Ruang kuliah yang dilayani sekarang | Beban sekarang | Setelah solusi |
|---|---|---|---|
| AP-F4.4 | F4.2 + F4.4 | **126%** ❌ | F4.4 saja: 63% ✅ |
| AP-F4.3 | F4.3 + F4.5 | **126%** ❌ | F4.3 saja: 63% ✅ |
| AP-F4.6 | F4.6 | 63% | 63% |
| AP-F4.1 | F4.1 | 63% | 63% |
| AP-F4.2 (baru) | – | – | F4.2: 63% ✅ |
| AP-F4.5 (baru) | – | – | F4.5: 63% ✅ |

Skenario normal (0,6 Mbps/user = 21 Mbps per kelas): 1 AP melayani 2 kelas = 42% (masih aman).

**Gambar:** foto suasana kelas (kalau ada).

**Naskah lisan**
> "Lantai 4 berisi 12 ruang kuliah. Kami asumsikan saat penuh tiap kelas diisi 35 orang, jadi ada sekitar 420 pengguna. Kalau semua menonton video kuliah 720p, kebutuhan per orang sekitar 1,8 Mbps, sesuai panduan resmi Zoom, jadi satu kelas butuh sekitar 63 Mbps. Satu AP kami perkirakan sanggup sekitar 100 Mbps. Masalahnya, di gedung utama ada 6 kelas tapi hanya 4 AP: AP di F4.3 sekaligus melayani F4.5, dan AP di F4.4 sekaligus melayani F4.2. Dua AP itu kelebihan beban, 126%. Ini dasar usulan kami: satu ruang kuliah, satu AP."

**Pendalaman**
- **Hitungan per AP:** 1 kelas = 35 × 1,8 = 63 Mbps. AP yang melayani 2 kelas = 126 Mbps ÷ 100 Mbps = **126%** (kelebihan beban). AP yang melayani 1 kelas = 63%, di bawah target 70%.
- **AP mana melayani kelas mana?** Ditentukan dari AP dengan sinyal terkuat di tengah tiap ruang (data survei titik 008, 009, 010, 013, 014, 015 + model). Contoh: di F4.5 (titik 013) AP terkuat adalah AP-F4.3 (−59 dBm), padahal AP-F4.3 berada di F4.3.
- **Hitungan total gedung utama** (pembanding): 210 user × 1,8 = 378 Mbps; 4 AP = 95%, 6 AP = 63%.
- **Kenapa kapasitas efektif ±100 Mbps padahal link rate 286,5 Mbps?**
  - Link rate adalah kecepatan "mentah" di udara. Sebagian waktu habis untuk antre (CSMA/CA), header, ACK, dan retransmisi.
  - Klien yang jauh juga memakai kecepatan lebih rendah, sehingga memakan airtime lebih lama.
  - Kami ambil ±35% sebagai angka konservatif. Ini **asumsi**, dan bisa diverifikasi dengan uji iperf3.
- **Kapasitas efektif hanya berlaku kalau AP punya kanal sendiri.** Kalau 2 AP berbagi kanal dan saling dengar, kapasitas 100 Mbps itu dibagi berdua. Inilah hubungan masalah kapasitas dengan CCI (slide 5).
- **Ext:** 6 kelas dengan 4 AP, total 378 Mbps ÷ 400 Mbps = 95% pada skenario berat. Ini masuk rekomendasi tahap 3 (kondisional) di slide 9.
- **Data controller (spreadsheet) tidak dipakai sebagai angka utama**, karena data itu dari 26-08-2025 dan sudah tidak sesuai kondisi sekarang (lihat Bagian E no. 5). Hanya disebut sebagai pembanding kalau ditanya: dulu tercatat ±364 klien di 8 AP L4, sejalan dengan estimasi kita.
- Angka 35 orang per kelas adalah **asumsi kelompok**, bukan hasil hitung orang saat survei. Katakan itu terus terang.

---

### Slide 4: Cakupan Sinyal & Posisi AP

**Di slide**
- **97,4%** titik ≥ −67 dBm (baik), **100%** titik ≥ −70 dBm, **0 blank spot**
- Median −56 dBm. Titik terlemah **−69 dBm di L4-006** (pojok kiri-atas, dekat toilet)
- Semua titik punya AP cadangan ≥ −75 dBm (syarat roaming terpenuhi)
- **8 AP 5 GHz:** 4 di gedung utama (AP-F4.1, AP-F4.3, AP-F4.4, AP-F4.6), 4 di Ext (AP-F4.9, AP-F4.10, AP-F4.13, AP-F4.14), semua 20 MHz
- Pojok kiri-atas (F4.2) tidak punya AP; F4.3 dan F4.5 berbagi satu AP (AP-F4.3, di atas pintu F4.3)
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
  - **Fisik / pemetaan langsung:** AP-F4.4 dan keempat AP Ext (AP-F4.9, AP-F4.10, AP-F4.13, AP-F4.14). Kami berdiri tepat di bawah AP dan men-scan. BSSID terkuat = AP itu.
  - **Fisik dari pengamatan lapangan:** AP-F4.3 terpasang **di dalam F4.3, di atas pintu masuk**. Ada 3 bukti yang cocok: (1) pengamatan anggota saat survei; (2) sinyal AP-F4.3 paling kuat di seluruh gedung utama ada di L4-021, tepat di depan pintu F4.3 (−48,8 dBm); (3) nama di controller "F4.3-R650".
  - **Estimasi:** AP-F4.6 dan AP-F4.1. Posisinya dihitung dari rata-rata berbobot 3 titik dengan sinyal terkuat AP tersebut. AP-F4.1 paling kuat di 015/018/201, di sekitar pintu F4.1, jadi kemungkinan besar AP-F4.1 juga terpasang di atas pintu F4.1.
  - Catatan jujur: hasil `--ap F4.3` di `map_bssid_L4.csv` justru menunjukkan AP-F4.1 paling kuat (−45 dBm) dan AP-F4.3 hanya −57 dBm. Kemungkinan scan itu diambil di bawah AP F4.1, bukan F4.3 (pintu kedua ruang sama-sama di sisi bawah).
  - Posisi bisa dikoreksi di `data/ap_fisik_L4.csv`.
- **Gambar area layanan (`2_posisi_area_AP_L4.png`)** menunjukkan titik L4-007 (gedung utama) **dilayani AP-F4.14 di Ext**, dari seberang hall. Ini tanda AP-F4.14 terlalu kuat dan ada celah AP di kiri-atas.
- **Bukti angka:** `output/L4_ringkasan.txt` dan `output/L4_titik.csv` (kolom `rssi1`, `rssi2`).

---

### Slide 5: Temuan Utama: Co-Channel Interference (CCI)

**Di slide**
- CCI = beberapa radio di **kanal yang sama** saling dengar, sehingga harus **bergiliran memakai airtime**. Akibatnya lambat dan loss walaupun sinyal kuat
- Aturan modul: radio sekanal ≥ −85 dBm; CCI > 2 = bermasalah
- **Total 43 kejadian CCI di 39 titik**; 6 titik CCI > 2
- **AP-F4.6 & AP-F4.13 sama-sama di kanal 153**, terdengar bersamaan di 9 titik
- Terparah: **hall (L4-000) dan L4-206: 6 radio sekanal**; L4-001: 5; L4-102: 4
- Pengganggu: AP kampus yang tidak memancarkan WiFi-UB.x, AP lantai 3, hotspot/jaringan lab

**Gambar:**
- Utama: `6_bukti_cci_L4.png` (spektrum di 4 titik terparah). Kalau terlalu ramai, crop panel **L4-000** saja.
- Pendamping kecil: `3_kanal_L4.png` (denah: kanal tiap AP + garis merah AP-F4.6–AP-F4.13 + lingkaran CCI per titik).

**Naskah lisan**
> "Ini temuan utama kami. Di Wi-Fi, perangkat di kanal yang sama harus bergiliran bicara: dengar dulu, kalau ada yang bicara, tunggu. Kalau banyak radio di satu kanal saling mendengar, waktu bicara dibagi-bagi. Akibatnya lambat, walaupun sinyalnya kuat.
> Grafik ini adalah 'spektrum' di 4 titik terparah. Sumbu bawah adalah kanal, sumbu kiri kekuatan sinyal. Bintang adalah AP yang melayani titik itu, pita kuning adalah kanalnya. Semua titik di pita kuning di atas garis putus-putus −85 dBm adalah pengganggu. Contohnya di hall, titik 000: AP pelayannya AP-F4.6 di kanal 153, dan ada 6 radio lain di kanal 153 yang terdengar. Di seluruh lantai 4 kami menemukan 43 kejadian seperti ini. Kami juga menemukan dua AP lantai 4, AP-F4.6 dan AP-F4.13, memakai kanal yang sama, yaitu 153."

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
- **(1)** AP-F4.6 dan AP-F4.13 memakai kanal yang sama (153) dan saling dengar.
- **(2)** AP L4 ditempatkan di kanal 149–161 (AP-F4.6, AP-F4.3, AP-F4.14, AP-F4.13), yang paling ramai jaringan lain.
- **(3)** Kanal DFS 52–64 di lantai 4 hampir kosong (52 dan 56 hanya 1 radio lemah, 60 dan 64 kosong), tapi tidak dimanfaatkan.

**Bukti kanal yang dipakai tiap AP:**
- `data/map_bssid_L4.csv` dan `data/passive_L4.csv` (kolom `channel`, `width_mhz`)
- Bisa didemokan dengan `netsh wlan show networks mode=bssid` atau WiFiAnalyzer (Bagian C)

---

### Slide 6: Kepadatan Kanal & Asal Radio

**Di slide**
- 51 radio 5 GHz terdengar di lantai 4 (≥ −85 dBm). Hanya **8** yang AP WiFi-UB.x lantai 4
- Kanal **149–161 paling padat** (17–20 radio per kanal): kebanyakan jaringan lain dan radio kampus non-WiFi-UB.x
- Kanal **36–48 lebih sepi** (2–5 radio)
- Kanal DFS **52–64 hampir kosong** (60 & 64 nol radio; 52 & 56 hanya 1 radio), belum dimanfaatkan
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
- **R1** (keliling gedung utama): pindah AP 1× (AP-F4.4 → AP-F4.3), ping putus ±4 detik
- **R2** (Ext ↔ gedung utama): pindah AP **12×**, termasuk ping-pong AP-F4.3 → AP-F4.10 → AP-F4.3 dalam 10 detik
- **Anomali, belum bisa disimpulkan:** setelah pindah AP, laptop tetap "tersambung" tapi 38 dari 55 ping gagal (69%) selama ±3,5 menit dan 6 uji aktif gagal, baru pulih setelah **reconnect manual**. Gejala serupa juga muncul saat survei pasif ketika laptop sedang scan berulang, dan hanya terjadi di 1 laptop. Jadi **tidak disajikan sebagai temuan**, melainkan anomali yang perlu diuji ulang (di deck: slide "Roaming: yang terbukti & yang belum").

**Gambar:** `9_timeline_roaming_L4.png` (utama). Opsional: `output/L4_status.png`.

**Naskah lisan**
> "Untuk membuktikan dampaknya, kami melakukan uji koneksi nyata. Tabel ini menunjukkan titik 102 di Ext: sinyalnya sangat kuat, −49 dBm, tapi 10% paket hilang. Ini ciri khas interferensi, bukan sinyal lemah. Lima dari delapan titik punya latensi di atas 50 ms.
> Yang terbukti dari grafik ini adalah perpindahan AP: 12 kali, termasuk ping-pong AP-F4.3–AP-F4.10 dalam 10 detik. Ada juga anomali yang belum bisa kami simpulkan: Garis atas menunjukkan AP mana yang dipakai laptop dari waktu ke waktu, dan grafik bawah adalah hasil ping. Setelah laptop berpindah AP, terutama setelah bolak-balik AP-F4.3–AP-F4.10 pukul 11:21, laptop tetap terlihat tersambung, tapi 69% ping gagal selama sekitar 3,5 menit. Uji aktif di 6 titik juga gagal karena alamat server tidak bisa ditemukan. Koneksi baru normal setelah kami putus dan sambung ulang secara manual. Setelah itu, uji ulang di semua titik berhasil."

**Pendalaman: arti tiap kolom**
- **RTT** (*round-trip time*): waktu bolak-balik paket dari laptop ke server dan kembali. > 50 ms terasa lambat untuk video call (batas modul).
- **Jitter:** seberapa berubah-ubah RTT. Jitter tinggi membuat video call patah-patah.
- **Loss:** persentase paket yang hilang. > 2% = BURUK (modul). Satu titik diuji 20 paket, jadi **loss 5% = 1 paket hilang** (indikatif) dan 10% = 2 paket.
- RTT diukur ke internet (filkom.ub.ac.id lewat Cloudflare, atau 1.1.1.1). Jadi angkanya termasuk jaringan kampus ke internet, bukan hanya Wi-Fi. Perbandingan antar-titik tetap bermakna karena jalurnya sama.

**Apa yang terjadi saat koneksi putus?** (kronologi dari `raw/roaming_L4_R2.csv` + `raw/roaming_ping_L4_R2.txt`):

| Jam | Kejadian |
|---|---|
| 11:19:03 | Laptop pindah ke AP-F4.6 |
| 11:19:47–11:21:10 | Uji aktif di 203, 006, 007 (2×) **gagal**: "Ping request could not find host filkom.ub.ac.id" |
| 11:21:42–11:21:52 | Ping-pong AP-F4.3 → AP-F4.10 → AP-F4.3 |
| 11:22:09–11:25:31 | **38 dari 55 ping gagal** (69%). Laptop tetap tersambung ke AP (BSSID ada di log). Uji aktif 101 & 106 gagal |
| 11:25:31 | **Reconnect manual** (di log terlihat BSSID 00:00:00…, artinya laptop sempat lepas sebentar) |
| 11:25:32 | Tersambung ke AP-F4.14, ping normal lagi |
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
| Jumlah AP | 8 | **10** (+AP-F4.2, +AP-F4.5) | K1 (F4.2 lemah) & K4 (1 kelas = 1 AP) |
| Lebar kanal | 20 MHz | **20 MHz** | K3: lebar = kanal sedikit = CCI |
| Kanal | 36, 40, 44, 48, 153×2, 157, 161 | **1 kanal = 1 AP**; 4 AP lama tetap; 3 AP pindah ke DFS | K3 |
| Daya | default | **AP-F4.14 −6 dB** | sinyal −34 dBm, bocor ke 007 |
| Roaming | – | **802.11k/v/r + min-RSSI ±−72 dBm** | temuan putus koneksi |

Rencana kanal:

| AP | AP-F4.4 | AP-F4.6 | AP-F4.3 | AP-F4.1 | AP-F4.14 | AP-F4.10 | AP-F4.13 | AP-F4.9 | AP-F4.2 | AP-F4.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| Lama | 36 | 153 | 161 | 44 | 157 | 40 | 153 | 48 | – | – |
| **Baru** | **157** | **60** | 161 | 44 | **52** | 40 | **56** | 48 | **153** | **36** |

**Gambar:** tabel saja. Boleh tambah tabel kecil "4 opsi kanal" (lihat Pendalaman).

**Naskah lisan**
> "Sebelum merancang, kami tetapkan enam kriteria: cakupan, roaming, interferensi, kapasitas, regulasi, dan biaya. Dari kriteria itu, kami mengusulkan tiga hal.
> Pertama, tambah dua AP: satu di F4.2 yang sinyalnya paling lemah, satu di F4.5 supaya F4.3 dan F4.5 tidak lagi berbagi satu AP. Hasilnya setiap ruang kuliah punya AP sendiri, dan beban per AP turun dari 126 ke 63%.
> Kedua, semua AP tetap di lebar 20 MHz. Kanal ditata ulang supaya **setiap AP lantai 4 punya kanal sendiri**. Dengan 10 AP, 8 kanal non-DFS tidak cukup, jadi 3 AP kami tempatkan di kanal DFS 52, 56, dan 60, yang di lantai 4 hampir kosong. Empat AP lama tidak perlu diubah kanalnya.
> Ketiga, turunkan daya AP Ext F4.14 sebanyak 6 dB, dan aktifkan fitur roaming 802.11k/v/r."

**Pendalaman: arti tabel "Kanal"**
- **Kolom "Sekarang"** berisi 8 AP di 7 kanal berbeda. Kanal 153 dipakai 2 AP (AP-F4.6 dan AP-F4.13), itulah yang dimaksud "153×2".
- **Kolom "Usulan" berarti:**
  - Pilih dari **12 kanal 20 MHz yang legal** di Indonesia: 36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161.
  - Setiap AP mendapat kanal yang **berbeda** dari 9 AP lainnya.
  - **4 AP lama tetap** (AP-F4.3 161, AP-F4.1 44, AP-F4.10 40, AP-F4.9 48); **4 AP lama pindah** (AP-F4.4 → 157, AP-F4.6 → 60, AP-F4.14 → 52, AP-F4.13 → 56); 2 AP baru (AP-F4.2 153, AP-F4.5 36).
  - Tiga AP (AP-F4.6, AP-F4.14, AP-F4.13) memakai kanal DFS 60/52/56.

**Cara rencana kanal dicari** (`solusi_L4.py`):
1. Data yang dipakai: sinyal setiap AP di 39 titik (terukur), sinyal 2 AP baru (diprediksi model, slide 11), dan semua radio lain yang terukur (lantai 3/5, jaringan lain, beserta kanalnya).
2. **Skor sebuah rencana** = CCI (cara modul) + jumlah titik tumpang tindih AP sekanal + 3 × jumlah AP di DFS + 1 × jumlah AP lama yang kanalnya diganti. Penalti DFS supaya DFS hanya dipakai kalau benar-benar membantu, dan penalti perubahan supaya admin tidak perlu mengubah AP yang sudah baik.
3. Komputer mencoba mengganti kanal satu AP sekali waktu. Kalau skornya turun, perubahan disimpan. Proses diulang sampai tidak bisa turun lagi, dari 30 titik awal acak, lalu diambil yang terbaik (*local search*).

**Perbandingan 4 opsi** (`opsi_kanal_L4.csv`):

| Opsi | CCI (metode modul) | Titik tumpang tindih AP sekanal | AP di DFS |
|---|---|---|---|
| Sekarang (8 AP) | 43 | 9 | 0 |
| +2 AP, kanal lama dibiarkan | 39 | **36** ⬆️ (makin parah) | 0 |
| +2 AP, kanal baru, hanya non-DFS | 12 | 32 | 0 |
| **+2 AP, kanal baru + DFS (usulan)** | **2** | **0** | 3 |

- **Menambah AP tanpa mengatur kanal justru memperparah** (tumpang tindih 9 → 36).
- Tanpa DFS, tumpang tindih tetap tinggi (32), karena 10 AP > 8 kanal non-DFS, jadi pasti ada 2 pasang AP berbagi kanal. Padahal semua AP L4 saling dengar.

**Cara mengecek rencana kanal valid** (`validasi_kanal_L4.csv`), dengan 3 syarat:
1. **Legal:** semua kanal ada di daftar 12 kanal (B3). ✅
2. **Tidak ada AP L4 sekanal:** setiap kanal di rencana usulan dipakai **tepat 1 AP L4**, jadi tumpang tindih = 0. ✅
3. **Radio lain di kanal itu lemah atau tidak ada:** di kanal 60 tidak ada radio lain sama sekali; di 52 dan 56 hanya 1 radio lemah (−82 dBm). Di 149–161 masih ada radio lain, tapi pada titik-titik yang dilayani AP tersebut sisa CCI hanya 2 (di 202 dan 203).

Lalu cek ulang di lapangan setelah diterapkan: survei ulang, bandingkan dengan `banding_titik_L4.csv`.

**Bedanya dengan 2,4 GHz:** di 2,4 GHz pilihan aman hanya 1/6/11 (3 kanal), karena kanal yang bersebelahan tumpang tindih. Di 5 GHz dengan 20 MHz, **semua kanal berbeda pasti tidak tumpang tindih**. Tugas kita hanya memastikan **AP yang saling dengar tidak memakai kanal yang sama**.

**Rekomendasi bertahap:**

| Tahap | Isi | Biaya |
|---|---|---|
| **Tahap 1** | Ubah kanal, turunkan daya AP-F4.14, aktifkan 802.11k/v/r + min-RSSI | 0, cukup lewat controller |
| **Tahap 2** | Pasang AP-F4.2 dan AP-F4.5 | 2 AP + kabel/PoE |
| **Tahap 3** (kondisional) | Kalau utilisasi kanal di controller Ext > 50% saat jam sibuk, tambah 1 AP di Ext F4.11/F4.12 | hitungan kapasitas Ext juga 95% pada skenario berat |

**Kalau dosen menolak DFS:** pakai rencana non-DFS (CCI 12, tumpang tindih 32). Ini tetap lebih baik dari sekarang soal CCI, tapi ada 2 pasang AP yang berbagi kanal.

---

### Slide 10: Penempatan AP & Rencana Kanal di Denah

**Di slide**
- ★ **AP-F4.2 (kiri-atas), kanal 153:** menutup 005/006/007/008. Sekarang titik terlemah −69 dBm, dan 007 dilayani AP Ext
- ★ **AP-F4.5, kanal 36:** F4.3 dan F4.5 sekarang sama-sama dilayani AP-F4.3 (beban 126% skenario berat). Dengan AP-F4.5, setiap ruang kuliah F4.1–F4.6 punya AP sendiri
- Label tiap AP: kanal lama → baru (4 AP lama tetap)
- Panah oranye: sinyal AP-F4.14 bocor sampai 007, sehingga daya AP-F4.14 diturunkan 6 dB
- Pemasangan di plafon, di tengah ruang, menjauhi kolom beton dan shaft lift

**Gambar:** `4_solusi_L4.png` (penuh). Kotak teks kanan boleh di-crop karena sudah ada di slide 9.

**Naskah lisan**
> "Ini posisi usulan. Bintang adalah AP baru. AP-F4.2 dipasang di pojok kiri-atas yang sekarang paling lemah dan terhalang lift dan toilet. AP-F4.5 dipasang karena sekarang F4.5 menumpang AP milik F4.3. Dengan dua AP ini, setiap ruang kuliah punya AP sendiri. AP lama tidak perlu dipindah, dan hanya empat yang perlu diganti kanalnya lewat controller. Panah oranye menunjukkan sinyal AP Ext yang terlalu kuat sampai menyeberang ke gedung utama, sehingga dayanya kami turunkan."

**Pendalaman**
- **Kenapa di dalam ruang, bukan di koridor?** Modul §9.4: AP di koridor yang melayani ruang kelas akan teredam dinding dan pintu (bata 8–15 dB, pintu 4–6 dB). AP di dalam ruang langsung melayani penggunanya.
- **Kenapa pojok kiri-atas lemah?** Ada inti lift, toilet, dan tangga. Material beton/bata dan logam lift meredam lebih dari 20 dB. Selain itu tidak ada AP di sisi kiri-atas.
- **Kenapa menambah AP, bukan memindah AP yang ada?** Kami membandingkan 7 opsi dengan model yang sama (tabel di bawah). Memindah AP ke F4.2 memang memperbaiki pojok kiri-atas, tapi selalu ada AP lain yang jadi melayani 2 kelas (beban 126%) atau malah 3 kelas (189%). Masalah kapasitas hanya hilang kalau jumlah AP = jumlah ruang kuliah.

| Opsi | AP gedung utama | 006 / 007 (model) | AP terberat (skenario berat) |
|---|---|---|---|
| Sekarang | 4 | −66 / −65 | 126% (AP-F4.4: F4.2+F4.4, AP-F4.3: F4.3+F4.5) |
| Pindah AP-F4.6 ke F4.2 | 4 | −54 / −54 | 126% (AP-F4.4: F4.4+F4.6, AP-F4.3: F4.3+F4.5) |
| Pindah AP-F4.4 ke F4.2 | 4 | −57 / −57 | 126% (AP-F4.6: F4.4+F4.6, AP-F4.3) |
| Pindah AP-F4.1 ke F4.2 | 4 | −57 / −57 | **189%** (AP-F4.3: F4.1+F4.3+F4.5) |
| Tambah AP-F4.2 F4.2 saja | 5 | −56 / −56 | 126% (AP-F4.3: F4.3+F4.5) |
| Tambah AP-F4.2 F4.2 + AP-F4.5 F4.8 | 6 | −56 / −56 | 126% (AP-F4.5 tidak melayani ruang kuliah) |
| **Tambah AP-F4.2 F4.2 + AP-F4.5 F4.5 (usulan)** | 6 | −56 / −56 | **63%** ✅ |

Catatan: angka 006/007 di tabel ini dari model (tanpa dinding) supaya semua opsi dibandingkan dengan cara yang sama; hasil ukur aslinya −69/−64 dBm.

- **Kenapa bukan F4.8?** Sinyal di F4.8 sudah BAIK (003: −59 dBm, 203: −63 dBm). AP di F4.8 hanya memperbaiki sinyal yang sebenarnya tidak bermasalah, dan tidak mengurangi beban ruang kuliah. Jitter/loss di 203 lebih mungkin karena interferensi dan beban, yang sudah ditangani rencana kanal. Kalau setelah implementasi 203 masih bermasalah, baru dipertimbangkan.
- **Kenapa tidak terlalu padat?** 6 AP untuk 6 ruang kuliah (±35 orang per ruang) masih wajar untuk ruang kelas. Kepadatan AP hanya jadi masalah kalau AP-AP itu berbagi kanal, dan itu sudah dicegah oleh rencana kanal (tumpang tindih = 0).
- Posisi AP-F4.2/AP-F4.5 adalah usulan berdasarkan denah. Saat pemasangan, cek ketersediaan kabel/PoE dan jalur plafon ke admin.

---

### Slide 11: Pembahasan: Analisis, Justifikasi & Keterbatasan

**Di slide**

| Indikator | Sekarang | Setelah solusi (prediksi) | Kriteria |
|---|---|---|---|
| Titik ≥ −67 dBm | 97,4% | **100%** | K1 ✅ |
| RSSI terlemah | −69,2 dBm (006) | **−63,0 dBm** (203) | K1 ✅ |
| CCI total (metode modul) | 43 | **2** | K3 ✅ |
| Tumpang tindih AP sekanal | 9 titik | **0** | K3 ✅ |
| CCI hall (000) | 6 | **0** | K3 ✅ |
| Beban AP terberat (skenario berat) | 126% | **63%** | K4 ✅ |

Contoh per titik: 006: −69 → −56 · 007: −64 → −56 · 008: −61 → −49 dBm

**Feasible karena:**
- Tahap 1 gratis (konfigurasi controller)
- Hanya +2 AP dari model yang sama
- Kanal & daya sesuai regulasi (izin kelas, maks. 23 dBm)
- DFS sudah dipakai di lantai 3

**Keterbatasan:**
- Tidak ada SNR (Windows)
- Prediksi = model tanpa dinding
- Posisi AP-F4.6 dan AP-F4.1 hasil estimasi
- 1 slot waktu survei
- 20 paket per uji aktif

**Gambar:** `5_prediksi_sebelum_sesudah_L4.png`.

**Naskah lisan**
> "Bagaimana kami tahu solusinya berhasil? Kami membuat model penurunan sinyal dari data survei kami sendiri, lalu menghitung ulang kondisi setelah solusi. Hasilnya: semua titik di atas −67 dBm, CCI turun dari 43 menjadi 2, tidak ada lagi dua AP lantai 4 yang berbagi kanal, dan setiap ruang kuliah punya AP sendiri. Solusinya juga realistis: tahap pertama hanya konfigurasi tanpa biaya, dan tahap kedua cuma dua AP. Tapi ini prediksi model, jadi perlu divalidasi dengan survei ulang setelah diterapkan."

**Pendalaman: model prediksi**
- **Rumus log-distance** (modul §4.1): `RSSI(d) = P − 10·n·log₁₀(d)`.
  - `P` = sinyal pada jarak 1 m (dihitung per AP).
  - `n` = eksponen redaman, dicari dari data kita: **n = 2,52**. Ruang bebas n = 2, gedung penuh dinding 3,5–4. Jadi n = 2,52 cocok untuk gedung dengan koridor cincin yang cukup terbuka.
  - **Galat model (RMSE) = 5,5 dB**, artinya rata-rata meleset ±5,5 dB dibanding hasil ukur.
  - Model **tidak menghitung dinding**, jadi bisa terlalu optimis. Karena itu sinyal AP baru **dibatasi maksimal −48,8 dBm**, yaitu sinyal terbaik yang pernah terukur dari AP gedung utama.
- **Cara menghitung "setelah solusi":**
  - AP lama: memakai **data terukur** (dikurangi 6 dB untuk AP-F4.14).
  - AP baru: memakai model.
  - CCI dihitung ulang dengan rencana kanal baru dan semua radio lain yang terukur.
  - Hasil per titik ada di `banding_titik_L4.csv`.
- **Kenapa angka CCI turun dari 43 ke 2?**
  - Kebanyakan dari 43 kejadian terjadi karena AP pelayan berada di kanal yang ramai (153/157/161).
  - Dengan rencana baru, AP yang melayani titik-titik itu pindah ke kanal yang sepi (60, 64, 40, 36), atau titiknya dilayani AP baru di kanal yang tidak ada pengganggunya.
  - Sisa 2 kejadian (di 202 dan 203) adalah radio lain yang tetap terdengar di kanal AP pelayan.
- **Kenapa tidak "tambah daya saja"?** Lihat B7. Sinyal sudah kuat. Menaikkan daya memperbesar sel dan CCI, membuat link asimetris dan klien makin sticky, dan dibatasi regulasi 23 dBm.
- **Kenapa tidak "pakai 80 MHz biar cepat"?** Lihat B6. Kanal non-DFS 80 MHz hanya ada 2 blok, padahal ada 10 AP yang saling dengar. Rata-rata 5 AP per kanal, jadi airtime tiap AP tinggal ±1/5. Noise juga naik 6 dB dan butuh sinyal 6 dB lebih kuat untuk kecepatan yang sama.

---

### Slide 12: Kesimpulan & Referensi

**Di slide**

Kesimpulan:
1. Cakupan sinyal lantai 4 **sudah baik**: 97,4% ≥ −67 dBm, tanpa blank spot
2. **Masalah utamanya co-channel interference**: 43 kejadian, AP sekanal saling tumpang tindih, kanal 149–161 padat, kanal DFS tidak dimanfaatkan
3. Sinyal lantai 5 bocor ke lantai 4 (6 titik nyaris tersaingi); roaming tidak terarah: 12× pindah AP termasuk ping-pong dalam 10 detik (anomali "tersambung tanpa internet" dicatat sebagai keterbatasan)
4. Solusi: **atur ulang kanal (1 AP = 1 kanal, 3 di DFS), +2 AP (F4.2, F4.5) sehingga 1 ruang kuliah = 1 AP, AP-F4.14 −6 dB, 802.11k/v/r**. Prediksi: CCI 43 → 2, semua titik ≥ −67 dBm, beban AP terberat 126% → 63%

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
> "Kesimpulannya: masalah Wi-Fi lantai 4 bukan sinyal yang lemah, tapi kanal yang terlalu ramai. Solusi terpenting justru yang paling murah, yaitu mengatur ulang kanal dan memperbaiki roaming lewat controller, lalu menambah dua AP supaya setiap ruang kuliah punya AP sendiri. Terima kasih."

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
- **Gambar kita tidak memakai posisi dari spreadsheet.** Posisi diambil dari pemetaan di bawah AP (AP-F4.4 + 4 AP Ext), pengamatan lapangan (AP-F4.3 di atas pintu), dan estimasi dari data (AP-F4.6, AP-F4.1). Semuanya tercatat di `data/ap_fisik_L4.csv`.
- **Kalau lo tahu posisi fisik AP-F4.6/AP-F4.1** (dari foto atau catatan waktu survei): ganti `x_px` dan `y_px` di file itu (koordinat pixel denah, 20 px = 1 m; lihat `denah/peta_titik_L4_rev.png` untuk acuan), lalu jalankan `python solusi_L4.py` dan `python bukti_L4.py`. Semua gambar akan ikut berubah.

**6. Penjelasan lisan kurang?** Sudah dibuat naskah lengkap per slide (Bagian D) dan konsep dasar dengan analogi (Bagian B).

**7. Bukti CCI & bukti kanal tiap AP?**
- **Bukti CCI:**
  - Gambar `6_bukti_cci_L4.png` (spektrum per titik)
  - `bukti_cci_L4.csv` (43 baris = 43 kejadian)
  - Kolom `cci` di `output/L4_titik.csv`
- **Masalah pemilihan kanal ada 3:** AP-F4.6 & AP-F4.13 sekanal; AP ditaruh di kanal paling ramai; kanal DFS kosong tidak dipakai (slide 5).
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

**17. Kenapa tambah 2 AP, bukan pindah? Kenapa F4.8, bukan F4.3/F4.5?**
- **Lo benar, dan usulannya sudah diganti: AP-F4.5 sekarang di F4.5, bukan F4.8.**
- **Kenapa tetap butuh 2 AP?**
  - AP-F4.2 untuk **cakupan**: titik terlemah 006 dan 007 yang dilayani AP Ext.
  - AP-F4.5 untuk **kapasitas**: sekarang AP-F4.3 (di atas pintu) melayani F4.3 sekaligus F4.5. Pada skenario berat, bebannya 126%.
- **Kenapa tidak cukup memindah AP?** Sudah dicoba 3 variasi pemindahan (AP-F4.4, AP-F4.6, atau AP-F4.1 ke F4.2). Semuanya tetap menyisakan 1 AP yang melayani 2–3 kelas (126–189%). Tabelnya ada di slide 10 Pendalaman.
- **Kenapa F4.8 dicoret?** Sinyalnya sudah BAIK (−59/−63 dBm), dan F4.8 bukan salah satu dari 6 ruang kuliah utama. AP di sana tidak mengurangi beban.
- **Terlalu padat?** Tidak, selama tiap AP punya kanal sendiri (tumpang tindih = 0). Kepadatan AP baru jadi masalah kalau kanalnya bentrok.
- **Posisi AP-F4.3** sudah dipindah ke dalam F4.3 di atas pintu, sesuai info lo. Datanya juga mendukung: titik L4-021 tepat di depan pintu F4.3 adalah titik terkuat AP-F4.3.

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
| Kalau ada radar dan AP DFS pindah kanal? | Klien di AP itu putus beberapa detik. Karena itu DFS hanya dipakai 3 dari 10 AP, dan ada rencana cadangan non-DFS. |
| Kenapa kanal 165 tidak dipakai? | Kanal 165 (5815–5835 MHz) melewati batas atas 5825 MHz di regulasi. |
| Seberapa yakin prediksinya? | Galat model 5,5 dB, tanpa dinding. Jadi itu arah perbaikan, bukan angka pasti. Sinyal AP baru sudah dibatasi supaya tidak optimis. Harus divalidasi dengan survei ulang. |
| Kenapa tidak geser AP saja? | Sudah kami bandingkan 3 variasi pemindahan. Semuanya menyisakan 1 AP yang melayani 2–3 kelas (beban 126–189%). Hanya dengan 1 AP per ruang kuliah bebannya turun ke 63%. |
| Kenapa AP baru di F4.5, bukan F4.8? | F4.8 sinyalnya sudah baik (−59/−63 dBm) dan bukan ruang kuliah utama. F4.5 sekarang menumpang AP F4.3, jadi AP baru di F4.5 langsung mengurangi beban. |
| Kenapa 802.11r? | WiFi-UB.x memakai WPA2/3-Enterprise (login akun). Tanpa 802.11r, setiap pindah AP harus login ulang penuh. Kami menemukan koneksi mati setelah pindah AP. |
| Apakah koneksi putus pasti salah jaringan? | Tidak pasti. Bisa juga driver laptop. Polanya konsisten setelah pindah AP. Kami rekomendasikan admin memeriksa log RADIUS/DHCP dan mengulang uji dengan perangkat lain. |
| Kenapa angka spreadsheet (klien, kanal) tidak dipakai? | Data dari Agustus 2025. 2 AP sudah tidak ada, dan kanal semua AP sudah berbeda. Kami memakai hasil ukur sendiri. |
| Dari mana 35 orang per kelas? | Asumsi kelompok berdasarkan kapasitas kelas 30–40 kursi, bukan hasil hitung saat survei. |
| Kalau anggaran hanya cukup 1 AP? | Prioritaskan Tahap 1 (gratis), lalu **AP-F4.2**, karena area itu paling lemah dan 007 bermasalah. |

---

## Bagian G: Angka kunci & checklist gambar

**Angka kunci (hafalkan):**
- **Survei:** 65 titik (L4 39 · L3 13 · L5 13), 8 titik uji aktif, 2 lintasan roaming
- **Cakupan L4:** 97,4% ≥ −67 dBm, median −56, terlemah −69 (006), 0 blank spot
- **CCI:**
  - 43 kejadian di 39 titik; terparah hall 000 dan 206 (6 radio)
  - AP-F4.6 & AP-F4.13 sekanal (153), tumpang tindih di 9 titik
  - 51 radio terdengar di L4, hanya 8 AP WiFi-UB.x L4; kanal 149–161 berisi 17–20 radio; 60/64 kosong
- **Floor bleed:**
  - 10 titik L4 mendengar AP L3/L5 ≥ −75; 6 titik selisih ≤ 6 dB (010: 1,5 dB)
  - Redaman lantai 26–30 dB (anomali 9 dB)
- **Uji aktif:** 5 dari 8 titik RTT > 50 ms; 3 titik loss > 2% (102: 10%)
- **Roaming:** R2 12× pindah AP; 69% ping gagal selama ±3,5 menit sampai reconnect manual
- **Offset laptop:** L3 −7,6 dB, L5 −5,4 dB
- **Solusi:**
  - +2 AP (AP-F4.2 F4.2 ch153, AP-F4.5 F4.5 ch36), 1 ruang kuliah = 1 AP
  - Kanal: 1 AP = 1 kanal; 4 AP lama tetap (AP-F4.3 161, AP-F4.1 44, AP-F4.10 40, AP-F4.9 48); AP-F4.4 → 157; AP-F4.6 → 60, AP-F4.14 → 52, AP-F4.13 → 56 (DFS)
  - AP-F4.14 −6 dB, 802.11k/v/r
  - CCI 43 → 2, tumpang tindih 9 → 0, terlemah −69 → −63 dBm, beban AP terberat 126% → 63%

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
2. Posisi fisik AP-F4.6 dan AP-F4.1 kalau diketahui (AP-F4.1 kemungkinan di atas pintu F4.1) → edit `data/ap_fisik_L4.csv`, lalu jalankan ulang skrip.
3. Screenshot `netsh wlan show networks mode=bssid` atau WiFiAnalyzer di bawah satu AP, sebagai bukti kanal (opsional, bagus untuk slide 5).

---

## Bagian H: Simulasi pembanding (deck teman, `Document/Lantai4-wifi-analysis (3).pptx`)

Dipakai di slide 39–43 `slide/SLIDE_L4.md` sebagai **pendukung**, bukan pengganti data ukur. Versi (3) adalah versi akhir yang memakai **posisi dan rencana kanal usulan kita (10 dari 10 AP sama)**.

| Item | Nilai |
|---|---|
| AP | 10 AP 5 GHz (di simulasi: 9 R650, 1 R750), Tx 20 dBm per AP |
| Kanal | AP-F4.14 52, AP-F4.10 40, AP-F4.13 56, AP-F4.9 48, AP-F4.4 157, AP-F4.1 44, AP-F4.6 60, AP-F4.3 161, AP-F4.2 153, AP-F4.5 36 (= rencana usulan) |
| Model propagasi | Free-space path loss + redaman dinding (128 dinding), plafon 4 m, klien referensi, downlink |
| Cakupan | 87,7% ≥ −70 dBm, dihitung dari kotak denah 53 × 34 m (1.807 m²) termasuk area luar gedung |

**Cara membaca 4 peta:**
- **SNR:** semua ruang hijau (kategori teratas). Kuning hanya di tangga dan shaft lift.
- **Interferensi kanal:** seluruh lantai hijau (0–10%). Dengan rencana kanal usulan, AP lantai 4 tidak saling mengganggu. Simulasi tidak tahu ada jaringan lain; sisa CCI dari data ukur = 2.
- **Kapasitas user:** seluruh lantai hijau (≥ 150% kebutuhan). Cocok dengan hitungan kita: beban 63% per AP sama dengan kapasitas ±1,6× kebutuhan.
- **Cakupan cadangan:** kuat di tengah gedung utama, lebih lemah di Ext dan tepi gedung. Data ukur tetap memenuhi K2.
- **Data rate** tidak ditampilkan, karena klien referensi simulasi tidak sama dengan laptop kita.

**Kenapa cakupan turun dari 90,2% (versi 2) ke 87,7% (versi 3)?**
- Versi 2 memakai model ITU-R P.1238. Versi 3 memakai free-space path loss + redaman dinding.
- Rencana kanal **tidak mengubah kuat sinyal**. Kanal hanya menentukan interferensi.
- Jadi selisihnya berasal dari model propagasi yang berganti, dan terjadi di area luar ruang. Semua ruang kuliah tetap hijau atau hijau muda.

**Versi 2 (rencana kanal teman sebelumnya)**, diuji dengan data ukur kita (`opsi_kanal_L4.csv`, baris "+2 AP, kanal dari simulasi"): CCI 4 (di 000, 109, 203), tumpang tindih 0, 2 AP di DFS, 6 AP lama diubah. Usulan kita: CCI 2, tumpang tindih 0, 3 AP di DFS, 4 AP lama diubah. Karena itu versi akhir simulasi memakai rencana kanal kita.

---

## Bagian I: Data Wi-Fi FILKOM (website filkom.ub.ac.id/wifi)

**Sumber:** `https://filkom.ub.ac.id/wifi/`, halaman publik milik kampus. Halaman ini memakai beberapa API publik. Data dibagi dua jenis:

| Endpoint | Isi | Sifat | Dipakai? |
|---|---|---|---|
| `api/public/recommend` | Per AP: rating, jumlah perangkat, airtime 5 GHz (%). Per lantai: rata-rata perangkat per jam (7 hari) | **live**, diperbarui tiap ±90 detik | ✅ |
| `api/public/wifimodel/clients` | Per perangkat tersambung: AP, RSSI, SNR, rate | **live** | ✅ (pelengkap) |
| `api/public/wifimodel` | Peta 3D: posisi, model, EIRP, kanal AP | **statis, belum diperbarui** | ❌ hanya diarsipkan |

**Prinsip:** data survei kita (kanal, posisi AP, RSSI, CCI) **tidak diganti** dengan data website. Data website hanya dipakai untuk hal yang tidak bisa kita ukur sendiri: airtime dari sisi AP dan jumlah perangkat nyata.

**Cara ambil:** `python kelompok6/ambil_web_filkom.py` (sekali) atau `--poll 5 --jam 8` (berulang, jalankan saat jam kuliah). Hasilnya:
- Snapshot JSON di `kelompok6/data/web_filkom/<tanggal_jam>/`
- Deret waktu di `poll_ap.csv` dan `poll_klien.csv`
- Field `id` perangkat tidak disimpan (privasi)

Gambar dibuat oleh `python kelompok6/web_L4.py`, yang menghasilkan:
- `10_web_pengguna_L4.png`
- `11_web_airtime_L4.png`
- `web_ringkasan_L4.txt`

**Yang didapat (memperkuat temuan, tidak mengubah angka survei):**
1. **CCI di kanal 153 terlihat dari sisi jaringan.**
   - Minggu malam 11 Okt 2026 (11 snapshot, 21:09–21:34), tanpa klien: dua AP yang menurut survei kita di kanal 153 (F4.6 dan F4-Ext-4.13) airtime rata-rata 40% dan 38%, tidak pernah di bawah 20%. Enam AP lain rata-rata ≤ 10% (AP-F4.10 sempat naik ke 42% di 2 snapshot).
   - Daftar AP kampus Agustus 2025 (jam kuliah): AP kanal 153 juga airtime tertinggi. F4-Ext-4.13 85% dengan hanya 18 klien.
   - Airtime tinggi tanpa klien = kanal dipakai radio lain.
2. **Asumsi ±420 pengguna masuk akal.**
   - Rata-rata 7 hari (termasuk akhir pekan): puncak 304 perangkat pukul 10:00, rata-rata jam 08–16 sebanyak 227.
   - Agustus 2025 15:40: 364 klien.
3. **SNR klien** (perangkat yang tersambung, se-gedung, Minggu malam): median 47 dB. Ini hanya pelengkap, bukan SNR per titik ukur.

**Yang tidak berubah:** semua angka survei, rencana kanal, daya AP-F4.14 (−6 dB), posisi AP, dan hasil prediksi.

**Catatan peta 3D website:** posisi, model, dan EIRP AP di sana belum diperbarui, jadi tidak dipakai. Kalau ditanya: "Peta 3D di website belum diperbarui, jadi posisi dan kanal AP kami ambil dari survei langsung."

**Keterbatasan:**
- Snapshot diambil Minggu malam, di luar jam kuliah. Jalankan polling di hari kerja untuk bukti jam kuliah.
- Profil per jam adalah rata-rata 7 hari termasuk akhir pekan.
- Lantai 3 berstatus "off" di website (tidak ada data).
- Daftar AP kampus 2025 memakai nama AP lama, jadi dibandingkan per kanal, bukan per nama.

**Jawaban kalau ditanya "dari mana data Wi-Fi FILKOM?":** "Dari website publik Wi-Fi FILKOM milik kampus. Kami hanya mengambil endpoint publik yang dipakai halaman itu sendiri, tanpa login, dan tidak menyimpan identitas perangkat."
