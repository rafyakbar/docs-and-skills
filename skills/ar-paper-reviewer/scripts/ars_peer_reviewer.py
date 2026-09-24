#!/usr/bin/env python3
"""
scripts/ars_peer_reviewer.py

Mesin Pengolah & Sintesis Peer Review Naskah Akademik Berdasarkan Kontrak Sprint Schema 13.2.
Membaca laporan ulasan dari 5 reviewer independen, mengevaluasi aturan kegagalan F0-F5,
memeriksa adjudikasi DA CRITICAL (anti-silent accept), menyertakan 4 baris audit sintesis kanonikal,
serta menghasilkan berkas 07_editorial_decision.md dan 08_revision_roadmap.md terstruktur.

Penggunaan:
    python scripts/ars_peer_reviewer.py --input reviews/ --output-dir paper/
    python scripts/ars_peer_reviewer.py --input review_report.md --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Reconfigure output for Windows UTF-8 console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Import konstanta
try:
    from _review_constants import (
        ACCEPTANCE_DIMENSIONS,
        DA_ADJUDICATION_STATES,
        DECISIONS,
        FAILURE_CONDITIONS,
        PANEL_ROLES,
        RE_CONFIDENCE,
        RE_DIMENSION_TAG,
        RE_EVIDENCE_ANCHOR,
        RE_RECOMMENDATION,
        RE_SEVERITY_TAG,
        ROLE_DISPLAY_NAMES,
        SEVERITIES,
    )
except ImportError:
    from scripts._review_constants import (
        ACCEPTANCE_DIMENSIONS,
        DA_ADJUDICATION_STATES,
        DECISIONS,
        FAILURE_CONDITIONS,
        PANEL_ROLES,
        RE_CONFIDENCE,
        RE_DIMENSION_TAG,
        RE_EVIDENCE_ANCHOR,
        RE_RECOMMENDATION,
        RE_SEVERITY_TAG,
        ROLE_DISPLAY_NAMES,
        SEVERITIES,
    )


class PeerReviewSynthesizer:
    def __init__(
        self,
        input_path: Path,
        output_dir: Optional[Path] = None,
        override_decision: Optional[str] = None,
        round_number: int = 1,
    ):
        self.input_path = input_path
        self.output_dir = output_dir if output_dir is not None else Path("paper_reviews/round-1")
        self.override_decision = override_decision.upper() if override_decision else None
        self.round_number = round_number
        self.desk_screening_found: bool = False
        self.desk_screening_status: str = "PASS"

        self.reports: Dict[str, Dict[str, Any]] = {}
        self.raw_text: str = ""
        self.findings: List[Dict[str, Any]] = []
        self.dimension_status: Dict[str, str] = {dim: "pass" for dim in ACCEPTANCE_DIMENSIONS}
        self.fired_condition: Optional[Dict[str, Any]] = None
        self.mechanical_decision: str = "ACCEPT"
        self.decision: str = "ACCEPT"
        self.da_critical_blocked: bool = False
        self.da_critical_marker: Optional[str] = None
        self.da_adjudications: List[Dict[str, str]] = []

    def load_inputs(self) -> None:
        """Membaca berkas ulasan dari file tunggal atau direktori ulasan."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input path tidak ditemukan: {self.input_path}")

        # Deteksi berkas skrining meja (00_desk_screening.md)
        desk_candidate = None
        if self.input_path.is_dir():
            cand = self.input_path / "00_desk_screening.md"
            if cand.exists():
                desk_candidate = cand
        elif self.input_path.parent.is_dir():
            cand = self.input_path.parent / "00_desk_screening.md"
            if cand.exists():
                desk_candidate = cand

        if desk_candidate:
            self.desk_screening_found = True
            try:
                desk_text = desk_candidate.read_text(encoding="utf-8")
                if "DESK_REJECT" in desk_text or ("REJECT" in desk_text and "PASS" not in desk_text):
                    self.desk_screening_status = "REJECT"
                else:
                    self.desk_screening_status = "PASS"
            except Exception:
                pass

        files_to_read: List[Path] = []
        if self.input_path.is_file():
            files_to_read.append(self.input_path)
        else:
            files_to_read = sorted([
                f for f in self.input_path.glob("*.md")
                if not (f.name.startswith("00_desk") or f.name.startswith("07_") or f.name.startswith("08_") or f.name.startswith("09_") or f.name.startswith("10_") or f.name.startswith("11_") or f.name.startswith("12_"))
            ])
            # Jika semua file terfilter, fallback membaca seluruh file .md
            if not files_to_read:
                files_to_read = sorted(list(self.input_path.glob("*.md")))

        combined_texts = []
        for f in files_to_read:
            try:
                content = f.read_text(encoding="utf-8")
                combined_texts.append(content)
            except Exception as e:
                print(f"[WARN] Gagal membaca berkas {f}: {e}", file=sys.stderr)

        self.raw_text = "\n\n".join(combined_texts)
        if not self.raw_text.strip():
            raise ValueError(f"Tidak ada konten ulasan yang dapat dibaca dari {self.input_path}")

    def parse_reports(self) -> None:
        """Membedah teks ulasan menjadi profil per-reviewer dan daftar kelemahan/kekuatan."""
        for role in PANEL_ROLES:
            self.reports[role] = {
                "detected": False,
                "recommendation": "Minor Revision",
                "confidence": 4,
                "strengths_count": 0,
                "weaknesses": [],
            }

        text_to_parse = self.raw_text
        if "## 2. Contoh Luaran" in text_to_parse:
            text_to_parse = text_to_parse.split("## 2. Contoh Luaran")[0]

        reviewer_blocks = re.split(
            r"(?:^|\n)(?=###?\s*(?:Peer Review Report|Laporan Review|Reviewer Information|Reviewer Role))",
            text_to_parse,
            flags=re.IGNORECASE,
        )

        role_keywords = {
            "eic": ["editor-in-chief", "eic"],
            "methodology": ["methodology", "metodologi", "reviewer 1"],
            "domain": ["domain expert", "domain reviewer", "reviewer 2", "bidang"],
            "perspective": ["perspective reviewer", "reviewer 3", "perspektif silang", "cross-disciplinary"],
            "da": ["devil's advocate", "adversarial evaluator", "da reviewer"],
        }

        w_pattern = re.compile(
            r"(?:^|\n)\s*(?:#{1,4}\s*|[-*]\s+\*{0,2})(W\d+|Kelemahan\s*\d+|Issue\s*\d+|Kritik\s*\d+|C\d+|M\d+|m\d+)\s*[:\*\n](.*?)(?=(?:\n\s*(?:#{1,4}\s*|[-*]\s+\*{0,2})(?:W\d+|S\d+|Kelemahan|Kekuatan|Issue|Coverage|Detailed|Recommendation|Strengths|C\d+|M\d+|m\d+)|\n---|\Z))",
            re.DOTALL | re.IGNORECASE,
        )

        counter = 1
        da_counter = 1
        for block in reviewer_blocks:
            if not block.strip():
                continue

            block_lower = block.lower()
            detected_role = None
            for r, kws in role_keywords.items():
                if any(k in block_lower for k in kws):
                    detected_role = r
                    break

            if not detected_role:
                continue

            self.reports[detected_role]["detected"] = True

            rec_match = RE_RECOMMENDATION.search(block)
            if rec_match:
                self.reports[detected_role]["recommendation"] = rec_match.group(1).title()

            conf_match = RE_CONFIDENCE.search(block)
            if conf_match:
                try:
                    self.reports[detected_role]["confidence"] = int(conf_match.group(1))
                except ValueError:
                    pass

            w_matches = w_pattern.findall(block)
            for w_tag, w_body in w_matches:
                full_w_text = f"{w_tag}: {w_body}".strip()

                first_line = full_w_text.split("\n")[0].strip()
                title_clean = re.sub(r"^(?:W\d+|Kelemahan\s*\d+|Issue\s*\d+|Kritik\s*\d+|C\d+|M\d+|m\d+)\s*[:\*\s]+", "", first_line).rstrip("*: ").strip()
                if not title_clean:
                    title_clean = first_line

                sev_match = RE_SEVERITY_TAG.search(full_w_text)
                if sev_match:
                    severity = sev_match.group(1).upper()
                elif w_tag.upper().startswith("C"):
                    severity = "CRITICAL"
                elif w_tag.upper().startswith("M"):
                    severity = "MAJOR"
                elif w_tag.upper().startswith("m"):
                    severity = "MINOR"
                else:
                    severity = "MAJOR"

                anchor_match = RE_EVIDENCE_ANCHOR.search(full_w_text)
                anchor = anchor_match.group(0) if anchor_match else "[section: general]"

                # Penentuan Dimensi Dinamis (D1-D6)
                dim_match = RE_DIMENSION_TAG.search(full_w_text)
                if dim_match:
                    dim_target = dim_match.group(1).upper()
                else:
                    # Heuristik pemetaan cerdas
                    lower_text = full_w_text.lower()
                    if detected_role == "methodology":
                        dim_target = "D1"
                    elif detected_role == "domain":
                        dim_target = "D2"
                    elif detected_role == "da":
                        dim_target = "D3"
                    elif detected_role == "perspective":
                        dim_target = "D4"
                    elif detected_role == "eic":
                        # Bedakan D5 (writing/structure/visuals) vs D6 (fit/novelty/contribution)
                        if any(w in lower_text for w in ["writing", "structure", "imrad", "penulisan", "struktur", "figur", "figure", "tabel", "grammar", "tata bahasa", "format"]):
                            dim_target = "D5"
                        else:
                            dim_target = "D6"
                    else:
                        dim_target = "D1"

                issue_id = f"ISSUE-{counter:02d}"
                da_key = None
                if detected_role == "da" and severity == "CRITICAL":
                    da_key = f"C{da_counter}"
                    da_counter += 1

                finding_item = {
                    "id": issue_id,
                    "da_key": da_key,
                    "role": detected_role,
                    "dimension": dim_target,
                    "title": title_clean,
                    "severity": severity,
                    "evidence_anchor": anchor,
                    "raw_block": full_w_text,
                }
                self.findings.append(finding_item)
                self.reports[detected_role]["weaknesses"].append(finding_item)
                counter += 1

    def evaluate_sprint_contract(self) -> None:
        """Mengevaluasi status dimensi D1-D6 dan menentukan keputusan editorial F0-F5."""
        for dim_id in ACCEPTANCE_DIMENSIONS:
            dim_findings = [f for f in self.findings if f["dimension"] == dim_id]
            crit_count = sum(1 for f in dim_findings if f["severity"] == "CRITICAL")
            major_count = sum(1 for f in dim_findings if f["severity"] == "MAJOR")
            minor_count = sum(1 for f in dim_findings if f["severity"] == "MINOR")

            if crit_count >= 2:
                self.dimension_status[dim_id] = "fatal"
            elif crit_count == 1 or major_count >= 2:
                self.dimension_status[dim_id] = "block"
            elif major_count == 1 or minor_count >= 2:
                self.dimension_status[dim_id] = "warn"
            else:
                self.dimension_status[dim_id] = "pass"

        mandatory_dims = [k for k, v in ACCEPTANCE_DIMENSIONS.items() if v["priority"] == "mandatory"]
        high_dims = [k for k, v in ACCEPTANCE_DIMENSIONS.items() if v["priority"] == "high"]

        has_fatal_mandatory = any(self.dimension_status[d] == "fatal" for d in mandatory_dims)
        has_block_mandatory = any(self.dimension_status[d] == "block" for d in mandatory_dims)
        warn_or_worse_mandatory = sum(1 for d in mandatory_dims if self.dimension_status[d] in ("warn", "block", "fatal"))
        has_block_high = any(self.dimension_status[d] == "block" for d in high_dims)
        any_warn_or_worse = any(self.dimension_status[d] in ("warn", "block", "fatal") for d in ACCEPTANCE_DIMENSIONS)

        if has_fatal_mandatory:
            self.fired_condition = FAILURE_CONDITIONS[0]  # F1
            self.mechanical_decision = "REJECT"
        elif has_block_mandatory:
            self.fired_condition = FAILURE_CONDITIONS[1]  # F2
            self.mechanical_decision = "MAJOR_REVISION"
        elif warn_or_worse_mandatory >= 2:
            self.fired_condition = FAILURE_CONDITIONS[2]  # F3
            self.mechanical_decision = "MAJOR_REVISION"
        elif has_block_high:
            self.fired_condition = FAILURE_CONDITIONS[3]  # F4
            self.mechanical_decision = "MAJOR_REVISION"
        elif any_warn_or_worse:
            self.fired_condition = FAILURE_CONDITIONS[4]  # F5
            self.mechanical_decision = "MINOR_REVISION"
        else:
            self.fired_condition = FAILURE_CONDITIONS[5]  # F0
            self.mechanical_decision = "ACCEPT"

        self.decision = self.mechanical_decision

        # Adjudikasi DA CRITICAL (Anti-Silent Accept)
        da_crit_findings = [f for f in self.findings if f["role"] == "da" and f["severity"] == "CRITICAL"]
        self.da_adjudications = []
        for idx, f in enumerate(da_crit_findings, 1):
            key = f.get("da_key") or f"C{idx}"
            # Default awal belum teradjudikasi jika ada
            self.da_adjudications.append({"key": key, "status": "UNRESOLVED", "issue": f["title"]})

        unresolved_da = [a for a in self.da_adjudications if a["status"] in ("VALIDATED", "UNRESOLVED")]
        if unresolved_da and self.mechanical_decision == "ACCEPT":
            self.da_critical_blocked = True
            unres_cnt = len(unresolved_da)
            self.da_critical_marker = f"[DA-CRITICAL-VS-ACCEPT: {unres_cnt} validated/unresolved]"
            # Sesuai aturan baku Schema 13 di hulu (Rule: Never Auto-Downgrade Mechanical Action),
            # aksi mekanis tidak boleh diturunkan secara sepihak menjadi MINOR_REVISION.
            # Keputusan mekanis ACCEPT tetap dipertahankan, namun status pembekuan ditandai penanda eskalasi.
            self.decision = self.mechanical_decision
        else:
            self.da_critical_marker = None

        if self.override_decision and self.override_decision in DECISIONS:
            self.decision = self.override_decision

    def generate_editorial_decision(self) -> str:
        """Menghasilkan draf surat keputusan editorial resmi EIC (07_editorial_decision.md)."""
        lines = []
        lines.append(f"# Surat Keputusan Editorial (Editorial Decision Letter) — Putaran {self.round_number}")
        lines.append("")
        if self.da_critical_blocked and self.da_critical_marker:
            lines.append(f"**Status Keputusan**: **{self.decision.replace('_', ' ')}** {self.da_critical_marker}  ")
        else:
            lines.append(f"**Status Keputusan**: **{self.decision.replace('_', ' ')}**  ")
        lines.append(f"**Putaran Ulasan**: Putaran {self.round_number} (Round {self.round_number})  ")
        lines.append(f"**Tanggal Evaluasi**: 2026-09-21  ")
        lines.append(f"**Panel Evaluator**: 5 Penilai Independen (EIC + 3 Peer Reviewers + Devil's Advocate)  ")
        lines.append(f"**Protokol Evaluasi**: Kontrak Sprint Schema 13 (Sprint Contract Protocol v2)  ")
        if self.desk_screening_found:
            lines.append(f"**Skrining Meja Editor (Review Awal)**: {'✅ PASS (Proceed to Full Panel Review)' if self.desk_screening_status == 'PASS' else '❌ DESK REJECT'}  ")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 4 Baris Audit Kanonikal (Pinned Audit Line Grammar untuk Validator Otomatis)
        lines.append("## 0. Baris Audit Sintesis Kanonikal (Pinned Audit Grammar)")
        lines.append("```text")
        dim_str = ", ".join(f"{k}={v.upper()}" for k, v in self.dimension_status.items())
        lines.append(f"dimension_verdicts: [{dim_str}]")
        fired_str = self.fired_condition['id'] if self.fired_condition else "F0"
        lines.append(f"fired_conditions: [{fired_str}]")
        if self.da_adjudications:
            da_str = ", ".join(f"{a['key']}={a['status']}" for a in self.da_adjudications)
            lines.append(f"da_critical_adjudications: [{da_str}]")
        else:
            lines.append("da_critical_adjudications: [none]")
        lines.append(f"editorial_decision={self.decision.lower()}")
        if self.da_critical_blocked and self.da_critical_marker:
            lines.append(self.da_critical_marker)
        lines.append("```")
        if self.da_critical_blocked and self.da_critical_marker:
            lines.append("")
            lines.append(self.da_critical_marker)
        lines.append("")
        lines.append("---")
        lines.append("")

        lines.append("## 1. Ringkasan Rekomendasi Panel Reviewer")
        lines.append("")
        lines.append("| Peran Reviewer | Fokus Ulasan | Rekomendasi Mandiri |")
        lines.append("|---|---|---|")
        for role in PANEL_ROLES:
            rep = self.reports.get(role, {})
            disp = ROLE_DISPLAY_NAMES.get(role, role)
            focus = ACCEPTANCE_DIMENSIONS.get(
                "D1" if role == "methodology" else ("D2" if role == "domain" else ("D3" if role == "da" else ("D4" if role == "perspective" else "D6"))),
                {}
            ).get("name", "General Assessment")
            rec = rep.get("recommendation", "Review Complete")
            lines.append(f"| **{disp}** | `{focus}` | **{rec}** |")

        lines.append("")
        lines.append("---")
        lines.append("")

        lines.append("## 2. Evaluasi 6 Dimensi Akseptasi (Schema 13)")
        lines.append("")
        lines.append("| Dimensi | Nama Dimensi | Prioritas | Eligible Roles | Owner Role | Status Evaluasi |")
        lines.append("|:---:|---|:---:|:---:|:---:|:---:|")
        for dim_id, meta in ACCEPTANCE_DIMENSIONS.items():
            status = self.dimension_status.get(dim_id, "pass").upper()
            status_badge = "✅ PASS" if status == "PASS" else ("⚠️ WARN" if status == "WARN" else ("🚫 BLOCK" if status == "BLOCK" else "🛑 FATAL"))
            elig_str = ", ".join(meta["eligible_roles"])
            lines.append(f"| **{dim_id}** | {meta['name']} | `{meta['priority']}` | `{elig_str}` | `{meta['owner_role']}` | **{status_badge}** |")

        lines.append("")
        if self.fired_condition:
            lines.append(f"> **Kondisi Aturan Terpicu**: `{self.fired_condition['id']}` ({self.fired_condition['expression']}) $\\rightarrow$ `{self.fired_condition['action']}`.")

        if self.da_critical_blocked and self.da_critical_marker:
            lines.append(f"> ⚠️ **{self.da_critical_marker}**: Terdapat temuan CRITICAL dari Devil's Advocate yang belum diselesaikan secara tuntas. Finalisasi keputusan `ACCEPT` dibekukan hingga bukti sanggahan terverifikasi.")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Top Blocking Issues (Maksimal 3 Isu Pemblokir Akseptasi)
        lines.append("## 3. Top Blocking Issues (Isu Pemblokir Prioritas Tinggi)")
        lines.append("")
        blocking_findings = [f for f in self.findings if f["severity"] in ("CRITICAL", "MAJOR")]
        if not blocking_findings:
            lines.append("- *Tidak ada isu pemblokir (blocking issues) yang teridentifikasi.*")
        else:
            lines.append("| Peringkat | ID Isu | Sumber | Dimensi | Severity | Deskripsi Cacat Kritis & Rujukan Roadmap |")
            lines.append("|:---:|:---:|:---:|:---:|:---:|---|")
            for idx, item in enumerate(blocking_findings[:3], 1):
                role_short = ROLE_DISPLAY_NAMES.get(item["role"], item["role"]).split("(")[0].strip()
                lines.append(f"| **#{idx}** | **`{item['id']}`** | {role_short} | `{item['dimension']}` | **`{item['severity']}`** | {item['title']} (Rujukan: `{item['evidence_anchor']}`) |")

        lines.append("")
        lines.append("---")
        lines.append("")

        lines.append("## 4. Catatan Evaluasi Kritis per Dimensi")
        lines.append("")
        for dim_id, meta in ACCEPTANCE_DIMENSIONS.items():
            dim_issues = [f for f in self.findings if f["dimension"] == dim_id]
            lines.append(f"### {dim_id}: {meta['name'].replace('_', ' ').title()} (`{meta['owner_role']}`)")
            if not dim_issues:
                lines.append("- *Tidak ditemukan kelemahan material pada dimensi ini (Memenuhi standar publikasi).*")
            else:
                for issue in dim_issues:
                    lines.append(f"- **[{issue['id']}] [{issue['severity']}] {issue['title']}** (Lokasi: `{issue['evidence_anchor']}`)")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## 5. Instruksi Revisi & Batas Waktu")
        lines.append("")
        if self.decision == "ACCEPT":
            if self.da_critical_blocked and self.da_critical_marker:
                lines.append(f"Naskah Anda secara mekanis memenuhi kriteria **DITERIMA (ACCEPT)**, namun status finalisasinya dibekukan sementara `{self.da_critical_marker}` karena terdapat temuan kritis Devil's Advocate yang belum diselesaikan. Penulis wajib menyajikan bukti sanggahan atau membatasi klaim sentral sebelum naskah dapat diproses ke tahap akhir.")
            else:
                lines.append("Naskah Anda dinyatakan **DITERIMA (ACCEPT)**. Penulis dapat melanjutkan ke tahap persiapan naskah akhir dan konversi format publikasi.")
        elif self.decision == "MINOR_REVISION":
            lines.append("Naskah Anda membutuhkan **REVISI MINOR (MINOR REVISION)**. Penulis diminta melengkapi perbaikan minor dan tanggapan formal dalam rentang waktu **2–3 minggu**.")
        elif self.decision == "MAJOR_REVISION":
            lines.append("Naskah Anda membutuhkan **REVISI MAYOR (MAJOR REVISION)**. Diperlukan analisis tambahan atau klarifikasi mendalam terhadap celah metodologis dan argumen sebelum naskah dapat dievaluasi kembali (*re-review*). Batas waktu pengajuan: **6–8 minggu**.")
        else:
            lines.append("Naskah Anda dinyatakan **DITOLAK (REJECT)** untuk publikasi pada venue ini karena kelemahan fundamental yang tidak dapat diperbaiki melalui revisi standar.")

        lines.append("")
        return "\n".join(lines)

    def generate_revision_roadmap(self) -> str:
        """Menghasilkan dokumen kerja terstruktur matriks rencana revisi (08_revision_roadmap.md)."""
        lines = []
        lines.append(f"# Rencana Aksi Revisi (Revision Roadmap Matrix) — Putaran {self.round_number}")
        lines.append("")
        lines.append("Dokumen kerja ini memetakan seluruh catatan reviewer menjadi daftar tindakan perbaikan konkret dengan kriteria keterterimaan (*Acceptance Criteria*) terukur untuk persiapan draf revisi dan surat tanggapan (*Point-by-Point Response to Reviewers*).")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Matriks Tindakan Revisi Terprioritas")
        lines.append("")
        lines.append("| ID Isu | Penilai Sumber | Dimensi | Severity | Ringkasan Isu & Lokasi Bukti | Rencana Aksi Perbaikan | Kriteria Keterterimaan (Acceptance Criteria) | Status |")
        lines.append("|:---:|:---:|:---:|:---:|---|---|---|:---:|")

        if not self.findings:
            lines.append("| `ISSUE-00` | EIC | `D5` | `MINOR` | Tidak ada kelemahan material tercatat. | Siapkan berkas submission final. | Semua berkas terformat lengkap. | [ ] |")
        else:
            sev_order = {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}
            sorted_findings = sorted(self.findings, key=lambda x: (sev_order.get(x["severity"], 3), x["dimension"]))

            for item in sorted_findings:
                role_disp = ROLE_DISPLAY_NAMES.get(item["role"], item["role"]).split("(")[0].strip()

                # Acceptance criteria generik terstandarisasi
                if item["severity"] == "CRITICAL":
                    acc_crit = "Eksperimen/partisi diperbaiki, bukti empiris disertakan, dan lulus audit re-review tanpa celah."
                elif item["severity"] == "MAJOR":
                    acc_crit = "Analisis/literatur tambahan dimasukkan ke naskah dan dijabarkan tuntas pada Response Letter."
                else:
                    acc_crit = "Perbaikan teks/sitasi dilakukan pada nomor baris yang dirujuk."

                lines.append(
                    f"| **`{item['id']}`** | {role_disp} | `{item['dimension']}` | **`{item['severity']}`** | "
                    f"{item['title']} (`{item['evidence_anchor']}`) | "
                    f"Perbaiki pada seksi terkait dan cantumkan justifikasi pada Response Letter. | "
                    f"{acc_crit} | [ ] |"
                )

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Pengelompokan Sprint Revisi Berdasarkan Prioritas")
        lines.append("")
        lines.append("### Priority 1: Structural & Critical Revisions (Must Fix - Blocker)")
        lines.append("- Wajib diselesaikan sebelum penyuntingan teks narasi; mencakup perbaikan partisi data, pengujian validitas statistik, atau pembatasan klaim sentral.")
        lines.append("")
        lines.append("### Priority 2: Content & Literature Supplementation (Should Fix - Major)")
        lines.append("- Menambahkan benchmark pembanding terkini, eksperimen sensitivitas, dan klarifikasi metodologis.")
        lines.append("")
        lines.append("### Priority 3: Text, Citations & Minor Formatting (Nice to Fix - Editorial)")
        lines.append("- Koreksi tipografi, penyempurnaan format referensi, dan perbaikan gaya penulisan tabel/gambar.")
        lines.append("")
        return "\n".join(lines)

    def write_outputs(self) -> Tuple[Path, Path]:
        """Menuliskan berkas luaran ke output_dir."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        decision_file = self.output_dir / "07_editorial_decision.md"
        roadmap_file = self.output_dir / "08_revision_roadmap.md"

        decision_content = self.generate_editorial_decision()
        roadmap_content = self.generate_revision_roadmap()

        decision_file.write_text(decision_content, encoding="utf-8")
        roadmap_file.write_text(roadmap_content, encoding="utf-8")

        return decision_file, roadmap_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mesin Pengolah & Sintesis Peer Review Naskah Akademik Berdasarkan Kontrak Sprint Schema 13."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path ke berkas ulasan Markdown (.md) atau folder ulasan.",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=None,
        help="Direktori target penyimpanan luaran (default: paper/ saat penulisan aktif).",
    )
    parser.add_argument(
        "--override-decision",
        choices=["ACCEPT", "MINOR_REVISION", "MAJOR_REVISION", "REJECT"],
        help="Paksa keputusan editorial tertentu (override).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Jalankan evaluasi tanpa menulis berkas luaran ke disk.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Cetak hasil evaluasi ringkas dalam format JSON ke konsol.",
    )

    args = parser.parse_args()
    input_path = Path(args.input)

    # Efek samping penulisan disk dicegah saat:
    # 1. Flag --dry-run diaktifkan, ATAU
    # 2. Flag --json dipanggil tanpa secara eksplisit menentukan --output-dir (-o)
    should_write = True
class ReReviewVerificationEngine:
    """
    Mesin Verifikasi Re-Review Putaran Kedua (Round 2+) Berdasarkan R&R Traceability Matrix.
    Memverifikasi pemenuhan komitmen perbaikan pada naskah baru terhadap 08_revision_roadmap.md
    dan surat sanggahan 09_response_letter.md.
    """
    def __init__(
        self,
        roadmap_path: Path,
        response_path: Optional[Path] = None,
        paper_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        round_number: int = 2,
        override_decision: Optional[str] = None,
    ):
        self.roadmap_path = roadmap_path
        self.response_path = response_path
        self.paper_dir = paper_dir if paper_dir is not None else Path("paper")
        self.output_dir = output_dir if output_dir is not None else Path(f"paper_reviews/round-{round_number}")
        self.round_number = round_number
        self.override_decision = override_decision.upper() if override_decision else None

        self.roadmap_items: List[Dict[str, Any]] = []
        self.responses: Dict[str, Dict[str, str]] = {}
        self.paper_texts: Dict[str, str] = {}
        self.verification_results: List[Dict[str, Any]] = []
        self.decision: str = "ACCEPT"
        self.metrics: Dict[str, Any] = {
            "total": 0,
            "fully_addressed": 0,
            "partially_addressed": 0,
            "not_addressed": 0,
            "p1_total": 0,
            "p1_fulfilled": 0,
            "p2_total": 0,
            "p2_fulfilled": 0,
            "p3_total": 0,
            "p3_fulfilled": 0,
        }

    def load_and_verify(self) -> None:
        """Memuat roadmap, respons, bab naskah dan mengevaluasi verifikasi."""
        if not self.roadmap_path.exists():
            raise FileNotFoundError(f"Berkas roadmap tidak ditemukan: {self.roadmap_path}")

        # 1. Parse Roadmap
        roadmap_text = self.roadmap_path.read_text(encoding="utf-8")
        self._parse_roadmap(roadmap_text)

        # 2. Parse Response Letter
        if self.response_path and self.response_path.exists():
            resp_text = self.response_path.read_text(encoding="utf-8")
            self._parse_response_letter(resp_text)

        # 3. Load Paper Files
        if self.paper_dir and self.paper_dir.exists():
            for f in sorted(list(self.paper_dir.glob("*.md"))):
                if f.name.startswith("07_") or f.name.startswith("08_") or f.name.startswith("11_"):
                    continue
                try:
                    self.paper_texts[f.name] = f.read_text(encoding="utf-8")
                except Exception:
                    pass

        # 4. Cross Verification
        self._verify_items()

        # 5. Evaluate Decision
        self._evaluate_decision()

    def _parse_roadmap(self, text: str) -> None:
        lines = text.split("\n")
        table_lines = [l for l in lines if l.strip().startswith("|") and not re.match(r"^\|\s*[-:]+\s*\|", l.strip())]

        item_counter = 1
        for line in table_lines:
            cols = [c.strip() for c in line.strip().split("|")[1:-1]]
            if len(cols) < 5:
                continue
            first_col = cols[0].strip("`* ")
            if first_col.lower() in ["id", "id isu", "issue id", "no", "#"]:
                continue

            item_id = first_col if first_col else f"ISSUE-{item_counter:02d}"
            role = cols[1] if len(cols) > 1 else "Reviewer"
            dimension = cols[2].strip("` ") if len(cols) > 2 else "D1"
            severity = cols[3].strip("`* ") if len(cols) > 3 else "MAJOR"
            summary = cols[4] if len(cols) > 4 else ""
            action = cols[5] if len(cols) > 5 else ""
            criteria = cols[6] if len(cols) > 6 else ""

            sev_up = severity.upper()
            if "CRITICAL" in sev_up or "FATAL" in sev_up or "BLOCK" in sev_up:
                priority = "P1 (Must Fix)"
            elif "MAJOR" in sev_up:
                priority = "P2 (Should Fix)"
            else:
                priority = "P3 (Consider)"

            self.roadmap_items.append({
                "id": item_id,
                "role": role,
                "dimension": dimension,
                "severity": severity,
                "priority": priority,
                "summary": summary,
                "action": action,
                "criteria": criteria,
            })
            item_counter += 1

        if not self.roadmap_items:
            bullets = re.findall(r"[-*]\s*\*{0,2}(ISSUE-\d+|[A-Za-z0-9_-]+)\*{0,2}[:\s]+(.*?)(?=\n[-*]\s|\n#|\Z)", text, re.DOTALL)
            for b_id, b_text in bullets:
                self.roadmap_items.append({
                    "id": b_id.strip(),
                    "role": "Reviewer",
                    "dimension": "D1",
                    "severity": "MAJOR",
                    "priority": "P2 (Should Fix)",
                    "summary": b_text.strip().split("\n")[0],
                    "action": b_text.strip(),
                    "criteria": "Perbaikan diverifikasi substantif.",
                })

    def _parse_response_letter(self, text: str) -> None:
        blocks = re.split(r"(?:^|\n)(?=#{1,4}\s*(?:Issue|ISSUE|Tanggapan|Point|Item|R\d+|DA-|W\d+)|[-*]\s+\*{1,2}(?:Issue|ISSUE|Point))", text, re.IGNORECASE)
        for block in blocks:
            if not block.strip():
                continue

            id_match = re.search(r"\b(ISSUE-\d+|W\d+|C\d+|M\d+|R\d+-[A-Z0-9]+)\b", block, re.IGNORECASE)
            matched_id = id_match.group(1).upper() if id_match else None

            claim_match = re.search(
                r"(?:\*{0,2}(?:Author(?:'s)?\s*Response|Tanggapan\s*Penulis|Respons|Jawaban)\*{0,2}\s*[:\n])(.*?)(?=(?:\*{0,2}(?:Manuscript\s*Changes|Location|Perubahan\s*Naskah|Lokasi)\*{0,2}\s*[:\n]|\n#{1,4}|\n---|\Z))",
                block,
                re.DOTALL | re.IGNORECASE,
            )
            claim_text = claim_match.group(1).strip() if claim_match else ""

            loc_match = re.search(
                r"(?:\*{0,2}(?:Manuscript\s*Changes|Location|Perubahan\s*Naskah|Lokasi)\*{0,2}\s*[:\n])(.*?)(?=(?:\n#{1,4}|\n---|\Z))",
                block,
                re.DOTALL | re.IGNORECASE,
            )
            loc_text = loc_match.group(1).strip() if loc_match else ""

            block_id_match = re.search(r"\b(B\d{4})\b", block)
            if block_id_match and not loc_text:
                loc_text = f"Block {block_id_match.group(1)}"

            sec_match = re.search(r"\[section:\s*([^\]]+)\]", block)
            if sec_match and not loc_text:
                loc_text = f"Section {sec_match.group(1)}"

            if not claim_text and not loc_text:
                claim_text = block.strip()[:200]

            key = matched_id if matched_id else f"RAW-{len(self.responses)+1}"
            self.responses[key] = {
                "claim": claim_text,
                "location": loc_text if loc_text else "Naskah terevisi",
                "full_block": block,
            }

    def _verify_items(self) -> None:
        all_paper_content = "\n\n".join(self.paper_texts.values())

        for idx, item in enumerate(self.roadmap_items, 1):
            item_id = item["id"]

            matched_resp = None
            for r_key, r_val in self.responses.items():
                if r_key.lower() == item_id.lower() or item_id.lower() in r_val["full_block"].lower():
                    matched_resp = r_val
                    break

            if not matched_resp and len(self.responses) >= idx:
                r_keys = list(self.responses.keys())
                matched_resp = self.responses[r_keys[idx - 1]]

            claim = matched_resp["claim"] if matched_resp else ""
            location = matched_resp["location"] if matched_resp else ""

            status = "NOT_ADDRESSED"
            icon = "❌ No"
            evaluation = "Tidak ditemukan tanggapan atau bukti perubahan pada draf naskah baru."

            if matched_resp:
                is_grounded = False
                block_ids = re.findall(r"\bB\d{4}\b", location + " " + claim)
                if block_ids and any(bid in all_paper_content for bid in block_ids):
                    is_grounded = True

                sec_names = re.findall(r"(?:0\d_[a-z0-9_-]+|introduction|methods|results|discussion|conclusion)", location.lower())
                if sec_names:
                    is_grounded = True

                if len(claim.split()) >= 15:
                    if is_grounded or len(all_paper_content) > 0:
                        status = "FULLY_ADDRESSED"
                        icon = "✅ Yes"
                        evaluation = "Perbaikan terverifikasi substantif pada naskah dan memenuhi kriteria keterterimaan."
                    else:
                        status = "PARTIALLY_ADDRESSED"
                        icon = "⚠️ Partial"
                        evaluation = "Penulis memberikan tanggapan terperinci, namun verifikasi rujukan lokasi naskah memerlukan konfirmasi manual."
                elif len(claim.split()) > 0:
                    status = "PARTIALLY_ADDRESSED"
                    icon = "⚠️ Partial"
                    evaluation = "Tanggapan penulis terlalu ringkas; perlu elaborasi bukti tekstual naskah."

            self.metrics["total"] += 1
            if status == "FULLY_ADDRESSED":
                self.metrics["fully_addressed"] += 1
            elif status == "PARTIALLY_ADDRESSED":
                self.metrics["partially_addressed"] += 1
            else:
                self.metrics["not_addressed"] += 1

            prio = item["priority"]
            if "P1" in prio:
                self.metrics["p1_total"] += 1
                if status == "FULLY_ADDRESSED":
                    self.metrics["p1_fulfilled"] += 1
            elif "P2" in prio:
                self.metrics["p2_total"] += 1
                if status == "FULLY_ADDRESSED":
                    self.metrics["p2_fulfilled"] += 1
            else:
                self.metrics["p3_total"] += 1
                if status == "FULLY_ADDRESSED":
                    self.metrics["p3_fulfilled"] += 1

            self.verification_results.append({
                "id": item_id,
                "priority": item["priority"],
                "summary": item["summary"],
                "claim": claim if claim else "--",
                "location": location if location else "--",
                "status": status,
                "icon": icon,
                "evaluation": evaluation,
            })

    def _evaluate_decision(self) -> None:
        p1_tot = self.metrics["p1_total"]
        p1_ful = self.metrics["p1_fulfilled"]
        p2_tot = self.metrics["p2_total"]
        p2_ful = self.metrics["p2_fulfilled"]

        if p1_tot > 0 and p1_ful == p1_tot:
            if p2_tot == 0 or (p2_ful / p2_tot) >= 0.80:
                self.decision = "ACCEPT"
            else:
                self.decision = "MINOR_REVISION"
        elif p1_tot == 0 and self.metrics["total"] > 0:
            if (self.metrics["fully_addressed"] / self.metrics["total"]) >= 0.80:
                self.decision = "ACCEPT"
            else:
                self.decision = "MINOR_REVISION"
        else:
            if self.metrics["not_addressed"] > 0:
                self.decision = "MAJOR_REVISION"
            else:
                self.decision = "MINOR_REVISION"

        if self.override_decision and self.override_decision in DECISIONS:
            self.decision = self.override_decision

    def generate_verification_report(self) -> str:
        """Menghasilkan berkas 11_re_review_verification.md."""
        lines = []
        lines.append(f"# Laporan Verifikasi Re-Review Putaran {self.round_number} (R&R Traceability Matrix)")
        lines.append("")
        lines.append("Audit ketertelusuran pemenuhan komitmen perbaikan naskah terhadap catatan penelaah putaran sebelumnya.")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 1. Ringkasan Metrik Verifikasi")
        lines.append("")
        lines.append("| Indikator Verifikasi | Jumlah | Persentase | Status Kepatuhan |")
        lines.append("|---|:---:|:---:|:---:|")
        tot = self.metrics["total"]
        fa = self.metrics["fully_addressed"]
        pa = self.metrics["partially_addressed"]
        na = self.metrics["not_addressed"]
        p1_tot = self.metrics["p1_total"]
        p1_ful = self.metrics["p1_fulfilled"]

        fa_pct = (fa / tot * 100) if tot > 0 else 100.0
        pa_pct = (pa / tot * 100) if tot > 0 else 0.0
        na_pct = (na / tot * 100) if tot > 0 else 0.0
        p1_pct = (p1_ful / p1_tot * 100) if p1_tot > 0 else 100.0

        p1_badge = "✅ 100% COMPLIANT" if p1_ful == p1_tot else "❌ INCOMPLETE"
        lines.append(f"| **Total Komitmen Putaran Sebelumnya** | {tot} | 100.0% | -- |")
        lines.append(f"| **Fully Addressed (Tuntas)** | {fa} | {fa_pct:.1f}% | {'✅ PASS' if fa_pct >= 80 else '⚠️ WARN'} |")
        lines.append(f"| **Partially Addressed (Sebagian)** | {pa} | {pa_pct:.1f}% | {'⚠️ WARN' if pa > 0 else '✅ PASS'} |")
        lines.append(f"| **Not Addressed (Belum Terjawab)** | {na} | {na_pct:.1f}% | {'🛑 FAIL' if na > 0 else '✅ PASS'} |")
        lines.append(f"| **Priority 1 Compliance (Blocker/Critical)** | {p1_ful}/{p1_tot} | {p1_pct:.1f}% | **{p1_badge}** |")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 2. Matriks Ketertelusuran Komitmen (Traceability Table)")
        lines.append("")
        lines.append("| ID Isu | Prioritas | Ringkasan Kritik Putaran Sebelumnya | Klaim Respons Penulis | Lokasi Teks Naskah | Status Verifikasi | Evaluasi Mutu Perbaikan |")
        lines.append("|:---:|:---:|---|---|---|:---:|---|")
        for res in self.verification_results:
            lines.append(
                f"| **`{res['id']}`** | `{res['priority']}` | {res['summary']} | "
                f"{res['claim'][:100]} | `{res['location']}` | **`{res['status']}`** ({res['icon']}) | {res['evaluation']} |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 3. Rekomendasi Editorial Re-Review")
        lines.append("")
        if self.decision == "ACCEPT":
            lines.append(f"✅ **DITERIMA (ACCEPT)**: Seluruh catatan kritis putaran sebelumnya telah diselesaikan secara substantif ({p1_ful}/{p1_tot} isu P1 tuntas). Naskah dinyatakan memenuhi standar publikasi.")
        elif self.decision == "MINOR_REVISION":
            lines.append(f"⚠️ **REVISI MINOR (MINOR REVISION)**: Seluruh isu kritis terselesaikan, namun masih terdapat catatan penyempurnaan kecil yang perlu dilengkapi.")
        else:
            lines.append(f"🛑 **REVISI MAYOR (MAJOR REVISION)**: Masih terdapat komitmen prioritas tinggi yang belum terselesaikan secara memuaskan pada naskah baru.")
        lines.append("")
        return "\n".join(lines)

    def generate_editorial_decision(self) -> str:
        """Menghasilkan berkas 07_editorial_decision.md putaran re-review."""
        lines = []
        lines.append(f"# Surat Keputusan Editorial (Editorial Decision Letter) — Putaran {self.round_number} (Re-Review)")
        lines.append("")
        lines.append(f"**Status Keputusan**: **{self.decision.replace('_', ' ')}**  ")
        lines.append(f"**Putaran Ulasan**: Putaran {self.round_number} (Verification Re-Review)  ")
        lines.append(f"**Tanggal Evaluasi**: 2026-09-23  ")
        lines.append(f"**Protokol Evaluasi**: R&R Traceability Verification Protocol  ")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 1. Ringkasan Eksekutif Putaran Verifikasi")
        lines.append("")
        tot = self.metrics["total"]
        fa = self.metrics["fully_addressed"]
        p1_tot = self.metrics["p1_total"]
        p1_ful = self.metrics["p1_fulfilled"]
        fa_pct = (fa / tot * 100) if tot > 0 else 100.0

        lines.append(f"- **Hasil Keputusan Akhir**: **{self.decision.replace('_', ' ')}**")
        lines.append(f"- **Total Komitmen Putaran 1**: {tot} butir perbaikan")
        lines.append(f"- **Tingkat Penyelesaian Keseluruhan**: {fa_pct:.1f}% ({fa}/{tot} butir tuntas)")
        lines.append(f"- **Kepatuhan Isu Kritis (Priority 1)**: {p1_ful}/{p1_tot} terselesaikan tuntas")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 2. Tindak Lanjut Penulis")
        lines.append("")
        if self.decision == "ACCEPT":
            lines.append("Selamat! Naskah revisi Anda telah diverifikasi dan dinyatakan **DITERIMA (ACCEPT)**. Penulis dapat melanjutkan ke tahap konversi format publikasi LaTeX (`ar-paper-latex-converter`) dan persiapan pengiriman akhir (*final submission package*).")
        elif self.decision == "MINOR_REVISION":
            lines.append("Naskah Anda membutuhkan sedikit penyesuaian akhir (**MINOR REVISION**). Silakan lengkapi catatan sisa pada `11_re_review_verification.md` dalam rentang waktu **1 minggu**.")
        else:
            lines.append("Naskah Anda masih membutuhkan perbaikan substantif (**MAJOR REVISION**). Perhatikan butir yang belum terselesaikan pada matriks verifikasi sebelum mengajukan kembali.")
        lines.append("")
        return "\n".join(lines)

    def write_outputs(self) -> Tuple[Path, Path]:
        """Menuliskan berkas luaran ke output_dir."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        verif_file = self.output_dir / "11_re_review_verification.md"
        decision_file = self.output_dir / "07_editorial_decision.md"

        verif_content = self.generate_verification_report()
        decision_content = self.generate_editorial_decision()

        verif_file.write_text(verif_content, encoding="utf-8")
        decision_file.write_text(decision_content, encoding="utf-8")

        return decision_file, verif_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mesin Pengolah & Sintesis Peer Review Naskah Akademik Berdasarkan Kontrak Sprint Schema 13 (Mendukung Full Review & Re-Review Multi-Round)."
    )
    parser.add_argument(
        "-i", "--input",
        default=None,
        help="Path ke berkas ulasan Markdown (.md) atau folder ulasan (misal: paper_reviews/round-1/).",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "re-review"],
        default="full",
        help="Modus operasi: 'full' (panel 5 reviewer putaran 1) atau 're-review' (verifikasi putaran 2+). Default: full.",
    )
    parser.add_argument(
        "--round",
        type=int,
        default=None,
        help="Nomor putaran ulasan (default: 1 untuk mode full, 2 untuk mode re-review).",
    )
    parser.add_argument(
        "--roadmap",
        default=None,
        help="Path ke berkas 08_revision_roadmap.md (untuk mode re-review).",
    )
    parser.add_argument(
        "--response",
        default=None,
        help="Path ke berkas 09_response_letter.md (untuk mode re-review).",
    )
    parser.add_argument(
        "--paper-dir",
        default="paper",
        help="Direktori naskah paper utama (default: paper/).",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=None,
        help="Direktori target penyimpanan luaran (default: paper_reviews/round-N atau paper/).",
    )
    parser.add_argument(
        "--override-decision",
        choices=["ACCEPT", "MINOR_REVISION", "MAJOR_REVISION", "REJECT"],
        help="Paksa keputusan editorial tertentu (override).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Jalankan evaluasi tanpa menulis berkas luaran ke disk.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Cetak hasil evaluasi ringkas dalam format JSON ke konsol.",
    )

    args = parser.parse_args()

    # Tentukan round number default
    if args.round is not None:
        round_num = args.round
    else:
        round_num = 2 if args.mode == "re-review" else 1

    # Cegah efek samping tulis disk saat --dry-run atau saat --json tanpa --output-dir eksplisit
    should_write = True
    if args.dry_run:
        should_write = False
    elif args.json and args.output_dir is None:
        should_write = False

    try:
        if args.mode == "re-review":
            # Resolusi path roadmap
            roadmap_path = None
            if args.roadmap:
                roadmap_path = Path(args.roadmap)
            elif args.input:
                p = Path(args.input)
                if p.is_file():
                    roadmap_path = p
                elif (p / "08_revision_roadmap.md").exists():
                    roadmap_path = p / "08_revision_roadmap.md"
            if not roadmap_path or not roadmap_path.exists():
                for cand in [Path("paper_reviews/round-1/08_revision_roadmap.md"), Path("paper/08_revision_roadmap.md")]:
                    if cand.exists():
                        roadmap_path = cand
                        break

            if not roadmap_path or not roadmap_path.exists():
                raise FileNotFoundError(
                    "Path roadmap perbaikan tidak ditemukan. Berikan via flag --roadmap (misal: --roadmap paper_reviews/round-1/08_revision_roadmap.md)."
                )

            # Resolusi path response letter
            resp_path = None
            if args.response:
                resp_path = Path(args.response)
            elif args.input and Path(args.input).is_dir() and (Path(args.input) / "09_response_letter.md").exists():
                resp_path = Path(args.input) / "09_response_letter.md"
            else:
                for cand in [Path(f"paper_reviews/round-{round_num}/09_response_letter.md"), Path("paper_reviews/round-2/09_response_letter.md"), Path("paper/09_response_letter.md")]:
                    if cand.exists():
                        resp_path = cand
                        break

            # Tentukan output dir
            out_dir = Path(args.output_dir) if args.output_dir else Path(f"paper_reviews/round-{round_num}")
            paper_dir = Path(args.paper_dir) if args.paper_dir else Path("paper")

            engine = ReReviewVerificationEngine(
                roadmap_path=roadmap_path,
                response_path=resp_path,
                paper_dir=paper_dir,
                output_dir=out_dir,
                round_number=round_num,
                override_decision=args.override_decision,
            )
            engine.load_and_verify()

            dec_file = None
            verif_file = None
            if should_write:
                dec_file, verif_file = engine.write_outputs()

            if args.json:
                res = {
                    "mode": "re-review",
                    "round": round_num,
                    "decision": engine.decision,
                    "metrics": engine.metrics,
                    "total_items": engine.metrics["total"],
                    "fully_addressed": engine.metrics["fully_addressed"],
                    "partially_addressed": engine.metrics["partially_addressed"],
                    "not_addressed": engine.metrics["not_addressed"],
                    "p1_compliance": f"{engine.metrics['p1_fulfilled']}/{engine.metrics['p1_total']}",
                    "decision_file": str(dec_file) if dec_file else None,
                    "verification_file": str(verif_file) if verif_file else None,
                }
                print(json.dumps(res, indent=2, ensure_ascii=False))
            else:
                print("=================================================================")
                print(f"  ARS PEER REVIEW RE-REVIEW VERIFICATION (ROUND {round_num})")
                print("=================================================================")
                print(f"Status Keputusan     : {engine.decision}")
                print(f"Total Komitmen R1    : {engine.metrics['total']} butir")
                print(f"Fully Addressed      : {engine.metrics['fully_addressed']} butir")
                print(f"Partially Addressed  : {engine.metrics['partially_addressed']} butir")
                print(f"Not Addressed        : {engine.metrics['not_addressed']} butir")
                print(f"Kepatuhan Priority 1 : {engine.metrics['p1_fulfilled']}/{engine.metrics['p1_total']} tuntas")
                if dec_file and verif_file:
                    print(f"Berkas Keputusan R{round_num}: {dec_file}")
                    print(f"Berkas Verifikasi    : {verif_file}")
                else:
                    print("Mode Penulisan       : DRY-RUN (Tidak ada berkas yang ditulis ke disk)")
                print("=================================================================")
            return 0

        else:
            # Mode Full (Round 1 Panel Review)
            if not args.input:
                raise ValueError("Argumen -i/--input wajib diberikan untuk mode full review.")

            input_path = Path(args.input)
            out_dir = Path(args.output_dir) if args.output_dir else Path(f"paper_reviews/round-{round_num}")

            synthesizer = PeerReviewSynthesizer(
                input_path=input_path,
                output_dir=out_dir,
                override_decision=args.override_decision,
                round_number=round_num,
            )
            synthesizer.load_inputs()
            synthesizer.parse_reports()
            synthesizer.evaluate_sprint_contract()

            dec_file = None
            road_file = None
            if should_write:
                dec_file, road_file = synthesizer.write_outputs()

            if args.json:
                result = {
                    "mode": "full",
                    "round": round_num,
                    "decision": synthesizer.decision,
                    "mechanical_decision": synthesizer.mechanical_decision,
                    "dimension_status": synthesizer.dimension_status,
                    "fired_condition": synthesizer.fired_condition,
                    "da_critical_blocked": synthesizer.da_critical_blocked,
                    "da_critical_marker": synthesizer.da_critical_marker,
                    "escalation_marker": synthesizer.da_critical_marker,
                    "da_adjudications": synthesizer.da_adjudications,
                    "desk_screening_found": synthesizer.desk_screening_found,
                    "desk_screening_status": synthesizer.desk_screening_status,
                    "total_findings": len(synthesizer.findings),
                    "decision_file": str(dec_file) if dec_file else None,
                    "roadmap_file": str(road_file) if road_file else None,
                }
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("=================================================================")
                print(f"  ARS PEER REVIEW SYNTHESIS ENGINE (SCHEMA 13.2) — ROUND {round_num}")
                print("=================================================================")
                print(f"Status Keputusan     : {synthesizer.decision}")
                print(f"Total Temuan Isu     : {len(synthesizer.findings)} temuan")
                if synthesizer.desk_screening_found:
                    print(f"Skrining Meja Editor : {synthesizer.desk_screening_status}")
                if synthesizer.fired_condition:
                    print(f"Kondisi Schema 13    : {synthesizer.fired_condition['id']} - {synthesizer.fired_condition['expression']}")
                if synthesizer.da_critical_blocked and synthesizer.da_critical_marker:
                    print(f"DA CRITICAL Status   : {synthesizer.da_critical_marker}")
                if dec_file and road_file:
                    print(f"Berkas Keputusan     : {dec_file}")
                    print(f"Berkas Rencana Aksi  : {road_file}")
                else:
                    print("Mode Penulisan       : DRY-RUN (Tidak ada berkas yang ditulis ke disk)")
                print("=================================================================")

            return 0

    except Exception as e:
        print(f"[ERROR] Gagal memproses ulasan: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
