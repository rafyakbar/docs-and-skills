# Protokol Kontrak Sprint Schema 13.2: Dimensi & Mesin Keputusan

Dokumen ini mendefinisikan secara formal spesifikasi matematis dan prosedural Kontrak Sprint Schema 13.2 yang digunakan untuk mengevaluasi kelayakan naskah akademik dan menghasilkan keputusan editorial deterministik.

---

## 1. Spesifikasi 6 Dimensi Akseptasi (Schema 13.2)

Setiap naskah dievaluasi terhadap 6 dimensi independen yang memiliki batasan peran (*role-scoping*) dan prioritas tertentu:

| ID Dimensi | Nama Dimensi | Prioritas | Peran yang Berhak (Eligible Roles) | Peran Pemilik (Owner Role) | Cakupan Evaluasi & Batas Integritas |
|:---:|---|:---:|:---:|:---:|---|
| **D1** | `methodology_rigor` | **Mandatory** | `["methodology"]` | `methodology` | Desain eksperimen bebas bias, pemisahan dataset strictly patient/entity-level, kecukupan ukuran sampel, validitas uji inferensial (p-value, interval kepercayaan 95%), serta reprodusibilitas kode & data. |
| **D2** | `domain_accuracy` | **Mandatory** | `["domain"]` | `domain` | Kebenaran representasi teori domain, ketepatan terminologi teknis/medis, peliputan literatur primer terkini, dan komparasi yang adil terhadap baseline state-of-the-art (SOTA). |
| **D3** | `argumentative_coherence` | **Mandatory** | `["da", "methodology"]` | `da` | Konsistensi tesis inti, penalaran bebas dari kesalahan logika (*fallacies*), deteksi data cherry-picking, dan ketahanan terhadap skenario penyangkalan terkuat (*counter-arguments*). |
| **D4** | `cross_disciplinary_relevance` | **High** | `["perspective"]` | `perspective` | Aksesibilitas bagi pembaca lintas disiplin, potensi adopsi praktis, kepatuhan etika data subjek/pasien, dan pertimbangan dampak kebijakan/sosial. |
| **D5** | `writing_and_structure` | **Normal** | `["eic"]` | `eic` | Alur naskah IMRaD kanonikal, kejelasan visualisasi grafik/tabel, keterbacaan gaya bahasa akademik, dan kelengkapan deklarasi pendanaan/konflik kepentingan. |
| **D6** | `venue_fit_and_contribution` | **Mandatory** | `["eic"]` | `eic` | Kesesuaian fokus dengan profil penerbit/jurnal target, orisinalitas kontribusi (bukan hanya peningkatan inkremental marjinal), dan kejelasan nilai tambah bagi pembaca. |

---

## 2. Prinsip Kesetaraan Keputusan (Decision Symmetry #574 B1)

Evaluasi editorial berlandaskan 3 pilar etika saintifik:
1. **Beban Bukti Simetris (*Symmetric Evidence Standards*)**:  
   Kesimpulan *Accept* dan *Reject* memikul beban pembuktian ilmiah yang setara. *Accept* membutuhkan verifikasi terjangkar positif bahwa setiap kriteria terpenuhi, persis sebagaimana *Reject* membutuhkan bukti terjangkar bahwa kriteria gagal. Tidak ada margin kehati-hatian asimetris yang mempermudah salah satu arah.
2. **Keputusan Mengikuti Kriteria, Bukan Distribusi Target (*Distribution Independence*)**:  
   Rigor tinjauan berasal dari standar venue dan ekspektasi jenis artikel, bukan dari target persentase tingkat penerimaan (*acceptance rate base rates*). Sesi ulasan yang menghasilkan lebih banyak penolakan tidak serta-merta lebih bermutu.
3. **Independensi Register Bahasa dari Keparahan (*Bidirectional Register Independence*)**:  
   Kesopanan tutur akademik (*respectful/constructive tone*) hanya mengatur pilihan kata (*wording*), dan **dilarang menurunkan tingkat keparahan (*severity*)**. Sebaliknya, gaya bahasa yang tajam atau adversarial **dilarang menaikkan tingkat keparahan**.

---

## 3. Skala Pengukuran Status Dimensi

Setiap dimensi dinilai berdasarkan akumulasi temuan kelemahan ke dalam 4 status diskret:

| Status Dimensi | Kriteria Pemicu (Berdasarkan Temuan Kelemahan) | Makna Metodologis |
|:---:|---|---|
| **`pass`** | Tidak ada temuan kelemahan, atau hanya memuat saran perbaikan tipografis minor. | Dimensi memenuhi standar publikasi internasional secara penuh. |
| **`warn`** | Ditemukan 1 kelemahan berderajat `MAJOR` atau $\ge 2$ kelemahan berderajat `MINOR`. | Terdapat celah atau ketidakjelasan yang dapat diperbaiki dalam hitungan minggu tanpa merombak arsitektur riset. |
| **`block`** | Ditemukan 1 kelemahan berderajat `CRITICAL` atau $\ge 2$ kelemahan berderajat `MAJOR`. | Terdapat cacat metodologis/teoretis serius yang menuntut analisis ulang mendalam atau restrukturisasi argumen inti. |
| **`fatal`** | Ditemukan $\ge 2$ kelemahan berderajat `CRITICAL` yang meruntuhkan keabsahan klaim utama (misal: *data leakage* fatal pada model). | Cacat mendasar yang tidak dapat diselamatkan melalui revisi standar; paper tidak layak terbit pada venue ini. |

---

## 4. Mesin Keputusan Editorial Deterministik (Aturan F0 – F5)

Keputusan akhir editorial (Accept / Minor Revision / Major Revision / Reject) ditentukan melalui evaluasi berurutan dari tingkat keparahan tertinggi ke terendah:

```
                  ┌─────────────────────────────────────┐
                  │ Evaluasi Seluruh Dimensi (D1 - D6) │
                  └──────────────────┬──────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   │
  [F1] Mandatory Dimensi Fatal? ──(Ya)──> REJECT               │
           │ (Tidak)                                           │
           ▼                                                   │
  [F2] Mandatory Dimensi Block? ──(Ya)──> MAJOR REVISION       │
           │ (Tidak)                                           │
           ▼                                                   │
  [F3] >=2 Mandatory Dimensi >=Warn (Mayoritas)? ──(Ya)──> MAJOR REVISION
           │ (Tidak)                                           │
           ▼                                                   │
  [F4] High Dimensi (D4) Block? ──(Ya)──> MAJOR REVISION       │
           │ (Tidak)                                           │
           ▼                                                   │
  [F5] Ada Dimensi >=Warn? ──(Ya)──> MINOR REVISION            │
           │ (Tidak)                                           │
           ▼                                                   │
  [F0] Seluruh Dimensi Pass ──> ACCEPT (dengan Cek DA Critical)│
                                                               ▼
                                                  [DA CRITICAL Terbuka?]
                                                  ├──(Ya)──> TAHAN FINALISASI (Marker Escalation)
                                                  └──(Tidak)─> RESMI ACCEPT
```

### Tabel Aturan Resmi Kontrak Sprint:

| ID Aturan | Severity | Quantifier | Ekspresi Formal (Expression) | Aksi Kanonikal | Keputusan |
|:---:|:---:|:---:|---|---|:---:|
| **F1** | 95 | `any` | `any mandatory dimension has a fatal block` | `editorial_decision=reject` | **REJECT** |
| **F2** | 90 | `any` | `any mandatory dimension scores 'block'` | `editorial_decision=major_revision` | **MAJOR REVISION** |
| **F3** | 70 | `majority` | `two or more mandatory dimensions score 'warn' or worse` | `editorial_decision=major_revision` | **MAJOR REVISION** |
| **F4** | 60 | `any` | `any high-priority dimension scores 'block'` | `editorial_decision=major_revision` | **MAJOR REVISION** |
| **F5** | 40 | `any` | `any dimension scores 'warn' or worse` | `editorial_decision=minor_revision` | **MINOR REVISION** |
| **F0** | 10 | `all` | `every dimension scores 'pass'` | `editorial_decision=accept` | **ACCEPT** |

> **Formula Kuantor Mayoritas (*Majority Quantifier Formula* untuk F3)**:  
> Suatu dimensi dianggap berstatus $\ge$ `warn` oleh mayoritas jika jumlah penilai yang memenuhi syarat (*eligible*) yang memberikan status tersebut memenuhi ambang batas:
> $$\text{threshold}(n) = \begin{cases} 1, & n = 1 \\ 2, & n = 2 \\ \lfloor n/2 \rfloor + 1, & n \ge 3 \end{cases}$$

---

## 5. Protokol Adjudikasi DA CRITICAL (Anti-Silent Accept)

Jika evaluasi mekanis menghasilkan rekomendasi `ACCEPT`, sistem wajib melakukan verifikasi silang terhadap temuan **Devil's Advocate (D3)**:
- **Status Tripartit Adjudikasi DA**:
  Setiap isu kritis Devil's Advocate (`C1..Cn`) wajib diadjudikasi oleh EIC ke salah satu dari 3 status:
  1. `VALIDATED`: Isu diakui benar dan terbukti merupakan cacat naskah $\rightarrow$ Memblokir *Accept*.
  2. `REJECTED`: Isu ditolak oleh EIC disertai alasan dan bukti sanggahan sah $\rightarrow$ **Tidak lagi menghalangi *Accept***.
  3. `UNRESOLVED`: Isu belum dapat diputuskan atau belum ada bukti sanggahan $\rightarrow$ Memblokir *Accept*.
- **Aturan Penahanan Finalisasi (*Never Auto-Downgrade Mechanical Action*)**:
  Jika terdapat temuan `VALIDATED` atau `UNRESOLVED`, keputusan mekanis tetap tercatat sebagai `ACCEPT`, namun sintesis **wajib menyematkan penanda eskalasi**:
  ```text
  [DA-CRITICAL-VS-ACCEPT: <n> validated/unresolved]
  ```
  Marker ini membekukan status finalisasi naskah hingga penulis menyajikan bukti sanggahan atau membatasi klaim.

---

## 6. Format 4 Baris Audit Kanonikal (Pinned Audit Line Grammar)

Setiap berkas keputusan editorial wajib menyertakan blok audit baku untuk verifikasi otomatis:
```text
dimension_verdicts: [D1=..., D2=..., D3=..., D4=..., D5=..., D6=...]
fired_conditions: [F...]
da_critical_adjudications: [C1=VALIDATED|REJECTED|UNRESOLVED, ...]
editorial_decision=accept|minor_revision|major_revision|reject
```
