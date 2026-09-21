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
    def __init__(self, input_path: Path, output_dir: Path, override_decision: Optional[str] = None):
        self.input_path = input_path
        self.output_dir = output_dir
        self.override_decision = override_decision.upper() if override_decision else None

        self.reports: Dict[str, Dict[str, Any]] = {}
        self.raw_text: str = ""
        self.findings: List[Dict[str, Any]] = []
        self.dimension_status: Dict[str, str] = {dim: "pass" for dim in ACCEPTANCE_DIMENSIONS}
        self.fired_condition: Optional[Dict[str, Any]] = None
        self.mechanical_decision: str = "ACCEPT"
        self.decision: str = "ACCEPT"
        self.da_critical_blocked: bool = False
        self.da_adjudications: List[Dict[str, str]] = []

    def load_inputs(self) -> None:
        """Membaca berkas ulasan dari file tunggal atau direktori ulasan."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input path tidak ditemukan: {self.input_path}")

        files_to_read: List[Path] = []
        if self.input_path.is_file():
            files_to_read.append(self.input_path)
        else:
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
            # Jangan ubah mechanical action secara sepihak, tetapi tandai status eskalasi tertahan
            self.decision = "MINOR_REVISION"

        if self.override_decision and self.override_decision in DECISIONS:
            self.decision = self.override_decision

    def generate_editorial_decision(self) -> str:
        """Menghasilkan draf surat keputusan editorial resmi EIC (07_editorial_decision.md)."""
        lines = []
        lines.append("# Surat Keputusan Editorial (Editorial Decision Letter)")
        lines.append("")
        lines.append(f"**Status Keputusan**: **{self.decision.replace('_', ' ')}**  ")
        lines.append(f"**Tanggal Evaluasi**: 2026-09-21  ")
        lines.append(f"**Panel Evaluator**: 5 Penilai Independen (EIC + 3 Peer Reviewers + Devil's Advocate)  ")
        lines.append(f"**Protokol Evaluasi**: Kontrak Sprint Schema 13 (Sprint Contract Protocol v2)  ")
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
        lines.append("```")
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

        if self.da_critical_blocked:
            unres_cnt = len([a for a in self.da_adjudications if a["status"] in ("VALIDATED", "UNRESOLVED")])
            lines.append(f"> ⚠️ **[DA-CRITICAL-VS-ACCEPT: {unres_cnt} validated/unresolved]**: Terdapat temuan CRITICAL dari Devil's Advocate yang belum diselesaikan secara tuntas. Keputusan `ACCEPT` ditangguhkan menjadi `MINOR REVISION` hingga bukti sanggahan terverifikasi.")

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
        lines.append("# Rencana Aksi Revisi (Revision Roadmap Matrix)")
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
        default="paper",
        help="Direktori target penyimpanan luaran (default: paper/).",
    )
    parser.add_argument(
        "--override-decision",
        choices=["ACCEPT", "MINOR_REVISION", "MAJOR_REVISION", "REJECT"],
        help="Paksa keputusan editorial tertentu (override).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Cetak hasil evaluasi ringkas dalam format JSON ke konsol.",
    )

    args = parser.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    try:
        synthesizer = PeerReviewSynthesizer(
            input_path=input_path,
            output_dir=output_dir,
            override_decision=args.override_decision,
        )
        synthesizer.load_inputs()
        synthesizer.parse_reports()
        synthesizer.evaluate_sprint_contract()
        dec_file, road_file = synthesizer.write_outputs()

        if args.json:
            result = {
                "decision": synthesizer.decision,
                "mechanical_decision": synthesizer.mechanical_decision,
                "dimension_status": synthesizer.dimension_status,
                "fired_condition": synthesizer.fired_condition,
                "da_critical_blocked": synthesizer.da_critical_blocked,
                "da_adjudications": synthesizer.da_adjudications,
                "total_findings": len(synthesizer.findings),
                "decision_file": str(dec_file),
                "roadmap_file": str(road_file),
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=================================================================")
            print("  ARS PEER REVIEW SYNTHESIS ENGINE (SCHEMA 13.2)")
            print("=================================================================")
            print(f"Status Keputusan     : {synthesizer.decision}")
            print(f"Total Temuan Isu     : {len(synthesizer.findings)} temuan")
            if synthesizer.fired_condition:
                print(f"Kondisi Schema 13    : {synthesizer.fired_condition['id']} - {synthesizer.fired_condition['expression']}")
            if synthesizer.da_critical_blocked:
                print("DA CRITICAL Status   : [DA-CRITICAL-VS-ACCEPT: Blocked by Devil's Advocate]")
            print(f"Berkas Keputusan     : {dec_file}")
            print(f"Berkas Rencana Aksi  : {road_file}")
            print("=================================================================")

        return 0

    except Exception as e:
        print(f"[ERROR] Gagal memproses ulasan: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
