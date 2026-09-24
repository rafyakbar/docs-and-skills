# Panduan Pemetaan Bukti & Kerangka CER (Claim-Evidence-Reasoning)

Dalam kepenulisan akademik, outline bukan sekadar daftar judul sub-bab—melainkan sebuah **cetak biru argumentatif dan empiris**. Panduan ini menjelaskan cara mengintegrasikan kerangka Klaim-Bukti-Penalaran (*Claim-Evidence-Reasoning* / CER) dan pelacakan kesenjangan data (*gap tracking*) ke dalam penyusunan outline.

---

## 1. Pola Klaim-Bukti-Penalaran (CER Pattern)

Untuk setiap bab atau sub-bab substantif dalam outline, tentukan rantai argumen secara eksplisit:

```
┌──────────────────────────────────────────────────────────┐
│ KLAIM: Pernyataan asersi apa yang diajukan pada bab ini? │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ BUKTI: Data empiris, statistik, atau sitasi apa yang     │
│        secara langsung mendukung klaim tersebut?         │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ PENALARAN: Bagaimana bukti tersebut membuktikan klaim    │
│            secara logis dan menghubungkannya ke tesis?   │
└──────────────────────────────────────────────────────────┘
```

### Contoh Penguraian CER dalam Format Outline

```markdown
#### 5.2 Temuan untuk RQ1: Pengaruh Bantuan AI terhadap Latensi Penulisan
- **Alokasi Target Kata**: 400 kata (6,6% dari total paper)
- **Tujuan (Objective)**: Melaporkan perbedaan kuantitatif waktu penyelesaian tugas antara kelompok kontrol dan perlakuan.
- **Peta Argumen CER**:
  - **Klaim (Claim)**: Partisipan yang menggunakan asisten AI menyelesaikan penyusunan draf naskah 34% lebih cepat dibandingkan kelompok kontrol manual.
  - **Bukti (Evidence)**: Hasil uji ANOVA pada kohort eksperimen ($F(1, 142) = 18,42, p < 0,001$, Cohen's $d = 0,72$), yang dirangkum pada Tabel 2.
  - **Penalaran (Reasoning)**: Modul temu-kembali otomatis dan pengindeksan sitasi secara substansial mengurangi beban kognitif (*cognitive overhead*) selama tahap awal sintesis literatur.
- **Sumber/Data yang Ditugaskan**: Dataset Uji Coba Eksperimen B, Tabel 2.
- **Elemen Visual**: Tabel 2 (Waktu penyelesaian berdasarkan jenis tugas).
```

---

## 2. Mengelola Kesenjangan Materi (`[MATERIAL GAP]`)

Sebelum penulisan draf naskah dimulai, outline wajib mengungkap secara transparan bukti-bukti yang belum tersedia. Langkah ini mencegah halusinasi penulis, asersi tanpa landasan data, atau kemunculan sitasi literatur fiktif (*phantom citations*).

### Protokol Penandaan (Tagging Protocol)

Ketika sebuah bagian memerlukan klaim yang saat ini masih kekurangan data pendukung atau literatur terverifikasi, berikan anotasi secara eksplisit menggunakan:

```markdown
[MATERIAL GAP: <deskripsi data/sumber yang diperlukan>]
```

### Tingkat Keparahan Kesenjangan (Severity Levels)

1. **Kesenjangan Data Empiris (Empirical Data Gap)**:
   - `[MATERIAL GAP: Memerlukan hasil uji post-hoc ANOVA dari kohort survei]`
   - *Tindakan*: Ditandai agar tim data / peneliti menghitung analisis statistik ini sebelum penulisan Bagian 5.3 dimulai.
2. **Kesenjangan Dukungan Literatur (Literature Support Gap)**:
   - `[MATERIAL GAP: Memerlukan sitasi terkini 2024–2026 mengenai adopsi AI lintas disiplin di perguruan tinggi]`
   - *Tindakan*: Ditandai untuk penelusuran literatur terarah sebelum penulisan Bagian 3.2 dimulai.
3. **Kesenjangan Justifikasi Metodologis (Methodological Justification Gap)**:
   - `[MATERIAL GAP: Berikan justifikasi mengapa convenience sampling tidak mengorbankan validitas internal]`
   - *Tindakan*: Ditandai agar penulis menyusun argumen pembelaan khusus pada Bagian 4.2.

---

## 3. Format Matriks Bukti (Evidence Matrix Format)

Untuk paper yang menangani basis literatur ekstensif, susunlah **Matriks Bukti-ke-Bab (Evidence-to-Section Matrix)** di akhir dokumen outline:

| Bab / Bagian | Klaim Utama | Sitasi Primer / Sumber Data | Status |
|---|---|---|:---:|
| 2.2 Rumusan Masalah | Integrasi AI memicu risiko validasi epistemik baru | Smith & Lee (2025); Nature (2026) | Terverifikasi |
| 3.1 Model Teoretis | Teori beban kognitif menjelaskan akselerasi penulisan draf | Sweller (2011); Paas et al. (2024) | Terverifikasi |
| 4.3 Instrumen | Survei SUS menunjukkan tingkat kegunaan antarmuka yang tinggi | Skor uji coba kegunaan (*usability*) ($n=85$) | Terverifikasi |
| 5.4 Retensi Jangka Panjang | Retensi pengetahuan jangka panjang tetap tidak terpengaruh | `[MATERIAL GAP: Menunggu data delayed post-test]` | **KESENJANGAN (GAP)** |

Matriks ini memberikan garansi bahwa saat penulisan draf lengkap dimulai, setiap bab telah memiliki pijakan bukti yang sahih dan teruji.
