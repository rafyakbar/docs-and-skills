# Paket Eksekusi Revisi Naskah Ilmiah (Sample Revision Execution Package)

Dokumen ini menyajikan contoh konkret paket eksekusi revisi naskah akademik secara *end-to-end* yang memenuhi seluruh persyaratan **ARS Spec #390 & #424**, **Schema 8**, dan **Schema 11**.

---

## 1. Draf Naskah Dasar Berjangkar (`paper/01_introduction.md`)

```markdown
<!--block:B0001-->
# 1. Introduction

<!--block:B0002-->
Facial demographic classification, encompassing race and gender categorization from unconstrained facial images, serves as a cornerstone for affective computing, human-computer interaction, and demographic-aware biometric authentication systems [[1]](06_references.md#ref1). Despite substantial advancements driven by deep convolutional neural networks (CNNs), prevailing models continue to exhibit acute performance disparities across disparate ethnic cohorts [[2]](06_references.md#ref2).

<!--block:B0003-->
Prior approaches attempted to resolve this discrepancy predominantly through data augmentation or class re-balancing loss functions. However, these techniques frequently lead to catastrophic forgetting on underrepresented sub-populations, failing to capture cross-domain facial geometries effectively.

<!--block:B0004-->
To overcome these limitations, this paper proposes a Multi-Domain Vision Transformer (MD-ViT) architecture that integrates domain-invariant feature adapters. The remainder of this paper is structured as follows: Section 2 surveys related literature; Section 3 details the proposed methodology; Section 4 presents experimental evaluations; and Section 5 concludes the work.
```

---

## 2. Berkas Manifest Blok (`paper/01_introduction.md.block-manifest.json`)

Diterbitkan secara mekanis oleh `ars_anchorize_draft.py`:

```json
{
  "manifest_format_version": "1.0",
  "base_draft_hash": "e7c2a49b81d3",
  "blocks": [
    {
      "block_id": "B0001",
      "old_hash": "2c9f4d1e8a0b",
      "first_line_excerpt": "# 1. Introduction"
    },
    {
      "block_id": "B0002",
      "old_hash": "b5e8c3a1d9f2",
      "first_line_excerpt": "Facial demographic classification, encompassing race and gender categorization..."
    },
    {
      "block_id": "B0003",
      "old_hash": "7d1a4c9e2f80",
      "first_line_excerpt": "Prior approaches attempted to resolve this discrepancy predominantly through..."
    },
    {
      "block_id": "B0004",
      "old_hash": "a8f3b0c6e4d1",
      "first_line_excerpt": "To overcome these limitations, this paper proposes a Multi-Domain Vision Transformer..."
    }
  ]
}
```

---

## 3. Dokumen Patch Revisi (`paper/revisions/patch_round1.json`)

Disusun oleh agen penulis untuk menjawab catatan Reviewer 1 (minta penjelasan kesenjangan riset lebih tajam) dan Reviewer 2 (minta penegasan kontribusi ilmiah):

```json
{
  "patch_format_version": "1.0",
  "revision_round": 1,
  "base_draft_hash": "e7c2a49b81d3",
  "emitted_by": "draft_writer_agent",
  "ops": [
    {
      "op": "replace_block",
      "block_id": "B0003",
      "old_hash": "7d1a4c9e2f80",
      "new_text": "Prior approaches attempted to resolve this discrepancy predominantly through data augmentation or class re-balancing loss functions [[3]](06_references.md#ref3). However, these techniques frequently induce catastrophic forgetting on underrepresented sub-populations, failing to capture subtle cross-domain facial geometries across varying lighting conditions and sensor types. Crucially, existing Vision Transformer baselines lack explicit parameter-efficient domain adaptation mechanisms tailored to demographic fairness.",
      "roadmap_item_ids": ["REV-001"]
    },
    {
      "op": "insert_after",
      "block_id": "B0003",
      "old_hash": "7d1a4c9e2f80",
      "new_text": "In this context, the primary research gap lies in the absence of unified attention routing that decouples demographic-invariant morphological representations from domain-specific lighting and acquisition variations.",
      "roadmap_item_ids": ["REV-001", "REV-002"]
    }
  ]
}
```

---

## 4. Draf Hasil Revisi (`paper/01_introduction.rev1.md`)

Diterbitkan secara deterministik oleh `ars_apply_revision_patch.py`:

```markdown
<!--block:B0001-->
# 1. Introduction

<!--block:B0002-->
Facial demographic classification, encompassing race and gender categorization from unconstrained facial images, serves as a cornerstone for affective computing, human-computer interaction, and demographic-aware biometric authentication systems [[1]](06_references.md#ref1). Despite substantial advancements driven by deep convolutional neural networks (CNNs), prevailing models continue to exhibit acute performance disparities across disparate ethnic cohorts [[2]](06_references.md#ref2).

<!--block:B0003-->
Prior approaches attempted to resolve this discrepancy predominantly through data augmentation or class re-balancing loss functions [[3]](06_references.md#ref3). However, these techniques frequently induce catastrophic forgetting on underrepresented sub-populations, failing to capture subtle cross-domain facial geometries across varying lighting conditions and sensor types. Crucially, existing Vision Transformer baselines lack explicit parameter-efficient domain adaptation mechanisms tailored to demographic fairness.

<!--block:B0005-->
In this context, the primary research gap lies in the absence of unified attention routing that decouples demographic-invariant morphological representations from domain-specific lighting and acquisition variations.

<!--block:B0004-->
To overcome these limitations, this paper proposes a Multi-Domain Vision Transformer (MD-ViT) architecture that integrates domain-invariant feature adapters. The remainder of this paper is structured as follows: Section 2 surveys related literature; Section 3 details the proposed methodology; Section 4 presents experimental evaluations; and Section 5 concludes the work.
```

*(Catatan: Blok B0001, B0002, dan B0004 identik byte-per-byte dengan berkas aslinya; blok baru disisipkan dengan ID segar B0005).*

---

## 5. Laporan Eksekusi Patch Sidecar (`paper/01_introduction.rev1.md.apply-report.json`)

```json
{
  "report_format_version": "1.2",
  "mode": "patch",
  "base_path": "paper/01_introduction.md",
  "output_path": "paper/01_introduction.rev1.md",
  "base_draft_hash": "e7c2a49b81d3",
  "output_draft_hash": "9f1c3e5a7b2d",
  "patch_digest": "3a8d9b1c7e4f0a2d5e8b6c4f1a9e3d7b5a8c2e1f4d9b6c3a0e7f2b5d8a1c4e9f",
  "revision_round": 1,
  "ops_applied": [
    {
      "op_index": 0,
      "op": "replace_block",
      "block_id": "B0003",
      "roadmap_item_ids": ["REV-001"],
      "new_block_ids": []
    },
    {
      "op_index": 1,
      "op": "insert_after",
      "block_id": "B0003",
      "roadmap_item_ids": ["REV-001", "REV-002"],
      "new_block_ids": ["B0005"]
    }
  ],
  "fresh_block_ids": ["B0005"],
  "pure_move_pairs": [],
  "structural_flags": {
    "heading_op_indexes": [],
    "section_count_delta": 0,
    "touched_ratio": 0.25,
    "touched_ratio_threshold": 0.6,
    "touched_ratio_exceeded": false,
    "any": false,
    "acknowledged": false
  },
  "counters": {
    "blocks_total": 4,
    "blocks_touched": 1,
    "blocks_preserved_byte_identical": 3,
    "preserved_ratio": 0.75
  }
}
```

---

## 6. Surat Tanggapan Reviewer (Schema 8 — `09_response_to_reviewers.md`)

```markdown
# Point-by-Point Response to Reviewers — Round 1

**Manuscript Title:** Multi-Domain Vision Transformer for Fair Facial Demographic Classification  
**Revision Round:** 1  
**Summary of Changes:** Successfully addressed all reviewer comments. Added explicit research gap framing and parameter-efficient domain adaptation motivation in Section 1.  
**Word Count Delta:** +52 words  
**New References Added:** 1  

---

### Response to Reviewer 1

#### REV-001 (R1 — Minor Comment, must_fix)
**Reviewer Comment:**  
> "The transition between the problem formulation and the proposed Vision Transformer architecture in the Introduction feels abrupt. The authors should explicitly delineate the research gap regarding why existing ViT models fail in cross-domain fairness."

**Status:** `RESOLVED`

**Author Response:**  
We express our sincere gratitude to Reviewer 1 for this constructive recommendation. We agree that the architectural motivation required sharper framing. In the revised manuscript, we have expanded Paragraph 3 and introduced a dedicated transition sentence clarifying that standard ViTs lack parameter-efficient mechanisms to disentangle morphological demographic features from environmental acquisition variations.

**Changes Made:**  
- Expanded Paragraph 3 with ViT domain adaptation limitations.
- Inserted a new paragraph explicitly defining the attention routing research gap.
- Location: `paper/01_introduction.md`, Section 1, Paragraphs 3 & 4.
- **Change Block IDs:** `B0003`, `B0005` (verified via `apply-report.json`).
```
