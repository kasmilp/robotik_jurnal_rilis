# Protokol Rekam — Command Trial Set (D3)

Berdasarkan `progres_robotika.pdf` Section 4.7. **Tujuan:** mengukur **command success rate** dan **latency**.

---

## Target

- 10 operator × 5 perintah × 10 ulangan = **500 trial**.

## Vocabulary (differential-drive)

- Perintah: `forward`, `backward`, `turn left`, `turn right`, `stop`
- Wake gesture (V3): `Span` (dipilih dari analisis confusion, Section 5.5)

## Keputusan protokol (Open Decision dari paper)

Paper membiarkan terbuka:
> *"V3 needs the wake gesture inside the trial, while V0–V2 latency should not include it. Either record each trial in two conditions (with/without wake) or store a separate cue time for the wake and for the command."*

**Rekomendasi:** rekam **satu trial dengan dua timestamp cue** (bukan dua kondisi):

- `cue_wake_t` — saat isyarat wake ditampilkan
- `cue_cmd_t` — saat perintah ditampilkan

Analisis:
- V0–V2 → hitung latency dari `cue_cmd_t`
- V3 → hitung latency dari `cue_wake_t`; lapor **wake success rate** & **false wake rate** terpisah

## Format log per trial (CSV)

```csv
operator_id,block_id,trial_id,intent_cmd,cue_wake_t,cue_cmd_t,decision_t,decided_cmd,accepted,latency_ms
```

## Balanced & urutan

- 10 ulangan per perintah per operator
- Urutan perintah diacak per blok (counterbalanced)
- Hindari pengulangan perintah yang sama berturut-turut

## Checklist pra-rekam

- [ ] Konsen tertulis
- [ ] Sinkronisasi cue & decision pada satu monotonic clock
- [ ] Simpan juga vektor probabilitas (fil kasus perlu replay ulang)
- [ ] Layar output (actuator) disembunyikan dari operator
- [ ] Posisi kamera & pencahayaan dicatat
- [ ] Tentukan urutan acak perintah sebelum rekam
