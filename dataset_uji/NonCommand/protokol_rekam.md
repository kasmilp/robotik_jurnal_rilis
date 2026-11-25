# Protokol Rekam — Non-Command Corpus (D2)

Berdasarkan `progres_robotika.pdf` Section 4.7. **Tujuan:** mengukur **false-activation per menit (FA/min)** selama tidak ada perintah.

---

## Target

- 10 operator × 5 menit = **50 menit** total.
- Tiap operator: 2 blok **counterbalanced** (urutan aktivitas beda) — mengurangi bias urutan.

## Aktivitas (skrip standar, wajib diulang persis)

| # | Aktivitas (5 menit/blok) | Catatan |
|---|---------------------------|---------|
| 1 | Berbicara sambil gestur | artikulasi tangan alami, bukan maksud perintah |
| 2 | Berjalan melewati frame | masuk/keluar bidang pandang kamera |
| 3 | Menyesuaikan pakaian | menaikkan lengan, menyelipkan baju, dll. |
| 4 | Memberi isyarat ke orang lain di luar frame | tangan keluar frame sebagian |
| 5 | Memegang ponsel | telusuri layar, angkat ke telinga |

## Karakteristik operator (untuk tabel deskriptif)

- Warna kulit
- Tangan dominan (kanan/kiri)
- Panjang lengan (pendek/sedang/panjang)
- Memakai kacamata (ya/tidak)

> Dengan 10 orang: deskriptif saja, **tidak diklaim bermakna statistik**.

## Yang direkam per frame (wajib — agar replay semua L4)

1. `t_capture` — waktu capture (monotonic clock)
2. `t_classifier_ready` — waktu output classifier tersedia
3. `hand_found` — tangan terdeteksi? (0/1)
4. `probs[0..14]` — **vektor probabilitas penuh** (15 kelas), bukan hanya argmax

## Format log (CSV)

```csv
operator_id,block_id,frame_idx,t_capture,t_classifier_ready,hand_found,p0,p1,...,p14
```

## Checklist pra-rekam

- [ ] Konsen tertulis semua partisipan
- [ ] Kamera USB 640×480 @30fps, fokus tetap
- [ ] Posisi kamera & pencahayaan dicatat (untuk reproduksibilitas)
- [ ] Satu monotonic clock untuk semua timestamp
- [ ] Uji: simpan vektor probabilitas (bukan argmax) — verifikasi ukuran file ±0,6 MB/operator untuk 5 mnt
- [ ] Blok counterbalanced: acak urutan 5 aktivitas per operator
