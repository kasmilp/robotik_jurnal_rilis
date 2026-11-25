# Dataset Uji — `progres_robotika.pdf`

Dokumen ini memetakan **semua data** yang dibutuhkan `progres_robotika.pdf` (Kelompok 3, Teknik Informatika Unhas, Draft 1 — 1 Oktober 2026). Berisi 3 komponen: **HANDS** (publik, sudah diunduh), **Non-command corpus** (harus direkam), dan **Command trial set** (harus direkam).

---

## Ringkasan kebutuhan data (dari paper)

| ID | Komponen | Section | Jumlah | Status | Pemilik |
|----|----------|---------|--------|--------|---------|
| D1 | HANDS dataset (RGB + depth + anotasi) | 5.1, 5.2, 5.3 | 5 subjek × 15 gesture × 150 frame | ✅ Publik (Mendeley) | Nuzzi et al. 2021 |
| D2 | Non-command corpus | 4.7, 5.6 | ≥50 menit, 10 operator | ⚠️ Rekam sendiri | kelompok |
| D3 | Command trial set | 4.7 | 500 trial (10 op × 5 cmd × 10 rep) | ⚠️ Rekam sendiri | kelompok |

---

## D1 — HANDS (data pelatihan classifier)

- **Sumber:** Mendeley Data, DOI `10.17632/ndrczc35bt.2` (CC BY 4.0).
- **Artikel pendamping:** Nuzzi et al. 2021 (Data in Brief) & 2020 (RCIM).
- **Isi per subjek:** 2400 RGB + 2400 depth frame; 12 gesture satu-tangan (kanan/kiri) + 3 gesture dua-tangan ⇒ 15 label.
- **Paper memakai:** hanya kanal RGB (Section 5.1); landmark MediaPipe 21 titik; dataset dihitung ulang oleh penulis: 12.000 frame → 21.750 hand crop (2 box/frame untuk 12 kelas, 1 box untuk 3 kelas).
- **Struktur folder:** `HANDS/RGB/SubjectN.zip`, `HANDS/Depth/SubjectN_Depth.zip`, `HANDS/annotations/SubjectN.{mat,txt}`, `HANDS/scripts/*`.

### Catatan reproduksi (dari paper)
1. **Perbaikan path**: file anotasi masing-masing subjek menunjuk ke folder subjek *berikutnya*; hanya pakai nama file + pasangkan ke subjek yang benar (Section 5.1).
2. **Defect label**: gesture *Horiz* punya 300 frame/subjek (bukan 150) — perhatikan saat menghitung total.
3. **Crop vs full frame**: training pakai landmark dari *crop*; pada saat live, landmark dari *full frame*. Normalisasi beda ±0.05 (Section 6.1). Untuk ablation, retrain dengan landmark full-frame.
4. **2-hand classes**: Collab, XSign, TimeOut dianotasi 1 box (dua tangan); landmarker hanya mengembalikan 1 tangan ⇒ recall rendah (Section 5.4). Hati-hati saat memetakan ke command/vocabulary.
5. **Split wajib LOSO**, bukan random frame split (H5; Section 5.3).

---

## D2 — Non-command corpus (harus direkam)

Tujuan: mengukur **false-activation rate per menit** (FA/min) saat tidak ada perintah, untuk H1–H4.

### Spesifikasi dari paper (Section 4.7)
- **10 operator**, masing-masing menjalani **2 blok terbalans (counterbalanced)**.
- Setiap operator: **5 menit** aktivitas alami di depan kamera ⇒ total ±50 menit.
- **Aktivitas sesuai skrip standar** (ulangi supaya bisa diulang):
  1. berbicara sambil gestur,
  2. berjalan melewati frame,
  3. menyesuaikan pakaian,
  4. memberi isyarat ke seseorang di luar frame,
  5. memegang ponsel.
- **Variasi subjek**: warna kulit, tangan dominan (handedness), panjang lengan, pemakaian kacamata — ini memengaruhi ekstraksi landmark. Dengan 10 orang, hanya deskriptif (bukan statistik).
- **Konsen tertulis** semua partisipan.

### Yang wajib direkam per frame (agar replay semua konfigurasi L4 memungkinkan)
- waktu *capture* (monotonic clock),
- waktu saat output classifier tersedia,
- apakah tangan ditemukan (yes/no),
- **vektor probabilitas penuh** (bukan hanya kelas terprediksi!) — Section 4.5.

### Output
- `NonCommand/record_log.csv` — kolom: `t_capture` `t_classifier_ready` `hand_found` `probs[0..14]` `operator_id` `block_id`.
- `NonCommand/operators.csv` — karakteristik operator (skin_tone, handedness, sleeve, glasses).
- `NonCommand/activity_script.pdf` — skrip aktivitas standar.

---

## D3 — Command trial set (harus direkam)

Tujuan: mengukur **command success rate**, **latency**, dan memvalidasi decision layer.

### Spesifikasi dari paper (Section 4.7)
- **10 operator × 5 perintah × 10 ulangan = 500 trial**.
- Perintah (differential-drive): `forward`, `backward`, `turn left`, `turn right`, `stop`.
- **Wake gesture** untuk V3: `Span` (dipilih dari analisis confusion, Section 5.5).
- Setiap trial merekam **timestamp cue** dan **timestamp keputusan**.

### Keputusan protokol yang masih terbuka (harus diselesaikan sebelum rekam)
> *"[Open protocol decision: V3 needs the wake gesture inside the trial, while V0–V2 latency should not include it. Either record each trial in two conditions (with and without wake) or store a separate cue time for the wake and for the command.]"* — paper, Section 4.7.

**Rekomendasi penulis dokumen ini:** satu trial dengan **dua timestamp cue** (wake & command), bukan dua kondisi terpisah:
- V0–V2 dihitung dari *command cue*;
- V3 dihitung dari *wake cue*, plus lapor `wake success rate` dan `false wake rate` terpisah.
Alasan: menghindari penggandaan trial & urutan efek (order effect).

### Kolom log per trial
`operator_id` `block_id` `trial_id` `intent_cmd` (5 perintah) `cue_wake_t` `cue_cmd_t` `decision_t` `decided_cmd` `accepted` (0/1) `latency_ms`.

### Catatan
- **Setelah seluruh data direkam**, semua konfigurasi L4 direplay offline dari *vektor probabilitas* — tidak perlu rekam ulang per strategi (Section 4.5, "Record once, evaluate many").
- Ukuran instalasi per frame: jika 15 kelas × float32 (4 byte) + timestamp ⇒ ± 64 byte/frame. Untuk 5 menit @30fps ≈ 9000 frame ⇒ ± 0,6 MB/operator (sangat ringan). **Pastikan menyimpan probabilitas, bukan hanya argmax.**

---

## Status unduhan HANDS

✅ **24/24 file lengkap** (Nov 2026):

- [x] Subject1.zip … Subject5.zip (RGB, masing-masing ±1,3–1,4 GB)
- [x] Subject1_Depth.zip … Subject5_Depth.zip (Depth)
- [x] Subject1.mat/.txt … Subject5.mat/.txt (anotasi)
- [x] Bags2Imgs.m, base_table.mat, RecordCreate.py, Table2Txt.m (script)

> Manifest hasil unduhan ada di `HANDS/_download_manifest.json`.
> Hasil validasi (unzip + hitung frame/crop) ada di `HANDS/_validation.json` dan dicetak oleh `HANDS/scripts/validate_hands.py`.
