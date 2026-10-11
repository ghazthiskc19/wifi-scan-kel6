---
marp: true
theme: default
size: 16:9
paginate: true
lang: id
title: Wi-Fi 5 GHz Lantai 4 FILKOM - Kelompok 6
author: Kelompok 6
header: ""
footer: "Kelompok 6 · Survei Wi-Fi 5 GHz · Lantai 4 FILKOM UB"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;500;600;700&display=swap');
  @font-face { font-family: 'Bebas Neue'; src: local('Bebas Neue'), url('fonts/BebasNeue-Regular.ttf'); }
  @font-face { font-family: 'Poppins'; font-weight: 300; src: local('Poppins Light'), url('fonts/Poppins-Light.ttf'); }
  @font-face { font-family: 'Poppins'; font-weight: 400; src: local('Poppins'), url('fonts/Poppins-Regular.ttf'); }
  @font-face { font-family: 'Poppins'; font-weight: 500; src: local('Poppins Medium'), url('fonts/Poppins-Medium.ttf'); }
  @font-face { font-family: 'Poppins'; font-weight: 600; src: local('Poppins SemiBold'), url('fonts/Poppins-SemiBold.ttf'); }
  @font-face { font-family: 'Poppins'; font-weight: 700; src: local('Poppins Bold'), url('fonts/Poppins-Bold.ttf'); }

  :root { --ink: #121212; --paper: #f7f6f2; --red: #e30613; --grey: #4d4d47; --line: #cfcec7; }

  /* ---------- dasar ---------- */
  section {
    background: var(--paper); color: var(--ink);
    font-family: 'Poppins', sans-serif; font-size: 20px; line-height: 1.5; font-weight: 400;
    padding: 86px 72px 66px;
    display: flex; flex-direction: column; justify-content: flex-start;
  }
  h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif; font-weight: 400; color: var(--ink);
    border: 0; padding: 0; letter-spacing: 0.01em; line-height: 0.95;
  }
  h2 { font-size: 60px; margin: 0 0 24px; }
  h3 { font-size: 30px; margin: 0 0 6px; }
  h1 em, h2 em, h3 em { font-style: normal; color: var(--red); }
  p { margin: 0 0 10px; }
  ul, ol { margin: 0; padding-left: 1.1em; }
  li { margin: 0 0 6px; }
  li::marker { color: var(--red); font-weight: 600; }
  strong { font-weight: 600; }
  code { font-family: 'Poppins', sans-serif; font-size: 0.88em; background: #e9e8e2; color: var(--ink); padding: 1px 6px; border-radius: 0; }

  /* ---------- header, footer, nomor halaman ---------- */
  header {
    position: absolute; top: 32px; left: 72px; right: 72px; padding: 0 0 10px;
    font-size: 12px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: var(--ink);
    border-bottom: 1.5px solid var(--ink);
  }
  header::before { content: ''; display: inline-block; width: 10px; height: 10px; background: var(--red); margin-right: 12px; }
  footer { position: absolute; bottom: 26px; left: 72px; font-size: 11px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--grey); }
  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
    position: absolute; right: 72px; bottom: 20px; padding: 0;
    font-family: 'Bebas Neue', sans-serif; font-size: 24px; color: var(--ink);
  }

  /* ---------- tabel ---------- */
  table { display: table; width: 100%; border-collapse: collapse; font-size: 17px; line-height: 1.35; margin: 0; }
  table tr { background: transparent !important; border: 0; }
  table th, table td { border: 0; border-bottom: 1px solid var(--line); padding: 7px 14px 7px 0; text-align: left; background: transparent; vertical-align: top; }
  table th { font-size: 11.5px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; border-bottom: 2px solid var(--ink); }

  /* ---------- utilitas ---------- */
  .m { color: var(--red); font-weight: 600; }
  .abu { color: var(--grey); }
  .ket { font-size: 13.5px; color: var(--grey); line-height: 1.4; margin-top: 10px; }
  .kecil { font-size: 16px; }
  .kecil table { font-size: 15px; }
  .mini table { font-size: 14px; }
  .mini th, .mini td { padding: 5px 12px 5px 0; }
  .mt { margin-top: 22px; }
  .label { font-size: 12px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--grey); margin-bottom: 8px; }
  .lead { font-size: 19px; max-width: 1050px; margin-bottom: 18px; }
  .dua { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: start; }
  .dua.g64 { grid-template-columns: 1.55fr 1fr; gap: 40px; }
  .dua.g46 { grid-template-columns: 1fr 1.45fr; gap: 40px; }
  .dua.g73 { grid-template-columns: 2.3fr 1fr; gap: 40px; }
  .dua.tengah { align-items: center; }
  .dua img, .tiga img { width: 100%; display: block; }
  .tiga { display: grid; grid-template-columns: repeat(3, 1fr); gap: 36px; }
  .kotak { border-top: 2px solid var(--ink); padding-top: 14px; }
  .kotak.merah { border-top-color: var(--red); }
  .no { font-family: 'Bebas Neue', sans-serif; font-size: 46px; line-height: 1; color: var(--red); }
  .raksasa { font-family: 'Bebas Neue', sans-serif; font-size: 230px; line-height: 0.8; color: var(--red); margin: 0; }
  .besar { font-family: 'Bebas Neue', sans-serif; font-size: 44px; line-height: 1; }

  /* deretan angka besar */
  .stat { display: grid; grid-template-columns: repeat(4, 1fr); gap: 28px; border-top: 2px solid var(--ink); padding-top: 16px; margin-bottom: 26px; }
  .stat.tiga-kolom { grid-template-columns: repeat(3, 1fr); }
  .stat.satu-kolom { grid-template-columns: 1fr; gap: 18px; margin-bottom: 0; }
  .stat b { display: block; font-family: 'Bebas Neue', sans-serif; font-weight: 400; font-size: 84px; line-height: 0.9; }
  .stat.sedang b { font-size: 60px; }
  .stat b.m { color: var(--red); }
  .stat span { display: block; font-size: 14px; color: var(--grey); line-height: 1.35; margin-top: 6px; }
  .stat b span { display: inline; font-size: inherit; line-height: inherit; margin: 0; color: var(--red); }

  /* langkah bernomor */
  .langkah { display: grid; grid-template-columns: 56px 1fr; gap: 6px 10px; align-items: start; }
  .langkah .no { font-size: 40px; }
  .langkah p { margin: 4px 0 12px; }

  /* ---------- slide judul ---------- */
  section.judul { justify-content: center; align-items: center; text-align: center; padding: 60px 100px; }
  section.judul h1 { font-size: 150px; line-height: 0.86; margin: 22px 0 28px; }
  section.judul .atas { font-size: 14px; font-weight: 600; letter-spacing: 0.32em; text-transform: uppercase; margin: 0; }
  section.judul .garis { width: 120px; height: 8px; background: var(--red); margin: 0 auto 26px; }
  section.judul .sub { font-size: 25px; font-weight: 300; max-width: 900px; margin: 0 auto; line-height: 1.4; }
  section.judul .kampus { position: absolute; bottom: 40px; left: 0; right: 0; font-size: 12px; letter-spacing: 0.24em; text-transform: uppercase; color: var(--grey); }

  /* ---------- slide tim ---------- */
  section.tim .grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 28px; }
  section.tim .grid4 img { width: 100%; aspect-ratio: 3 / 4; object-fit: cover; object-position: center 25%; display: block; background: #d9d9d4; }
  section.tim .grid4 h3 { font-size: 27px; line-height: 1; margin: 14px 0 6px; min-height: 54px; }
  section.tim .grid4 p { font-size: 14px; color: var(--grey); margin: 0; line-height: 1.45; }
  section.tim .grid4 p b { color: var(--ink); font-weight: 600; letter-spacing: 0.04em; }

  /* ---------- daftar isi ---------- */
  section.isi .daftar { display: grid; grid-template-columns: repeat(5, 1fr); gap: 22px; border-top: 2px solid var(--ink); padding-top: 20px; margin-top: 30px; }
  section.isi .daftar b { display: block; font-family: 'Bebas Neue', sans-serif; font-weight: 400; font-size: 120px; line-height: 0.85; color: var(--red); }
  section.isi .daftar i { display: block; font-style: normal; font-family: 'Bebas Neue', sans-serif; font-size: 34px; line-height: 1; margin: 14px 0 8px; }
  section.isi .daftar span { display: block; font-size: 14px; color: var(--grey); line-height: 1.4; }
  section.isi .daftar small { display: block; font-size: 12px; font-weight: 600; letter-spacing: 0.16em; margin-top: 10px; }

  /* ---------- pembatas bab ---------- */
  section.bab { background: var(--red); color: #fff; justify-content: center; align-items: center; text-align: center; }
  section.bab .nomor { font-family: 'Bebas Neue', sans-serif; font-size: 110px; line-height: 0.85; color: rgba(255, 255, 255, 0.6); margin: 0; }
  section.bab h1 { color: #fff; font-size: 150px; line-height: 0.85; margin: 8px 0 26px; }
  section.bab .isi-bab { font-size: 21px; font-weight: 300; max-width: 860px; margin: 0 auto; }
  section.bab::after, section.bab footer { color: #fff; }

  /* ---------- slide gambar penuh ---------- */
  section.gambar h2 { font-size: 46px; margin-bottom: 14px; }
  section.gambar p:has(img) { flex: 1; min-height: 0; display: flex; align-items: center; justify-content: center; margin: 0; }
  section.gambar p img { max-width: 100%; max-height: 452px; object-fit: contain; }
  section.gambar.penuh p img { max-height: 502px; }
  section.gambar .ket { margin-top: 8px; }

  /* ---------- dua gambar berdampingan ---------- */
  section.duagambar .dua { gap: 28px; }
  section.duagambar h3 { font-size: 30px; margin: 0 0 8px; }
  section.duagambar .ket { font-size: 14px; color: var(--ink); }

  /* ---------- penutup ---------- */
  section.penutup { background: var(--red); color: #fff; justify-content: center; }
  section.penutup h1 { color: #fff; font-size: 210px; line-height: 0.85; margin: 0 0 24px; }
  section.penutup p { font-size: 24px; font-weight: 300; }
  section.penutup::after, section.penutup footer { color: #fff; }
---

<!-- _class: judul -->
<!-- _paginate: false -->
<!-- _footer: "" -->

<p class="atas">Jaringan Nirkabel &nbsp;·&nbsp; Kelompok 6</p>

# Wi-Fi 5 GHz<br>Lantai 4 *FILKOM*

<div class="garis"></div>

<p class="sub">Pemetaan kualitas sinyal, interferensi kanal, dan usulan penempatan access point</p>

<p class="kampus">Fakultas Ilmu Komputer &nbsp;·&nbsp; Universitas Brawijaya</p>

<!--
Pembuka. Sebutkan judul dan kelompok, lalu langsung kalimat kunci yang akan diulang di akhir, "masalah Wi-Fi lantai 4 bukan sinyal yang lemah, tapi kanal yang terlalu ramai".
-->

---

<!-- _class: tim -->

## Kenalan *dulu*

<div class="grid4">
<div>

![Muhammad Ghazy Humaidi](foto/Ghazy_anggota1.png)

### Muhammad Ghazy Humaidi
<p><b>245150200111071</b><br>Cakupan, CCI, kanal, pembahasan</p>

</div>
<div>

![Alif Kusuma Fauzan](foto/anggota2.jpg)

### Alif Kusuma Fauzan
<p><b>245150201111051</b><br>Kapasitas, uji aktif &amp; roaming</p>

</div>
<div>

![Auliya Rahman Arianto](foto/anggota3.jpg)

### Auliya Rahman Arianto
<p><b>24515020711093</b><br>Pembuka, latar belakang, kesimpulan</p>

</div>
<div>

![Alkhwarizmi Widya Bagaskara](foto/anggota4.jpg)

### Alkhwarizmi Widya Bagaskara
<p><b>245150200111068</b><br>Kebocoran antar-lantai, desain solusi</p>

</div>
</div>

<!--
Perkenalan singkat tiap anggota dan bagian yang dibawakan. Foto anggota 2 sampai 4 diganti dengan menimpa slide/foto/anggota2.jpg, anggota3.jpg, anggota4.jpg (nama file harus sama), foto otomatis dipotong rasio 3x4.
-->

---

<!-- _class: isi -->

## Daftar *isi*

<div class="daftar">
<div><b>01</b><i>Latar Belakang</i><span>Konteks, tujuan, eksperimen, dan cara pengambilan data</span><small>Slide 5–7</small></div>
<div><b>02</b><i>Deskripsi Masalah</i><span>User aktif, data titik, cakupan, CCI &amp; airtime, kanal, kebocoran antar-lantai, uji aktif &amp; roaming</span><small>Slide 9–28</small></div>
<div><b>03</b><i>Desain Solusi</i><span>Kriteria, alokasi AP, kanal, daya, dan penempatan</span><small>Slide 30–35</small></div>
<div><b>04</b><i>Pembahasan</i><span>Prediksi, simulasi pembanding, justifikasi</span><small>Slide 37–44</small></div>
<div><b>05</b><i>Kesimpulan</i><span>Kesimpulan, keterbatasan, dan referensi</span><small>Slide 46–47</small></div>
</div>

<!--
Alur presentasi ada lima bagian. Bagian 02 paling panjang karena di situ semua temuan data kami.
-->

---

<!-- _class: bab -->
<!-- header: "01 — Latar Belakang" -->
<!-- _header: "" -->

<p class="nomor">01</p>

# Latar Belakang

<p class="isi-bab">Konteks, tujuan, eksperimen, dan cara kami mengambil data</p>

<!--
Masuk ke bagian pertama, kenapa survei ini dilakukan dan bagaimana caranya.
-->

---

## Satu nama jaringan, *masalah tak terlihat*

<div class="dua g64">
<div>

- Lantai 4 berisi **12 ruang kuliah**, sekitar **420 pengguna** saat jam penuh
- Semua AP memancarkan SSID yang sama (`WiFi-UB.x`), jadi pengguna hanya tahu "tersambung" atau "lambat", tanpa tahu penyebabnya
- 5 GHz punya kanal lebih banyak dan lebih cepat, tapi jangkauannya lebih pendek. Akibatnya **penempatan AP dan pembagian kanal jadi kritis**
- AP terpasang: **Ruckus R650** (Wi-Fi 6), dan R750 di Ext F4.10 (sesuai nama AP di controller)

</div>
<div class="kotak merah">

<p class="label">Tujuan</p>
<div class="langkah">
<span class="no">01</span><p>Memetakan kualitas sinyal 5 GHz lantai 4</p>
<span class="no">02</span><p>Menemukan area bermasalah dan <strong>akar masalahnya</strong></p>
<span class="no">03</span><p>Mengusulkan jumlah AP, kanal, daya, dan penempatan berbasis data</p>
</div>

</div>
</div>

<!--
Wi-Fi kampus memakai satu nama jaringan untuk semua AP. Dari sisi pengguna, yang terlihat hanya tersambung atau lambat, tanpa tahu penyebabnya. Kami ingin menjawab tiga hal, yaitu di mana area bermasalah, apa akar masalahnya, dan bagaimana memperbaikinya dengan bukti data, bukan tebakan.

Pendalaman. 5 GHz teredam sekitar 6,5 dB lebih besar dari 2,4 GHz pada jarak yang sama (FSPL, modul 4.1) dan lebih teredam dinding. Tapi 5 GHz punya 12 kanal 20 MHz yang legal di Indonesia, 2,4 GHz praktis hanya 3. Karena itu pembagian kanal 5 GHz bisa dan harus direncanakan.
-->

---

## Apa yang kami uji &amp; *kenapa*

<div class="mini">

| Eksperimen | Yang dilakukan | Yang diukur | Kenapa penting |
|---|---|---|---|
| **Survei pasif L4**<br>39 titik | Berdiri di tiap titik, laptop scan semua Wi-Fi 3× | RSSI, BSSID, kanal, lebar kanal setiap radio | Peta cakupan, posisi &amp; kanal AP, dan CCI, **tanpa akses ke controller** |
| **Survei pasif L3 &amp; L5**<br>13 + 13 titik | Titik tepat di atas/bawah titik L4 bernomor sama | Sinyal AP lantai lain | SSID sama di semua lantai: laptop bisa tersambung ke AP lantai lain, dan sinyal bocor **menambah CCI** |
| **Kalibrasi**<br>3 laptop | Ketiga laptop scan bersamaan di hall L4 | Selisih bacaan antar-laptop | 3 lantai diukur 3 laptop berbeda; tanpa koreksi, datanya **tidak bisa dibandingkan** |
| **Uji aktif**<br>8 titik | Tersambung ke `WiFi-UB.x`, kirim 20 paket ping/TCP | RTT, jitter, packet loss, link rate | Scan hanya melihat kuat sinyal; uji aktif mengukur **pengalaman nyata pengguna** |
| **Uji roaming**<br>2 lintasan | Berjalan sambil tersambung, catat AP per detik + ping | Kapan &amp; ke mana laptop pindah AP, gangguan ping | Mahasiswa berpindah ruang sambil online; satu SSID berarti **perpindahan AP harus mulus** |
| **Data Wi-Fi FILKOM**<br>filkom.ub.ac.id/wifi | Ambil data API publik `filkom.ub.ac.id/wifi` (skrip, tiap 2 menit) | Airtime &amp; jumlah perangkat per AP (live); perangkat per jam (7 hari); SNR klien | Data dari **sisi jaringan** untuk **memvalidasi** hasil survei dari sisi laptop |

</div>

<!--
Kami melakukan lima kegiatan, masing-masing menjawab pertanyaan berbeda.

Survei pasif lantai 4 adalah data utama. Laptop hanya mendengarkan semua sinyal Wi-Fi di sekitar, tanpa tersambung, sehingga kami tahu kekuatan sinyal, AP mana yang terdengar, dan kanal yang dipakai. Dari sini lahir heatmap dan perhitungan CCI.

Lantai 3 dan 5 kami ukur karena SSID di semua lantai sama. Laptop di lantai 4 bisa saja tersambung ke AP lantai 5, dan sinyal dari lantai lain ikut berebut kanal.

Kalibrasi diperlukan karena tiap lantai diukur laptop berbeda. Kalau satu laptop membaca 5 dB lebih lemah, perbandingan antar-lantai jadi salah.

Uji aktif menjawab pertanyaan, kalau sinyalnya kuat, apakah internetnya juga lancar? Scan pasif hanya membaca kekuatan beacon, tidak tahu apakah paket data sampai. Uji aktif benar-benar mengirim paket dan mengukur waktu bolak-balik (RTT), variasinya (jitter), dan paket yang hilang (loss), persis yang dirasakan pengguna saat video call.

Uji roaming menjawab, apakah perpindahan AP saat berjalan mulus? Di kampus, mahasiswa berpindah ruang sambil tetap online, dan karena semua AP satu SSID, laptop yang harus memilih kapan pindah.

Terakhir, kami mengambil data publik dari website Wi-Fi FILKOM, yang datanya berasal langsung dari sistem pengelola Wi-Fi kampus. Survei kami melihat jaringan dari sisi laptop, data Wi-Fi FILKOM melihat dari sisi AP. Kalau dua sisi ini cocok, temuan kami lebih kuat.
-->

---

## Cara kami *mengambil data*

<div class="dua g46 tengah">
<div class="kecil">

<div class="langkah">
<span class="no">01</span><p><strong>Tentukan titik di denah</strong><br><span class="abu">Grid tengah ruang &amp; koridor + titik terjauh dari AP (pojok, tangga)</span></p>
<span class="no">02</span><p><strong>Scan di tiap titik</strong><br><span class="abu">Skrip Python membaca semua BSSID 3× (Windows Native WiFi API), disimpan ke CSV</span></p>
<span class="no">03</span><p><strong>Olah per titik</strong><br><span class="abu">RSSI dirata-rata dalam mW; AP pelayan = BSSID WiFi-UB.x terkuat; hitung CCI</span></p>
<span class="no">04</span><p><strong>Analisis</strong><br><span class="abu">Heatmap, kanal, CCI, antar-lantai, prediksi, dibandingkan dengan simulasi</span></p>
</div>

<p class="ket">Alat: 3 laptop Windows 11 (Realtek RTL8852AE), dikalibrasi bersama: offset L3 −7,6 dB, L5 −5,4 dB.</p>

</div>
<div>

![Peta titik ukur lantai 4](img/peta_titik.png)

<p class="ket">Rencana titik ukur lantai 4. Titik 207 dan 208 (tangga darurat) tidak bisa dimasuki, jadi tidak dipakai: 39 titik.</p>

</div>
</div>

<!--
Caranya, kami menentukan titik di denah dulu, berupa grid di tengah ruang dan koridor ditambah titik-titik terjauh dari AP seperti pojok dan tangga, untuk mencari area terlemah. Di tiap titik, laptop menjalankan skrip yang membaca semua sinyal Wi-Fi tiga kali dan menyimpannya ke CSV. Lalu datanya diolah per titik.

Pendalaman. RSSI dirata-rata dalam miliwatt, bukan dBm, karena dBm logaritmik. Rata-rata −40 dan −80 kalau langsung di dBm hasilnya −60, padahal secara daya −43. Windows tidak memberikan noise floor, jadi SNR tidak bisa dihitung.
-->

---

<!-- _class: bab -->
<!-- header: "02 — Deskripsi Masalah" -->
<!-- _header: "" -->

<p class="nomor">02</p>

# Deskripsi Masalah

<p class="isi-bab">Pengguna &amp; ruang, data titik ukur, cakupan, interferensi kanal, kebocoran antar-lantai, uji aktif &amp; roaming</p>

<!--
Bagian kedua, apa yang kami temukan dari data.
-->

---

## 6 kelas, *4 AP*: dua AP kelebihan beban

<div class="dua">
<div>

<p class="label">Fungsi ruang &amp; user aktif</p>

| Area | Fungsi | User saat penuh |
|---|---|---|
| F4.1–F4.6 | Ruang kuliah | 6 × 35 = **210** |
| F4.9–F4.14 (Ext) | Ruang kuliah | 6 × 35 = **210** |
| F4.7, F4.8 | *[isi fungsi ruang]* | *[isi]* |
| Hall, koridor | Menunggu, lalu-lalang | ±10–20 |

<p class="ket">Aplikasi: LMS, slide, browsing, video/kuliah daring. 35 orang per kelas = asumsi kelompok (kapasitas 30–40 kursi), dicek dengan data Wi-Fi FILKOM di slide berikutnya.</p>

</div>
<div>

<p class="label">Beban per AP · skenario berat</p>

| AP | Melayani | Beban |
|---|---|---|
| AP-F4.4 | F4.2 + F4.4 | <span class="m">126%</span> |
| AP-F4.3 | F4.3 + F4.5 | <span class="m">126%</span> |
| AP-F4.1 | F4.1 | 63% |
| AP-F4.6 | F4.6 | 63% |

<p class="ket">1 kelas = 35 × 1,8 Mbps (Zoom 720p) = 63 Mbps. Kapasitas efektif ±100 Mbps per AP (±35% dari link rate terukur 286,5 Mbps). Target ≤ 70%.</p>

</div>
</div>

<!--
Lantai 4 berisi 12 ruang kuliah. Kami asumsikan saat penuh tiap kelas diisi 35 orang, jadi ada sekitar 420 pengguna. Kalau semua menonton video kuliah 720p, kebutuhan per orang sekitar 1,8 Mbps sesuai panduan resmi Zoom, jadi satu kelas butuh sekitar 63 Mbps. Satu AP kami perkirakan sanggup sekitar 100 Mbps. Masalahnya, di gedung utama ada 6 kelas tapi hanya 4 AP. AP di F4.3 sekaligus melayani F4.5, dan AP di F4.4 sekaligus melayani F4.2. Dua AP itu kelebihan beban, 126 persen. Ini dasar usulan kami, satu ruang kuliah satu AP.

Pendalaman. Skenario normal 0,6 Mbps per user, 1 AP untuk 2 kelas = 42 persen, masih aman. Kapasitas efektif 100 Mbps adalah asumsi konservatif dan bisa diverifikasi dengan iperf3. Kapasitas itu hanya berlaku kalau AP punya kanal sendiri, kalau dua AP sekanal saling dengar, kapasitasnya dibagi dua, inilah hubungannya dengan CCI. Ext juga 6 kelas dengan 4 AP, 95 persen di skenario berat, masuk rekomendasi tahap 3.
-->

---

<!-- _class: gambar -->

## Data Wi-Fi FILKOM: *perangkat per jam*

![Perangkat per jam di lantai 4 menurut data Wi-Fi FILKOM](img/web_pengguna.png)

<p class="ket">Rata-rata perangkat 5 GHz tersambung ke 8 AP lantai 4 per jam, 7 hari terakhir (website Wi-Fi FILKOM, diambil 11 Okt 2026). Karena Sabtu–Minggu ikut dirata-rata, angka hari kerja lebih tinggi. Belah ketupat = data daftar AP kampus 26 Agu 2025.</p>

<!--
Asumsi 35 orang per kelas kami cek dengan data Wi-Fi FILKOM. Rata-rata 7 hari terakhir, lantai 4 mencapai puncak 304 perangkat pukul 10 pagi, dan sekitar 230 perangkat sepanjang jam 8 sampai 16. Angka ini sudah termasuk Sabtu dan Minggu yang hampir kosong, jadi di hari kerja angkanya lebih tinggi, kira-kira 304 × 7/5 ≈ 425 kalau akhir pekan nol. Data daftar AP kampus Agustus 2025 juga mencatat 364 klien pada jam kuliah. Jadi asumsi 420 pengguna saat penuh masuk akal, bukan angka karangan.

Catatan. Satu orang bisa membawa lebih dari satu perangkat, dan perangkat yang hanya tersambung 2,4 GHz tidak terhitung di sini.
-->

---

<!-- _class: gambar penuh -->

## Data mentah: *39 titik ukur*

![Data 39 titik ukur lantai 4](img/titik_data.png)

<!--
Ini data mentah kami. RSSI tiap titik adalah rata-rata 3 scan, warnanya status menurut aturan modul §4.5 (RSSI, AP cadangan, CCI, latensi, loss). Setiap titik adalah tempat kami berdiri dan men-scan. Angka atas adalah nomor titik, angka bawah adalah RSSI AP terkuat di titik itu. Warnanya status menurut aturan modul, hijau baik, kuning perhatian, merah buruk. Lingkaran hitam adalah titik-titik yang juga kami uji aktif. Dari 39 titik, 29 baik, 7 perhatian, 3 buruk. Semua heatmap dan perhitungan berikutnya berasal dari titik-titik ini.

Data lengkap per titik ada di kelompok6/output/L4_titik.csv, data mentah scan di kelompok6/data/passive_L4.csv.
-->

---

<!-- _class: gambar -->

## Heatmap RSSI *lantai 4*

![Heatmap RSSI terukur lantai 4](img/heatmap.png)

<p class="ket">Warna = RSSI AP terkuat, diinterpolasi antar-titik ukur (hijau = kuat). Garis hijau = kontur −67 dBm. Segitiga = 8 AP 5 GHz beserta kanalnya. Area putih = tidak ada titik ukur, bukan blank spot.</p>

<!--
Dari titik-titik tadi kami buat heatmap. Hijau artinya kuat. Garis hijau adalah batas −67 dBm, batas aman untuk video call. Hampir seluruh lantai berada di atas batas itu. Segitiga adalah posisi 8 AP 5 GHz beserta kanalnya.

Pendalaman. Warna diinterpolasi antar titik ukur, maksimal 6 m dari titik terdekat.
-->

---

## Sinyal *bukan* masalahnya

<div class="stat">
<div><b class="m">97,4%</b><span>titik ≥ −67 dBm (baik)<br>100% titik ≥ −70 dBm</span></div>
<div><b>−56</b><span>dBm, RSSI median</span></div>
<div><b>−69</b><span>dBm, titik terlemah (L4-006, pojok kiri-atas dekat toilet)</span></div>
<div><b>0</b><span>blank spot (&lt; −80 dBm)</span></div>
</div>

<div class="dua">
<div>

- Semua titik punya **AP cadangan ≥ −75 dBm**, jadi syarat roaming terpenuhi
- **8 AP 5 GHz, semua 20 MHz**: 4 di gedung utama, 4 di Ext

</div>
<div>

- Pojok kiri-atas (F4.2) **tidak punya AP**
- F4.3 dan F4.5 **berbagi satu AP** (AP-F4.3, di atas pintu F4.3)

</div>
</div>

<p class="besar mt">Kalau sinyal bagus, <span class="m">kenapa masih lambat?</span></p>

<!--
Hampir seluruh lantai di atas −67 dBm dan tidak ada blank spot. Area paling lemah ada di pojok kiri-atas dekat toilet, −69 dBm, karena tidak ada AP di sana. Tapi secara umum sinyalnya bagus. Pertanyaannya, kalau sinyal bagus, kenapa masih lambat?

Bukti angka ada di output/L4_ringkasan.txt dan output/L4_titik.csv kolom rssi1 dan rssi2.
-->

---

## Posisi AP &amp; *area layanan*

<div class="dua g64 tengah">
<div>

![Posisi AP dan area layanan](img/area_ap.png)

</div>
<div class="kecil">

<p class="label">Asal posisi AP</p>

- **Fisik, berdiri di bawah AP:** AP-F4.4, AP-F4.9, AP-F4.10, AP-F4.13, AP-F4.14
- **Pengamatan lapangan:** AP-F4.3 di dalam F4.3, di atas pintu
- **Estimasi** (3 titik terkuat): AP-F4.6, AP-F4.1

<p class="label mt">Temuan</p>

- Titik **L4-007** di gedung utama **dilayani AP-F4.14 dari Ext**, menyeberang hall. Artinya AP Ext terlalu kuat dan ada celah AP di kiri-atas

</div>
</div>

<!--
Gambar ini menunjukkan tiap titik dilayani AP mana. Warna area sama dengan warna AP pelayannya, garis menghubungkan titik ke AP-nya. Posisi lima AP kami dapat langsung dengan berdiri di bawahnya, AP-F4.3 dari pengamatan lapangan, dan dua AP sisanya kami estimasi dari tiga titik dengan sinyal terkuat. Yang menarik, titik 007 di gedung utama justru dilayani AP Ext F4.14 dari seberang hall.

Pendalaman. Bukti AP-F4.3 di atas pintu F4.3 ada tiga, yaitu pengamatan anggota, titik L4-021 tepat di depan pintu F4.3 adalah titik terkuat AP itu (−48,8 dBm), dan nama di controller F4.3-R650. Nama AP di dokumen kami berdasarkan lokasi fisik. Peta 3D di website Wi-Fi FILKOM belum diperbarui, jadi posisi AP tetap dari survei kami sendiri.
-->

---

## 10 titik bermasalah, *6 karena CCI*

<div class="dua g73">
<div class="mini">

| Titik | Lokasi | RSSI | Gejala | Akar masalah |
|---|---|---|---|---|
| 000 | Hall | −61 | CCI 6, RTT 118 ms | <span class="m">CCI</span> |
| 001 | Sudut koridor kanan-atas | −51 | CCI 5 | <span class="m">CCI</span> |
| 101 | Ext F4.14 | −34 | CCI 3, RTT 55 ms | <span class="m">CCI</span> |
| 102 | Ext F4.12 | −42 | CCI 4, loss 10% | <span class="m">CCI</span> |
| 107 | Ext F4.13 | −48 | CCI 4 | <span class="m">CCI</span> |
| 206 | Ext F4.11 sisi bawah | −58 | CCI 6 | <span class="m">CCI</span> |
| 006 | Koridor kiri-atas (toilet) | −69 | RSSI marginal | tidak ada AP di kiri-atas |
| 007 | Koridor kiri, depan lift | −64 | loss 5%, RTT 72 ms | dilayani AP Ext dari jauh |
| 203 | F4.8 pojok | −63 | loss 5%, RTT 108 ms | jauh dari AP |
| 017 | Sudut koridor kiri-bawah | −58 | RTT 132 ms | belum jelas (sinyal baik, CCI 0) |

</div>
<div>

<div class="stat satu-kolom">
<div><b class="m">6 / 10</b><span>titik bermasalah karena co-channel interference, padahal sinyalnya kuat (−34 s.d. −61 dBm)</span></div>
<div><b>1 / 10</b><span>titik bermasalah karena sinyal lemah (006)</span></div>
</div>

<p class="ket">Status: 29 baik · 7 perhatian · 3 buruk. Sumber: output/L4_titik.csv (kolom status &amp; penyebab).</p>

</div>
</div>

<!--
Dari 39 titik ada 10 yang bermasalah. Kalau kita lihat penyebabnya, enam di antaranya karena co-channel interference, padahal sinyalnya kuat, bahkan ada yang −34 dBm. Hanya satu titik yang bermasalah karena sinyal lemah, yaitu 006 di pojok kiri-atas. Dua titik lagi jauh dari AP atau dilayani AP yang jauh, dan satu titik, 017, latensinya tinggi tapi sinyal dan kanalnya baik, jadi penyebabnya belum bisa kami pastikan. Jadi akar masalah utamanya adalah CCI. Apa itu CCI? Slide berikutnya.

Pendalaman. Status dihitung otomatis oleh analyze.py dengan aturan modul §4.5. PERHATIAN kalau RSSI −70 sampai −67, CCI > 2, atau latensi > 50 ms. BURUK kalau RSSI < −70 atau packet loss > 2%.
-->

---

## Temuan utama: *co-channel interference*

<div class="dua">
<div>

<p class="label">Cara kerja Wi-Fi (CSMA/CA)</p>
<div class="langkah">
<span class="no">01</span><p>Sebelum mengirim, setiap perangkat <strong>mendengarkan kanalnya dulu</strong></p>
<span class="no">02</span><p>Ada perangkat lain mengirim di kanal yang sama di atas ±−82 dBm? <strong>Wajib menunggu</strong></p>
<span class="no">03</span><p>Semua radio sekanal yang saling dengar <strong>bergiliran memakai airtime</strong>, walaupun tersambung ke AP berbeda</p>
</div>

</div>
<div class="kotak merah">

<p class="besar">Sinyal kuat ≠ koneksi cepat</p>

Akibat CCI: latensi, jitter, dan packet loss naik **walaupun RSSI tinggi**. Contoh: titik 102 sinyal −42 dBm tapi loss 10%.

<p class="label mt">Cara mengukur (modul §4.5)</p>

CCI titik = jumlah radio lain, SSID apa pun, **di kanal AP pelayan** yang terdengar ≥ −85 dBm. **CCI &gt; 2 = bermasalah.**

</div>
</div>

<!--
Ini temuan utama kami. Di Wi-Fi, perangkat di kanal yang sama harus bergiliran bicara, dengar dulu, kalau ada yang bicara tunggu. Kalau banyak radio di satu kanal saling mendengar, waktu bicara dibagi-bagi. Akibatnya lambat walaupun sinyalnya kuat.

Analogi. Satu ruang kelas, satu spidol. Dua dosen di ruang yang sama berbagi satu spidol harus bergantian menulis, walaupun suara keduanya keras. Kalau tiap dosen punya ruang sendiri, yaitu kanal berbeda, keduanya bisa mengajar bersamaan.

Kenapa batas −85 dBm? Standar 802.11 mewajibkan menunggu kalau mendengar sinyal Wi-Fi sekitar −82 dBm untuk 20 MHz, −85 diambil sebagai margin. Catatan, RSSI titik 102 di survei pasif −42 dBm, saat uji aktif −49 dBm.
-->

---

<!-- _class: gambar penuh -->

## Bukti: spektrum di *4 titik terparah*

![Bukti CCI di 4 titik terparah](img/bukti_cci.png)

<!--
Grafik ini adalah spektrum di 4 titik terparah. Sumbu bawah adalah kanal, sumbu kiri kekuatan sinyal. Bintang adalah AP yang melayani titik itu, pita kuning adalah kanalnya. Semua titik di pita kuning di atas garis putus-putus −85 dBm adalah pengganggu. Garis horizontal adalah radio 40 atau 80 MHz yang menduduki beberapa kanal sekaligus. Contohnya di hall, titik 000, AP pelayannya AP-F4.6 di kanal 153, dan ada 6 radio lain di kanal 153 yang terdengar.
-->

---

## 43 kejadian CCI di *39 titik*

<div class="dua g46">
<div>

<p class="raksasa">43</p>

<p class="label mt">kejadian CCI · 6 titik CCI &gt; 2</p>

Terparah: **hall L4-000 &amp; L4-206 (6 radio)**, L4-001 (5), L4-102 (4)

</div>
<div>

<p class="label">Asal 43 pengganggu</p>

| Asal | Jumlah |
|---|---|
| Jaringan lain (lab, hotspot, fakultas lain) | **21** |
| AP kampus yang bukan 8 AP L4 (hanya eduroam/FILKOM EVENT, atau area lain) | **17** |
| AP lantai 3 | **4** |
| AP L4 lain di kanal yang sama | **1** |

<p class="ket">CSMA/CA tidak peduli nama jaringan: semua radio sekanal harus bergiliran. Rincian 43 baris: output/solusi_L4/bukti_cci_L4.csv. Total = jumlah kolom cci di output/L4_titik.csv.</p>

</div>
</div>

<!--
Di seluruh lantai 4 kami menemukan 43 kejadian seperti tadi. Separuhnya berasal dari jaringan lain seperti lab dan hotspot, dan sebagian besar sisanya radio kampus yang tidak memancarkan WiFi-UB.x. Radio-radio itu tidak membantu pengguna WiFi-UB.x, tapi tetap memakan airtime.

Pendalaman, asal angka 43. Jumlah kolom cci di output/L4_titik.csv yaitu 000=6, 001=5, 003=1, 008=1, 010=2, 011=2, 101=3, 102=4, 104=2, 105=2, 106=1, 107=4, 108=2, 203=1, 205=1, 206=6.
-->

---

## Tiga *kesalahan* pemilihan kanal

<div class="dua g64 tengah">
<div>

![Kanal tiap AP dan CCI per titik](img/kanal_peta.png)

</div>
<div>

<div class="langkah">
<span class="no">01</span><p><strong>AP-F4.6 &amp; AP-F4.13 sama-sama kanal 153</strong> dan terdengar bersama di <span class="m">9 titik</span></p>
<span class="no">02</span><p>4 AP L4 ditaruh di <strong>kanal 149–161</strong>, kanal yang paling ramai</p>
<span class="no">03</span><p>Kanal <strong>DFS 52–64 hampir kosong</strong>, tapi tidak dimanfaatkan</p>
</div>

<p class="ket">Lingkaran merah = jumlah radio sekanal yang terdengar di titik itu. Garis putus merah = dua AP L4 sekanal yang saling tumpang tindih.</p>

</div>
</div>

<!--
Dari peta kanal ini ada tiga masalah pemilihan kanal. Pertama, AP-F4.6 dan AP-F4.13 memakai kanal yang sama, 153, dan terdengar bersama di 9 titik. Kedua, empat AP lantai 4 ditaruh di kanal 149 sampai 161 yang paling ramai. Ketiga, kanal DFS 52 sampai 64 hampir kosong tapi tidak dipakai.

Bukti kanal tiap AP ada di data/map_bssid_L4.csv dan data/passive_L4.csv kolom channel dan width_mhz. Bisa didemokan dengan netsh wlan show networks mode=bssid atau aplikasi WiFiAnalyzer.
-->

---

<!-- _class: gambar -->

## Data Wi-Fi FILKOM: *airtime* per AP

![Airtime 5 GHz per AP lantai 4 menurut data Wi-Fi FILKOM](img/web_airtime.png)

<p class="ket">Airtime = persentase waktu kanal sibuk menurut AP. Kiri: daftar AP kampus (Agu 2025) saat jam kuliah. Kanan: website Wi-Fi FILKOM, Minggu malam (garis abu-abu = rentang antar-snapshot).</p>

<!--
Ini data dari sisi jaringan, dari website Wi-Fi FILKOM. Airtime adalah persentase waktu kanal sibuk menurut AP itu sendiri. Batang merah adalah AP di kanal 153.
-->

---

## Kanal 153 *sibuk tanpa pengguna*

<div class="stat tiga-kolom">
<div><b class="m">85%</b><span>airtime AP Ext F4.13 (kanal 153) dengan hanya 18 klien, jam kuliah 26 Agu 2025. AP lain 18–56%</span></div>
<div><b class="m">±40%</b><span>rata-rata airtime 2 AP kanal 153 (F4.6 &amp; Ext F4.13) dengan 0 klien; 11 snapshot Minggu malam 11 Okt 2026, tidak pernah &lt; 20%</span></div>
<div><b>≤ 10%</b><span>rata-rata airtime 6 AP lantai 4 lain pada saat yang sama (AP-F4.10 sempat naik sesaat)</span></div>
</div>

<div class="dua">
<div>

- Tidak ada pengguna, tapi kanal sibuk: airtime itu **dipakai radio lain** di kanal 153, persis definisi CCI
- Survei kami menemukan hal yang sama: **20 radio** terdengar di kanal 153, dan AP-F4.6 &amp; AP-F4.13 saling dengar di **9 titik**

</div>
<div>

- **Dua sumber berbeda** (laptop kami &amp; data Wi-Fi FILKOM), **dua waktu berbeda** (2025 &amp; 2026), kesimpulan sama
- Rencana kanal baru memindahkan kedua AP ini ke kanal DFS 60 &amp; 56 yang kosong

</div>
</div>

<!--
Ini bukti paling kuat bahwa masalahnya interferensi kanal. Pada Minggu malam, tidak ada satu pun pengguna di dua AP kanal 153, tapi kanalnya tetap sibuk rata-rata sekitar 40 persen waktu, dan di 11 kali pengambilan data tidak pernah di bawah 20 persen. Enam AP lain di kanal berbeda rata-rata paling tinggi 10 persen. Artinya airtime kanal 153 dimakan radio lain. Pola yang sama sudah terlihat di data Wi-Fi FILKOM Agustus 2025, AP kanal 153 punya airtime tertinggi, 85 persen, padahal kliennya cuma 18. Data ini dari data Wi-Fi FILKOM, bukan dari laptop kami, jadi menguatkan temuan survei dari sisi yang berbeda.

Catatan jujur. Nama AP di daftar AP kampus 2025 belum mengikuti lokasi fisik, jadi kami membandingkan per kanal, bukan per nama. Snapshot 2026 diambil di luar jam kuliah. Untuk data jam kuliah, jalankan kelompok6/ambil_web_filkom.py --poll 5 --jam 8 di hari kerja.
-->

---

<!-- _class: gambar -->

## Kepadatan kanal &amp; *asal radio*

![Jumlah radio per kanal di lantai 4](img/radio_kanal.png)

<p class="ket">Jumlah radio 5 GHz yang terdengar ≥ −85 dBm di lantai 4, per kanal 20 MHz. Biru = AP kita, merah/oranye = AP lantai 5/3, ungu = AP kampus lain, abu-abu = jaringan lain. Radio 40/80 MHz dihitung di setiap kanal yang didudukinya.</p>

<!--
Grafik ini menghitung berapa radio yang terdengar di tiap kanal di lantai 4, dan dari mana asalnya. Biru adalah AP kita sendiri, abu-abu jaringan lain seperti lab atau hotspot HP, ungu AP kampus lain.
-->

---

## 149–161 *penuh*, DFS *kosong*

<div class="stat">
<div><b>51</b><span>radio 5 GHz terdengar di L4. Hanya 8 yang AP WiFi-UB.x lantai 4</span></div>
<div><b class="m">17–20</b><span>radio per kanal di 149–161</span></div>
<div><b>2–5</b><span>radio per kanal di 36–48</span></div>
<div><b class="m">0</b><span>radio di kanal DFS 60 &amp; 64 (52 &amp; 56: 1 radio lemah)</span></div>
</div>

<div class="dua">
<div>

- **Kenapa 149–161 padat?** Banyak router dan hotspot memakai UNII-3 dengan lebar 80 MHz secara default. Satu hotspot 80 MHz di kanal 149 menduduki 149, 153, 157, dan 161 sekaligus
- Contoh: hotspot HP 80 MHz terdengar **−35 dBm** di Ext

</div>
<div>

- **Artinya:** kanal 149–161 adalah tempat terburuk untuk AP lantai 4, sementara kanal DFS yang sepi belum dipakai
- Ini **dasar rencana kanal baru** di bagian solusi

</div>
</div>

<!--
Kanal 149 sampai 161 sangat padat, 17 sampai 20 radio per kanal, padahal 4 AP lantai 4 ditaruh di sana. Sebaliknya, kanal 60 dan 64 kosong sama sekali. Ini dasar rencana kanal baru kami.

Pendalaman. Klasifikasi asal radio. AP lantai 3/5 kalau sinyalnya minimal 3 dB lebih kuat di lantai itu setelah koreksi offset laptop. AP kampus lain kalau memancarkan SSID kampus tapi bukan 8 AP L4. Nama SSID pribadi disamarkan untuk privasi. Daftar lengkap di output/solusi_L4/radio_L4.csv.
-->

---

<!-- _class: gambar -->

## Sinyal lantai 5 *bocor* ke lantai 4

![Sinyal AP lantai 3 dan 5 di titik lantai 4](img/floor_peta.png)

<p class="ket">Lingkaran = sinyal AP lantai 5 (merah) dan lantai 3 (oranye) yang terdengar di titik lantai 4; makin besar makin kuat. Label = 6 titik dengan sinyal lantai lain terkuat dan selisihnya dengan AP lantai 4.</p>

<!--
Kami juga mengukur lantai 3 dan 5 untuk melihat apakah sinyal antar-lantai saling bocor. Lingkaran merah adalah sinyal AP lantai 5 yang terdengar di lantai 4.
-->

---

## Kebocoran antar-lantai: *6 titik nyaris tersaingi*

<div class="dua g46 tengah">
<div class="kecil">

- **10 dari 39 titik L4** mendengar AP lantai 5/3 ≥ −75 dBm
- Di **6 titik**, AP lantai 5 hanya kalah ≤ 6 dB dari AP lantai 4, jadi laptop bisa tersambung ke lantai 5. **L4-010: −53 vs −52 dBm**
- Dari lantai 3 lemah (maks. −81 dBm di L4)
- **Dampak:** AP lantai 5 ikut menanggung beban lantai 4 dan roaming makin acak. Kanal L5 yang bocor (40, 48, 161) sudah diperhitungkan di rencana kanal baru

</div>
<div>

<p class="label">Estimasi redaman pelat lantai</p>

![Estimasi redaman pelat lantai](img/floor_redaman.png)

<p class="ket">Sesuai pustaka 20–30 dB, kecuali <span class="m">9 dB</span> di atas F4.6: kemungkinan ada jalur bocor (void, tangga, shaft).</p>

</div>
</div>

<!--
Di 6 titik, sinyal AP lantai 5 hampir sama kuat dengan AP lantai 4. Di titik 010 selisihnya hanya sekitar 1,5 dB, jadi laptop di sana bisa saja tersambung ke AP lantai 5. Redaman pelat lantai 26 sampai 30 dB, sesuai literatur, kecuali di atas F4.6 yang hanya 9 dB. Sinyal dari lantai 3 lemah, jadi tidak bermasalah.

Cara menghitung redaman. Ambil AP lantai 5 di titik L5 tempat sinyalnya terkuat, misal L5-007 −38,6 dBm setelah koreksi offset, lalu ukur AP yang sama di titik L4 tepat di bawahnya, L4-007 −68,6 dBm. Selisihnya 30 dB. Keterbatasan, L3 dan L5 hanya 13 titik, jadi nilai redaman adalah perkiraan kasar.
-->

---

## Uji aktif: sinyal kuat, *tetap loss*

<p class="lead">Scan pasif hanya membaca kuat sinyal. Uji aktif <strong>benar-benar tersambung dan mengirim paket</strong>, jadi mengukur apa yang dirasakan pengguna saat video call.</p>

<div class="stat tiga-kolom sedang">
<div><b class="m">5 / 8</b><span>titik RTT &gt; 50 ms</span></div>
<div><b class="m">3 / 8</b><span>titik packet loss &gt; 2%</span></div>
<div><b>286,5</b><span>Mbps link rate (Wi-Fi 6, 2 stream, 20 MHz)</span></div>
</div>

<div class="mini">

| Titik | RSSI (dBm) | RTT | Jitter | Loss | Catatan |
|---|---|---|---|---|---|
| 102 (Ext) | −49 | 30 ms | 2 ms | <span class="m">10%</span> | sinyal kuat tapi loss, CCI 4 |
| 203 (F4.8) | −64 | <span class="m">108 ms</span> | <span class="m">97 ms</span> | <span class="m">5%</span> | pojok, jauh dari AP |
| 007 | −70 | <span class="m">72 ms</span> | 59 ms | <span class="m">5%</span> | dilayani AP Ext |
| 000 (hall) | −65 | <span class="m">118 ms</span> | 60 ms | 0% | CCI 6 |
| 017 | −58 | <span class="m">132 ms</span> | 76 ms | 0% | latensi tinggi |
| 101 / 106 / 006 | −43 / −53 / −65 | 55 / 42 / 39 ms | – | 0% | relatif baik |

</div>

<p class="ket">Batas modul: RTT ≤ 50 ms, loss ≤ 2%. 20 paket per titik (loss 5% = 1 paket, indikatif). RTT diukur ke internet (Cloudflare), jadi termasuk jaringan kampus. RSSI = bacaan saat uji aktif.</p>

<!--
Uji aktif menjawab pertanyaan, kalau sinyalnya kuat, apakah internetnya juga lancar? Scan pasif hanya membaca kekuatan beacon. Uji aktif benar-benar tersambung dan mengirim 20 paket ke server, lalu mengukur waktu bolak-balik (RTT), seberapa berubah-ubah waktunya (jitter), dan berapa paket yang hilang (loss).

Hasilnya, titik 102 di Ext sinyalnya sangat kuat tapi 10 persen paket hilang. Ini ciri khas interferensi, bukan sinyal lemah. Lima dari delapan titik punya latensi di atas 50 ms.

Catatan metode. Uji 000 dan 017 memakai TCP port 443 ke filkom.ub.ac.id karena ICMP tidak dibalas, 6 titik lain ICMP ke 1.1.1.1. Keduanya server Cloudflare, jadi sebanding. Hasil yang dipakai adalah uji ulang 11.34 sampai 11.39, uji pertama yang gagal (DNS) tidak dipakai.
-->

---

<!-- _class: gambar -->

## Uji roaming *R2*: AP tersambung &amp; ping

![Timeline roaming R2](img/timeline_roaming.png)

<p class="ket">Atas: AP yang dipakai laptop dari waktu ke waktu (× merah = uji aktif gagal, ● hijau = berhasil). Bawah: hasil ping (× = gagal). Area merah = periode gangguan, garis hitam = reconnect manual.</p>

<!--
Grafik atas menunjukkan AP mana yang dipakai laptop dari waktu ke waktu saat kami berjalan dari Ext ke gedung utama dan kembali. Setiap anak tangga adalah perpindahan AP. Grafik bawah adalah hasil ping selama berjalan.
-->

---

## Roaming: yang *terbukti* &amp; yang *belum*

<div class="dua">
<div class="kotak">

<p class="label">Terbukti dari log</p>

- **R1** (keliling gedung utama): pindah AP 1× (AP-F4.4 → AP-F4.3), ping putus ±4 detik
- **R2** (Ext ↔ gedung utama): pindah AP **12× dalam ±13 menit**
- **Ping-pong AP-F4.3 → AP-F4.10 → AP-F4.3 dalam 10 detik**: laptop memilih AP sendiri tanpa panduan dari jaringan
- Inilah dasar usulan **802.11k/v + min-RSSI**

</div>
<div class="kotak merah">

<p class="label">Belum bisa disimpulkan</p>

- 11:22–11:25 laptop tetap tersambung, tapi **38 dari 55 ping gagal** dan DNS gagal; normal lagi setelah **reconnect manual**
- Gejala "tersambung tanpa internet" ini **juga muncul saat survei pasif**, ketika laptop sedang scan berulang
- Hanya 1 laptop, 1 kali. Penyebab bisa jaringan (802.1X/DHCP/DNS), driver, atau aktivitas scan
- Kami catat sebagai **anomali**, bukan temuan; perlu uji ulang dengan perangkat lain tanpa skrip scan

</div>
</div>

<!--
Kami pisahkan mana yang terbukti dan mana yang belum. Yang terbukti dari log, saat berjalan dari Ext ke gedung utama laptop pindah AP 12 kali, termasuk bolak-balik AP-F4.3 dan AP-F4.10 dalam 10 detik. Ini menunjukkan laptop memilih AP sendiri tanpa panduan, jadi kami usulkan 802.11k/v dan min-RSSI.

Yang belum bisa disimpulkan, sempat ada sekitar 3,5 menit laptop tetap tersambung tapi tidak ada internet, dan baru normal setelah kami reconnect manual. Gejala yang sama juga kadang muncul waktu survei pasif ketika laptop sedang scanning. Karena hanya terjadi di satu laptop dan tidak bisa kami ulang secara terkontrol, kami tidak menyimpulkan penyebabnya. Kami catat sebagai anomali dan sarankan admin memeriksa log RADIUS dan DHCP, serta uji ulang dengan perangkat lain.

Kenapa uji roaming tetap penting? Modul meminta hasil uji roaming, dan perpindahan AP adalah pengalaman sehari-hari mahasiswa yang berjalan antar ruang.
-->

---

<!-- _class: bab -->
<!-- header: "03 — Desain Solusi" -->
<!-- _header: "" -->

<p class="nomor">03</p>

# Desain Solusi

<p class="isi-bab">Kriteria, alokasi sumber daya (jumlah AP, kanal, daya), dan penempatan</p>

<!--
Bagian ketiga, bagaimana kami merancang solusinya.
-->

---

## Kriteria dulu, *baru solusi*

| No | Kriteria | Target | Sumber |
|---|---|---|---|
| **K1** | Cakupan | ≥ 95% titik ≥ −67 dBm, tanpa blank spot | modul §4.5 |
| **K2** | Roaming | AP cadangan ≥ −75 dBm di semua titik | modul §4.5 |
| **K3** | Interferensi | CCI ≤ 2 per titik; **tidak ada 2 AP L4 sekanal yang saling dengar** | modul §4.5 |
| **K4** | Kapasitas | beban ≤ 70% pada skenario berat | perhitungan slide 9 |
| **K5** | Regulasi | kanal &amp; daya sesuai Permenkominfo 2/2023 (maks. 23 dBm, indoor) | regulasi |
| **K6** | Biaya | maksimalkan AP yang ada; ubah lewat controller dulu | praktis |

<!--
Sebelum merancang, kami tetapkan enam kriteria, yaitu cakupan, roaming, interferensi, kapasitas, regulasi, dan biaya. Semua solusi nanti diuji terhadap kriteria ini di bagian pembahasan.
-->

---

## Alokasi *sumber daya*

| Komponen | Sekarang | Usulan | Alasan |
|---|---|---|---|
| **Jumlah AP** | 8 | **10** (+AP-F4.2, +AP-F4.5) | K1: F4.2 lemah · K4: 1 kelas = 1 AP |
| **Lebar kanal** | 20 MHz | **20 MHz** | K3: kanal lebar = kanal sedikit = CCI naik |
| **Kanal** | 7 kanal, 153 dipakai 2 AP | **1 AP = 1 kanal**; 4 AP lama tetap; 3 AP pindah ke DFS | K3 |
| **Daya** | default | **AP-F4.14 −6 dB** | −34 dBm di bawah AP, bocor sampai 007 |
| **Roaming** | – | **802.11k/v/r + min-RSSI ±−72 dBm** | 12× pindah AP + ping-pong 10 detik (R2) |

<!--
Dari kriteria itu, kami mengusulkan tiga hal. Pertama, tambah dua AP, satu di F4.2 yang sinyalnya paling lemah, satu di F4.5 supaya F4.3 dan F4.5 tidak lagi berbagi satu AP. Kedua, semua AP tetap 20 MHz dan kanal ditata ulang supaya setiap AP lantai 4 punya kanal sendiri. Ketiga, turunkan daya AP Ext F4.14 sebanyak 6 dB, dan aktifkan fitur roaming.

802.11k memberi daftar AP tetangga, 802.11v menyarankan klien pindah ke AP yang lebih baik, 802.11r mempercepat login ulang WPA2/3-Enterprise saat pindah AP. Min-RSSI melepas klien yang sinyalnya di bawah ambang supaya pindah ke AP terdekat.
-->

---

## 1 AP = *1 kanal*

<div class="dua g46">
<div class="kecil">

| AP | Lama | Baru |
|---|---|---|
| AP-F4.1 | 44 | 44 · tetap |
| AP-F4.3 | 161 | 161 · tetap |
| AP-F4.9 | 48 | 48 · tetap |
| AP-F4.10 | 40 | 40 · tetap |
| AP-F4.4 | 36 | **157** |
| AP-F4.6 | 153 | **60** · DFS |
| AP-F4.13 | 153 | **56** · DFS |
| AP-F4.14 | 157 | **52** · DFS, −6 dB |
| AP-F4.2 *baru* | – | **153** |
| AP-F4.5 *baru* | – | **36** |

</div>
<div>

<p class="label">Perbandingan opsi (dihitung dengan data ukur)</p>

| Opsi | CCI | Tumpang tindih | DFS |
|---|---|---|---|
| Sekarang (8 AP) | 43 | 9 | 0 |
| +2 AP, kanal lama | 39 | <span class="m">36</span> | 0 |
| +2 AP, kanal baru non-DFS | 12 | 32 | 0 |
| **+2 AP, kanal baru + DFS** | **2** | **0** | 3 |

<p class="ket">Tambah AP tanpa atur kanal justru memperparah (9 → 36). Tanpa DFS, 10 AP &gt; 8 kanal, jadi pasti ada AP yang berbagi kanal. Kanal 165 tidak dipakai: di luar pita 5725–5825 MHz.</p>

</div>
</div>

<!--
Dengan 10 AP, 8 kanal non-DFS tidak cukup, jadi 3 AP kami tempatkan di kanal DFS 52, 56, dan 60, yang di lantai 4 hampir kosong. Empat AP lama tidak perlu diubah kanalnya.

Cara rencana dicari (solusi_L4.py). Skor = CCI + titik tumpang tindih AP sekanal + 3 × AP di DFS + 1 × AP lama yang diganti. Komputer mengganti kanal satu AP sekali waktu, menyimpan kalau skor turun, diulang dari 30 titik awal acak (local search).

Rencana valid kalau semua kanal legal, tidak ada dua AP L4 sekanal, dan radio lain di kanal itu lemah. Di 5 GHz dengan 20 MHz, kanal berbeda tidak pernah tumpang tindih, beda dengan 2,4 GHz yang harus 1, 6, 11. Kalau dosen menolak DFS, pakai rencana non-DFS (CCI 12).
-->

---

<!-- _class: gambar -->

## Usulan penempatan *&amp; kanal*

![Usulan solusi di denah lantai 4](img/solusi_peta.png)

<p class="ket">★ = AP baru. Label = kanal lama → baru (warna segitiga = kanal baru). Panah oranye = sinyal AP-F4.14 bocor sampai titik 007. Lingkaran merah = titik lemah/buruk saat ini.</p>

<!--
Ini posisi usulan. Bintang adalah AP baru. AP-F4.2 dipasang di pojok kiri-atas yang sekarang paling lemah dan terhalang lift dan toilet. AP-F4.5 dipasang karena sekarang F4.5 menumpang AP milik F4.3. AP lama tidak perlu dipindah, dan hanya empat yang perlu diganti kanalnya lewat controller. Panah oranye menunjukkan sinyal AP Ext yang terlalu kuat sampai menyeberang ke gedung utama.
-->

---

## Kenapa *tambah 2 AP*, bukan pindah?

<div class="dua">
<div>

<div class="langkah">
<span class="no">★</span><p><strong>AP-F4.2 · kanal 153 → cakupan</strong><br>Menutup pojok kiri-atas (005–008): terlemah −69 dBm, dan 007 sekarang dilayani AP Ext</p>
<span class="no">★</span><p><strong>AP-F4.5 · kanal 36 → kapasitas</strong><br>F4.3 &amp; F4.5 sekarang berbagi AP-F4.3 (126%). Hasilnya: <strong>1 ruang kuliah = 1 AP</strong></p>
</div>

<p class="ket">Dipasang di plafon di dalam ruang, bukan koridor (dinding bata 8–15 dB, pintu 4–6 dB), menjauhi kolom beton dan shaft lift.</p>

</div>
<div>

<p class="label">7 opsi dibandingkan dengan model yang sama</p>

| Opsi | Beban AP terberat |
|---|---|
| Pindah AP-F4.6 ke F4.2 | <span class="m">126%</span> |
| Pindah AP-F4.4 ke F4.2 | <span class="m">126%</span> |
| Pindah AP-F4.1 ke F4.2 | <span class="m">189%</span> |
| Tambah 1 AP di F4.2 saja | <span class="m">126%</span> |
| Tambah F4.2 + F4.8 | <span class="m">126%</span> |
| **Tambah F4.2 + F4.5 (usulan)** | **63%** |

</div>
</div>

<!--
Kenapa tidak memindah AP saja? Kami membandingkan 7 opsi dengan model yang sama. Memindah AP ke F4.2 memang memperbaiki pojok kiri-atas, tapi selalu ada AP lain yang jadi melayani 2 kelas, 126 persen, atau malah 3 kelas, 189 persen. Masalah kapasitas hanya hilang kalau jumlah AP sama dengan jumlah ruang kuliah.

Kenapa bukan F4.8? Sinyal di F4.8 sudah baik (003 −59, 203 −63 dBm) dan F4.8 bukan ruang kuliah utama, jadi AP di sana tidak mengurangi beban. Terlalu padat? Tidak, selama tiap AP punya kanal sendiri. Kalau anggaran hanya cukup 1 AP, prioritaskan AP-F4.2.
-->

---

## Bertahap, *mulai dari yang gratis*

<div class="tiga">
<div class="kotak merah">

<span class="no">Tahap 1</span>

**Konfigurasi controller**

Ubah kanal 4 AP, turunkan daya AP-F4.14 6 dB, aktifkan 802.11k/v/r + min-RSSI

<p class="label mt">Biaya: 0</p>

</div>
<div class="kotak">

<span class="no">Tahap 2</span>

**Pasang 2 AP baru**

AP-F4.2 (kanal 153) dan AP-F4.5 (kanal 36), model sama dengan AP yang ada

<p class="label mt">Biaya: 2 AP + kabel/PoE</p>

</div>
<div class="kotak">

<span class="no">Tahap 3</span>

**Kondisional: +1 AP Ext**

Kalau utilisasi kanal Ext &gt; 50% saat jam sibuk, tambah 1 AP di F4.11/F4.12 (kapasitas Ext 95% di skenario berat)

<p class="label mt">Biaya: 1 AP</p>

</div>
</div>

<p class="besar mt">Feasible: <span class="abu">gratis dulu · hanya +2 AP · sesuai regulasi · DFS sudah dipakai di lantai 3</span></p>

<!--
Solusinya bertahap. Tahap pertama hanya konfigurasi controller tanpa biaya, dan justru ini yang paling berdampak ke CCI. Tahap kedua cuma dua AP. Tahap ketiga kondisional untuk Ext.

DFS legal di Indonesia untuk dalam ruangan (pita 5250–5350 MHz, Permenkominfo 2/2023), dan lantai 3 FILKOM sudah memakai kanal 52, 60, 64, jadi controller dan perangkat terbukti mendukung.
-->

---

<!-- _class: bab -->
<!-- header: "04 — Pembahasan" -->
<!-- _header: "" -->

<p class="nomor">04</p>

# Pembahasan

<p class="isi-bab">Prediksi hasil, simulasi pembanding, dan justifikasi solusi</p>

<!--
Bagian keempat, apakah solusinya benar-benar bekerja.
-->

---

<!-- _class: gambar -->

## Prediksi *sebelum vs sesudah*

![Prediksi cakupan sebelum dan sesudah solusi](img/prediksi.png)

<p class="ket">Model log-distance dari data survei sendiri: n = 2,52, RMSE 5,5 dB, tanpa redaman dinding. Sinyal AP baru dibatasi maks. −48,8 dBm (sinyal terbaik yang pernah terukur dari AP gedung utama). Kiri = kondisi sekarang, kanan = setelah solusi.</p>

<!--
Bagaimana kami tahu solusinya berhasil? Kami membuat model penurunan sinyal dari data survei kami sendiri, lalu menghitung ulang kondisi setelah solusi.

Pendalaman. RSSI(d) = P − 10·n·log10(d). n = 2,52 cocok untuk gedung dengan koridor cincin yang cukup terbuka (ruang bebas n = 2, gedung penuh dinding 3,5 sampai 4). AP lama memakai data terukur (AP-F4.14 dikurangi 6 dB), AP baru memakai model. Hasil per titik di banding_titik_L4.csv.
-->

---

## Semua kriteria *terpenuhi* (prediksi)

<div class="stat sedang">
<div><b>43 → <span class="m">2</span></b><span>CCI total (metode modul) · K3</span></div>
<div><b>9 → <span class="m">0</span></b><span>titik tumpang tindih AP sekanal · K3</span></div>
<div><b>126 → <span class="m">63%</span></b><span>beban AP terberat, skenario berat · K4</span></div>
<div><b>−69 → <span class="m">−63</span></b><span>dBm, RSSI terlemah · K1</span></div>
</div>

<div class="dua">
<div>

- Titik ≥ −67 dBm: **97,4% → 100%** (K1)
- CCI hall (000): **6 → 0**
- Contoh titik: 006 −69 → −56 · 007 −64 → −56 · 008 −61 → −49 dBm

</div>
<div>

- **Kenapa CCI turun?** AP pelayan pindah dari kanal ramai (153/157/161) ke kanal sepi, atau titiknya dilayani AP baru di kanal tanpa pengganggu
- Sisa 2 kejadian (202 &amp; 203): radio lain yang tetap terdengar di kanal AP pelayan

</div>
</div>

<!--
Hasilnya, semua titik di atas −67 dBm, CCI turun dari 43 menjadi 2, tidak ada lagi dua AP lantai 4 yang berbagi kanal, dan setiap ruang kuliah punya AP sendiri. Tapi ini prediksi model, jadi perlu divalidasi dengan survei ulang setelah diterapkan.
-->

---

<!-- _class: gambar -->

## Simulasi pembanding: *kekuatan sinyal*

![Simulasi kekuatan sinyal 10 AP Ruckus dengan rencana kanal usulan](img/sim_sinyal.jpg)

<p class="ket">Simulasi 10 AP dengan rencana kanal usulan dan 128 dinding. Hijau ≥ −57 dBm (excellent), hijau muda −65 s.d. −57, kuning −70 s.d. −65, oranye −80 s.d. −70, merah &lt; −80 dBm.</p>

<!--
Model kami tidak menghitung dinding. Karena itu kami juga membuat simulasi dengan perangkat lunak perencanaan Wi-Fi yang memodelkan 128 dinding, memakai 10 AP dan rencana kanal persis seperti usulan kami, yaitu satu AP per ruang kuliah di gedung utama ditambah 4 AP Ext. Label di tiap AP menunjukkan kanal usulan.
-->

---

## Simulasi *dengan dinding*: kesimpulannya sama

<div class="stat">
<div><b class="m">87,7%</b><span>area ≥ −70 dBm (dihitung dari kotak denah 53 × 34 m)</span></div>
<div><b>10</b><span>AP: 9× Ruckus R650, 1× R750, kanal = rencana usulan</span></div>
<div><b>128</b><span>dinding dimodelkan</span></div>
<div><b>1.807</b><span>m² luas denah</span></div>
</div>

<div class="dua">
<div class="kecil">

<p class="label">Pengaturan simulasi</p>

- Model propagasi **free-space path loss + redaman dinding**, lingkungan kantor
- Tx power 20 dBm per AP, plafon 4 m
- Klien referensi, arah downlink, ambang −70 dBm

</div>
<div class="kecil">

<p class="label">Cara membacanya</p>

- **Semua ruang kuliah hijau atau hijau muda** (≥ −65 dBm). Kuning/oranye hampir semuanya di hall, tangga, toilet, dan luar dinding (atap Lt. 3)
- 87,7% dihitung dari kotak 53 × 34 m termasuk area luar gedung, jadi **cakupan di dalam ruang lebih tinggi**
- Menjawab keterbatasan model kami (tanpa dinding): **10 AP cukup menutup seluruh ruang kuliah**

</div>
</div>

<!--
Simulasi memakai model free-space path loss ditambah redaman 128 dinding, Tx 20 dBm. Angka 87,7 persen terlihat lebih rendah dari prediksi kami, tapi area yang dihitung adalah seluruh kotak denah 53 kali 34 meter, termasuk atap lantai 3 di pojok gedung. Kalau dilihat petanya, semua ruang kuliah hijau. Jadi dengan dinding pun, 10 AP cukup.

Kalau ditanya kenapa versi simulasi sebelumnya 90,2 persen. Versi sebelumnya memakai model ITU-R P.1238 dan rencana kanal yang berbeda. Rencana kanal tidak mengubah kekuatan sinyal, kanal hanya menentukan interferensi. Selisih 2,5 persen itu berasal dari model propagasi yang berganti, dan terjadi di area luar ruang.

Peta data rate tidak kami tampilkan karena memakai klien referensi simulasi yang spesifikasinya berbeda dengan laptop kami, jadi angkanya tidak sebanding dengan link rate terukur 286,5 Mbps.
-->

---

<!-- _class: duagambar -->

## Simulasi: *SNR &amp; interferensi kanal*

<div class="dua">
<div>

![Simulasi SNR](img/sim_snr.jpg)

### Signal-to-noise ratio
<p class="ket">Semua ruang hijau, kategori SNR tertinggi pada legenda simulasi (≥ 30 dB), di atas kebutuhan video ±25 dB. Kuning hanya di tangga dan shaft lift. Melengkapi data kami: Windows tidak memberi noise floor.</p>

</div>
<div>

![Simulasi interferensi kanal](img/sim_interferensi.jpg)

### Channel interference
<p class="ket">Seluruh lantai hijau (interferensi 0–10%): dengan <strong>rencana kanal usulan</strong>, 10 AP tidak saling mengganggu. Simulasi tidak mengenal jaringan lain; dengan data ukur, sisa CCI rencana ini 2 (slide 38).</p>

</div>
</div>

<!--
Simulasi juga memberi dua hal yang tidak bisa kami ukur. Pertama SNR, yang di semua ruang ada di kategori teratas. Kedua interferensi kanal. Dengan rencana kanal usulan kami, seluruh lantai hijau, tidak ada AP lantai 4 yang saling mengganggu. Ini konfirmasi dari alat lain bahwa prinsip satu AP satu kanal memang menghilangkan interferensi antar-AP kita sendiri.

Catatan jujur. Simulasi tidak tahu ada jaringan lain di sekitar (hotspot, lab, AP kampus lain, AP lantai 5). Karena itu kanal kami pilih dari data ukur, dan sisa CCI dari jaringan lain dihitung terpisah, hasilnya 2.
-->

---

<!-- _class: duagambar -->

## Simulasi: *kapasitas &amp; cakupan cadangan*

<div class="dua">
<div>

![Simulasi kapasitas user](img/sim_kapasitas.jpg)

### User capacity
<p class="ket">Seluruh lantai hijau: kapasitas ≥ 150% dari kebutuhan. Sejalan dengan hitungan kami: dengan 1 AP per kelas, beban AP terberat 63% (kapasitas ±1,6× kebutuhan, skenario berat).</p>

</div>
<div>

![Simulasi cakupan sekunder](img/sim_sekunder.jpg)

### Secondary coverage
<p class="ket">Tengah gedung utama hijau (AP kedua ≥ −70 dBm); gedung Ext dan tepi gedung kuning–oranye, jadi AP cadangan di sana lebih lemah. Data ukur kami: semua titik punya AP cadangan ≥ −75 dBm (<strong>K2</strong>).</p>

</div>
</div>

<!--
Peta kapasitas seluruhnya hijau, artinya dengan 10 AP kapasitas yang tersedia minimal 1,5 kali kebutuhan pengguna. Ini cocok dengan hitungan kami. Satu kelas butuh 63 Mbps di skenario berat dan satu AP sanggup sekitar 100 Mbps, jadi dengan satu AP per kelas kapasitasnya sekitar 1,6 kali kebutuhan.

Peta cakupan cadangan menunjukkan AP kedua paling kuat di tengah gedung utama. Di gedung Ext dan tepi gedung, AP cadangan lebih lemah. Data ukur kami tetap memenuhi K2, semua titik punya AP cadangan ≥ −75 dBm.

Legenda kapasitas. Hijau ≥ 150 persen dari kebutuhan, 110 sampai 150, kuning 90 sampai 110, oranye 60 sampai 90, merah di bawah 60. Legenda cakupan cadangan. Kuat ≥ −70, baik −80 sampai −70, cukup −85 sampai −80, lemah −90 sampai −85 dBm.
-->

---

## Simulasi memakai *rencana kanal kami*

<div class="dua">
<div class="kecil">

| AP (simulasi) | Model sim. | Kanal sim. | Kanal usulan |
|---|---|---|---|
| AP-F4.14 (AP 1) | R650 | 52 | 52 ✓ |
| AP-F4.10 (AP 2) | R750 | 40 | 40 ✓ |
| AP-F4.13 (AP 3) | R650 | 56 | 56 ✓ |
| AP-F4.9 (AP 4) | R650 | 48 | 48 ✓ |
| AP-F4.4 (AP 5) | R650 | 157 | 157 ✓ |
| AP-F4.1 (AP 6) | R650 | 44 | 44 ✓ |
| AP-F4.6 (AP 7) | R650 | 60 | 60 ✓ |
| AP-F4.3 (AP 8) | R650 | 161 | 161 ✓ |
| AP-F4.2 *baru* (AP 9) | R650 | 153 | 153 ✓ |
| AP-F4.5 *baru* (AP 10) | R650 | 36 | 36 ✓ |

</div>
<div>

<div class="stat satu-kolom">
<div><b class="m">10 / 10</b><span>AP di simulasi memakai posisi dan kanal usulan kami</span></div>
<div><b>0–10%</b><span>interferensi antar-AP di seluruh lantai menurut simulasi; sisa CCI dari jaringan lain menurut data ukur: 2</span></div>
</div>

<p class="ket">Dua alat berbeda, kesimpulan sama: data ukur kami (CCI 43 → 2, tumpang tindih 9 → 0) dan simulasi dengan dinding (interferensi hijau, kapasitas hijau, semua ruang kuliah tercakup).</p>

</div>
</div>

<!--
Simulasi ini memakai posisi dan rencana kanal persis seperti usulan kami, sepuluh dari sepuluh AP. Hasilnya, interferensi antar-AP hijau di seluruh lantai, kapasitas hijau, dan semua ruang kuliah tercakup. Jadi dua pendekatan yang berbeda, pengukuran langsung dan simulasi dengan dinding, sampai pada kesimpulan yang sama.

Kalau ditanya soal versi simulasi sebelumnya. Versi awal simulasi memakai rencana kanal lain yang juga satu AP satu kanal. Kami uji dengan data ukur, CCI-nya 4 dan 6 AP lama perlu diubah, sedangkan usulan kami CCI 2 dan cukup 4 AP diubah. Karena itu simulasi akhir memakai rencana kanal kami. Hitungannya ada di output/solusi_L4/opsi_kanal_L4.csv baris "+2 AP, kanal dari simulasi".
-->

---

## Kenapa bukan *daya lebih besar* atau *80 MHz*?

<div class="dua">
<div class="kotak">

<h3>Tambah daya?</h3>

- Sinyal **sudah kuat** (97,4% ≥ −67 dBm)
- Sel AP membesar, jadi **lebih banyak AP sekanal saling dengar** dan CCI naik
- **Link asimetris:** AP bisa 23 dBm, HP/laptop hanya ±15 dBm
- Klien makin **sticky** (contoh: 007 dilayani AP Ext)
- Batas legal **23 dBm** indoor

</div>
<div class="kotak">

<h3>Kanal 80 MHz?</h3>

- Kanal non-DFS tidak tumpang tindih: **20 MHz = 8, 40 MHz = 4, 80 MHz = 2**
- 10 AP yang saling dengar di 2 kanal = **±5 AP per kanal**, airtime tiap AP tinggal ±1/5
- Noise naik **+6 dB** (−101 → −95 dBm)
- MCS 9 butuh sinyal **6 dB lebih kuat** (−57 → −51 dBm)

</div>
</div>

<p class="besar mt">Banyak kanal sempit <span class="m">&gt;</span> sedikit kanal lebar</p>

<!--
Dua pertanyaan yang sering muncul. Kenapa tidak tambah daya? Sinyal sudah kuat, menaikkan daya memperbesar sel sehingga CCI naik, membuat link asimetris dan klien makin sticky, dan dibatasi regulasi 23 dBm. Kenapa tidak 80 MHz? Kanal non-DFS 80 MHz hanya ada 2 blok, padahal ada 10 AP yang saling dengar, rata-rata 5 AP per kanal, airtime tiap AP tinggal seperlima. Analogi jalan tol, 8 lajur kecil yang masing-masing dipakai 1 bus lebih lancar daripada 2 lajur besar yang masing-masing dipakai 5 bus bergantian.

Derau termal = −174 dBm/Hz + 10·log10(lebar), 20 MHz ≈ −101 dBm, 80 MHz ≈ −95 dBm.
-->

---

<!-- _class: bab -->
<!-- header: "05 — Kesimpulan" -->
<!-- _header: "" -->

<p class="nomor">05</p>

# Kesimpulan

<p class="isi-bab">Kesimpulan, keterbatasan, dan referensi</p>

<!--
Bagian terakhir, kesimpulan.
-->

---

## Bukan sinyal lemah, tapi *kanal terlalu ramai*

<div class="dua g64">
<div>

<div class="langkah">
<span class="no">01</span><p>Cakupan sinyal lantai 4 <strong>sudah baik</strong>: 97,4% ≥ −67 dBm, tanpa blank spot</p>
<span class="no">02</span><p><strong>Masalah utama: co-channel interference.</strong> 6 dari 10 titik bermasalah, 43 kejadian, 2 AP L4 sekanal, kanal 149–161 padat, DFS tidak dimanfaatkan. <strong>Dikonfirmasi data Wi-Fi FILKOM:</strong> AP kanal 153 airtime tertinggi (85% di 2025; ±40% tanpa klien di 2026)</p>
<span class="no">03</span><p>Sinyal lantai 5 bocor ke lantai 4 (6 titik nyaris tersaingi); roaming tidak terarah: 12× pindah AP termasuk ping-pong dalam 10 detik</p>
<span class="no">04</span><p><strong>Solusi:</strong> 1 AP = 1 kanal (3 di DFS), +2 AP (F4.2, F4.5), AP-F4.14 −6 dB, 802.11k/v/r. Prediksi: CCI 43 → 2, semua titik ≥ −67 dBm, beban 126% → 63%. Didukung simulasi dengan dinding</p>
</div>

</div>
<div class="kotak">

<p class="label">Keterbatasan</p>

<div class="kecil">

- SNR tidak terukur dari laptop; data Wi-Fi FILKOM hanya memberi SNR klien (median 47 dB se-gedung, di luar jam kuliah)
- Prediksi = model tanpa dinding; simulasi tanpa jaringan sekitar
- Posisi AP-F4.6 &amp; AP-F4.1 hasil estimasi
- 1 slot waktu survei; 20 paket per uji aktif
- Anomali "tersambung tanpa internet" belum bisa dijelaskan (1 laptop, 1 kali)
- Perlu **survei ulang** setelah implementasi

</div>
</div>
</div>

<!--
Kesimpulannya, masalah Wi-Fi lantai 4 bukan sinyal yang lemah, tapi kanal yang terlalu ramai. Solusi terpenting justru yang paling murah, yaitu mengatur ulang kanal dan memperbaiki roaming lewat controller, lalu menambah dua AP supaya setiap ruang kuliah punya AP sendiri.
-->

---

## *Referensi*

<div class="kecil">

1. Modul *Hands-on: Pemetaan Kualitas Sinyal Wi-Fi 5 GHz Gedung FILKOM*
2. IEEE Std 802.11-2020, *Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications*
3. Permenkominfo No. 2 Tahun 2023 tentang Penggunaan Spektrum Frekuensi Radio Berdasarkan Izin Kelas
4. Coleman, D. &amp; Westcott, D., *CWNA Certified Wireless Network Administrator Study Guide*, Sybex
5. Cisco, *High Density Experience (HDX) Deployment Guide*
6. ITU-R P.1238, *Propagation data and prediction methods for the planning of indoor radiocommunication systems*
7. Zoom Support, *Zoom system requirements: bandwidth* (KB0060748)
8. Microsoft Learn, *Native Wifi API*
9. Website Wi-Fi FILKOM, `filkom.ub.ac.id/wifi` (API publik *recommend* &amp; *clients*, data live), diakses 11 Oktober 2026

</div>

<!--
Referensi utama adalah modul, standar IEEE 802.11, dan regulasi Permenkominfo 2/2023 untuk kanal dan daya. Angka kebutuhan bandwidth dari panduan resmi Zoom.
-->

---

<!-- _class: penutup -->
<!-- _header: "" -->

# Terima<br>kasih

Masalahnya bukan sinyal yang lemah, tapi kanal yang terlalu ramai.

<!--
Tutup dengan kalimat kunci, lalu buka sesi tanya jawab. Persiapan jawaban ada di OUTLINE_PPT.md bagian F.
-->
