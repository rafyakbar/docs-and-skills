#!/usr/bin/env python3
"""
scripts/verify_reviewer_integrity.py

Auditor Penjaminan Mutu Laporan Peer Review (Reviewer Integrity & Finding Contract Auditor).
Memvalidasi kepatuhan laporan ulasan terhadap Kontrak Sprint Schema 13,
Finding Contract #574 (A1/A2/A3/B1), Batasan Read-Only Naskah, Typed Evidence Anchors (6 tipe),
Peniadaan Kuota Buatan (Anti-Quota Patterns), dan Validitas Coverage Receipt.

Penggunaan:
    python scripts/verify_reviewer_integrity.py --input reviews/ --paper-dir paper/
    python scripts/verify_reviewer_integrity.py --input review_report.md --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
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
        PANEL_ROLES,
        QUOTA_PATTERNS,
        RE_EVIDENCE_ANCHOR,
        ROLE_DISPLAY_NAMES,
        SEVERITIES,
    )
except ImportError:
    from scripts._review_constants import (
        PANEL_ROLES,
        QUOTA_PATTERNS,
        RE_EVIDENCE_ANCHOR,
        ROLE_DISPLAY_NAMES,
        SEVERITIES,
    )


class ReviewerIntegrityAuditor:
    def __init__(self, input_path: Path, paper_dir: Optional[Path] = None):
        self.input_path = input_path
        self.paper_dir = paper_dir
        self.raw_text: str = ""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.stats: Dict[str, Any] = {
            "detected_roles": [],
            "missing_roles": [],
            "total_weaknesses": 0,
            "total_strengths": 0,
            "anchored_weaknesses": 0,
            "unanchored_weaknesses": 0,
            "quota_violations": 0,
            "read_only_violation": False,
        }

    def load_content(self) -> None:
        """Membaca isi berkas ulasan."""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input path tidak ditemukan: {self.input_path}")

        files_to_read: List[Path] = []
        if self.input_path.is_file():
            files_to_read.append(self.input_path)
        else:
            files_to_read = sorted(list(self.input_path.glob("*.md")))

        texts = []
        for f in files_to_read:
            if (
                f.name.startswith("00_desk")
                or f.name.startswith("07_")
                or f.name.startswith("08_")
                or f.name.startswith("09_")
                or f.name.startswith("10_")
                or f.name.startswith("11_")
                or f.name.startswith("12_")
                or f.name == "REVIEW_LOG.md"
            ):
                continue
            try:
                texts.append(f.read_text(encoding="utf-8"))
            except Exception as e:
                self.warnings.append(f"Gagal membaca berkas {f}: {e}")

        self.raw_text = "\n\n".join(texts)

    def check_read_only_constraint(self) -> None:
        """Memeriksa apakah ada tanda modifikasi tidak sah pada direktori naskah paper."""
        if not self.paper_dir or not self.paper_dir.exists():
            return

        # 1. Pengecekan inline komentar review
        content_files = [f for f in self.paper_dir.glob("*.md") if not (f.name.startswith("07_") or f.name.startswith("08_"))]
        for cf in content_files:
            try:
                text = cf.read_text(encoding="utf-8")
                if re.search(r"<!--\s*REVIEWER_COMMENT|\[REVIEWER_FEEDBACK\]|###\s*Peer Review Report", text, re.IGNORECASE):
                    self.errors.append(f"Pelanggaran Read-Only: Berkas naskah {cf.name} memuat modifikasi atau komentar ulasan langsung!")
                    self.stats["read_only_violation"] = True
            except Exception:
                pass

        # 2. Pengecekan git status jika git aktif
        try:
            res = subprocess.run(
                ["git", "status", "--porcelain", str(self.paper_dir)],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout.strip():
                # Filter hanya file konten bab
                modified_lines = [line for line in res.stdout.strip().splitlines() if not any(k in line for k in ["07_", "08_"])]
                if modified_lines:
                    self.warnings.append(f"Peringatan Git: Terdeteksi perubahan pada direktori naskah paper: {', '.join(modified_lines)}")
        except Exception:
            pass

    def check_persona_coverage(self) -> None:
        """Memastikan 5 persona penilai hadir dan terdeteksi."""
        role_detectors = {
            "eic": re.compile(r"(?:EIC|Editor-in-Chief)", re.IGNORECASE),
            "methodology": re.compile(r"(?:Methodology Reviewer|Peer Reviewer 1|Metodologi)", re.IGNORECASE),
            "domain": re.compile(r"(?:Domain Reviewer|Peer Reviewer 2|Pakar Bidang)", re.IGNORECASE),
            "perspective": re.compile(r"(?:Perspective Reviewer|Peer Reviewer 3|Perspektif Silang)", re.IGNORECASE),
            "da": re.compile(r"(?:Devil's Advocate|Adversarial Reviewer|Adversarial Evaluator)", re.IGNORECASE),
        }

        detected = []
        missing = []
        for role, pattern in role_detectors.items():
            if pattern.search(self.raw_text):
                detected.append(role)
            else:
                missing.append(role)

        self.stats["detected_roles"] = detected
        self.stats["missing_roles"] = missing

        if missing:
            missing_names = [ROLE_DISPLAY_NAMES.get(r, r) for r in missing]
            self.warnings.append(f"Persona panel tidak lengkap. Peran yang belum terdeteksi: {', '.join(missing_names)}")

    def check_quota_regressions(self) -> None:
        """Memeriksa apakah ada kembalinya kuota temuan buatan (#574 A1 Quota Regressions)."""
        for pattern in QUOTA_PATTERNS:
            matches = pattern.findall(self.raw_text)
            if matches:
                self.stats["quota_violations"] += len(matches)
                for m in matches:
                    self.errors.append(f"Pelanggaran Kontrak #574 A1 (Kuota Buatan): Ditemukan instruksi kuota numerik terlarang: '{m}'")

    def check_evidence_anchors(self) -> None:
        """Memeriksa bahwa setiap kelemahan (weakness) memiliki typed evidence anchor."""
        text_to_audit = self.raw_text
        if "## 2. Contoh Luaran" in text_to_audit:
            text_to_audit = text_to_audit.split("## 2. Contoh Luaran")[0]

        w_pattern = re.compile(
            r"(?:^|\n)\s*(?:#{1,4}\s*|[-*]\s+\*{0,2})(W\d+|Kelemahan\s*\d+|Issue\s*\d+|Kritik\s*\d+|C\d+|M\d+|m\d+)\s*[:\*\n](.*?)(?=(?:\n\s*(?:#{1,4}\s*|[-*]\s+\*{0,2})(?:W\d+|S\d+|Kelemahan|Kekuatan|Issue|Coverage|Detailed|Recommendation|Strengths|C\d+|M\d+|m\d+)|\n---|\Z))",
            re.DOTALL | re.IGNORECASE,
        )

        w_matches = w_pattern.findall(text_to_audit)
        self.stats["total_weaknesses"] = len(w_matches)

        for w_tag, w_body in w_matches:
            full_w_text = f"{w_tag}: {w_body}".strip()
            first_line = full_w_text.split("\n")[0].strip()

            if RE_EVIDENCE_ANCHOR.search(full_w_text):
                self.stats["anchored_weaknesses"] += 1
            else:
                self.stats["unanchored_weaknesses"] += 1
                self.errors.append(f"Kelemahan tanpa Evidence Anchor: '{first_line}' tidak menyertakan bukti lokasi [section: ...], [page: ...], [table: ...], dll.")

    def check_severity_cleanliness(self) -> None:
        """Memastikan tidak ada field Severity apapun pada seksi Strengths (#574 A3)."""
        text_to_audit = self.raw_text
        if "## 2. Contoh Luaran" in text_to_audit:
            text_to_audit = text_to_audit.split("## 2. Contoh Luaran")[0]

        s_pattern = re.compile(
            r"(?:^|\n)\s*(?:#{1,4}\s*|[-*]\s+\*{0,2})(S\d+|Kekuatan\s*\d+|Strength\s*\d+)\s*[:\*\n](.*?)(?=(?:\n\s*(?:#{1,4}\s*|[-*]\s+\*{0,2})(?:W\d+|S\d+|Kelemahan|Kekuatan|Issue|Coverage|Detailed|Recommendation|Weaknesses|C\d+|M\d+|m\d+)|\n---|\Z))",
            re.DOTALL | re.IGNORECASE,
        )

        s_matches = s_pattern.findall(text_to_audit)
        self.stats["total_strengths"] = len(s_matches)

        for s_tag, s_body in s_matches:
            full_s_text = f"{s_tag}: {s_body}".strip()
            first_line = full_s_text.split("\n")[0].strip()
            # Severity hanya boleh ada pada Weaknesses!
            if re.search(r"\bSeverity\s*:\s*\w+", full_s_text, re.IGNORECASE):
                self.errors.append(f"Pelanggaran Format #574 A3: Ditemukan tag Severity pada blok kekuatan '{first_line}'. Severity hanya boleh digunakan pada Weaknesses!")

    def check_anti_sycophancy(self) -> None:
        """Memeriksa apakah laporan menyertakan Coverage Receipt sah jika salah satu polaritas kosong (#574 A1)."""
        has_receipt = bool(re.search(r"###?\s*Coverage Receipt", self.raw_text, re.IGNORECASE))
        has_valid_covers_header = bool(re.search(r"\*\*Covers\*\*\s*:\s*(?:Strengths|Weaknesses|both)", self.raw_text, re.IGNORECASE))

        # Jika kelemahan kosong
        if self.stats["total_weaknesses"] == 0:
            if not has_receipt:
                self.errors.append("Pelanggaran Anti-Sycophancy (#574 A1): Laporan tidak memuat kelemahan apapun dan TIDAK menyertakan 'Coverage Receipt' formal!")
            elif not has_valid_covers_header:
                self.warnings.append("Format Coverage Receipt tidak lengkap: Belum menyertakan penanda '**Covers**: [Weaknesses/both]'.")

        # Jika kekuatan kosong
        if self.stats["total_strengths"] == 0:
            if not has_receipt and self.stats["total_weaknesses"] > 0:
                # Bila strengths kosong tanpa receipt, catat sebagai peringatan/audit receipt
                self.warnings.append("Laporan tidak memuat kekuatan (Strengths). Disarankan menyertakan 'Coverage Receipt' untuk menutup dimensi.")

    def run_audit(self) -> bool:
        """Menjalankan seluruh rangkaian audit integritas ulasan."""
        self.load_content()
        self.check_read_only_constraint()
        self.check_persona_coverage()
        self.check_quota_regressions()
        self.check_evidence_anchors()
        self.check_severity_cleanliness()
        self.check_anti_sycophancy()

        return len(self.errors) == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Auditor Penjaminan Mutu Laporan Peer Review Naskah Akademik."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path ke berkas ulasan Markdown (.md) atau direktori ulasan.",
    )
    parser.add_argument(
        "-p", "--paper-dir",
        help="Direktori naskah paper untuk pemeriksaan read-only constraint.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Cetak luaran audit dalam format JSON.",
    )

    args = parser.parse_args()
    input_path = Path(args.input)
    paper_dir = Path(args.paper_dir) if args.paper_dir else None

    try:
        auditor = ReviewerIntegrityAuditor(input_path=input_path, paper_dir=paper_dir)
        is_valid = auditor.run_audit()

        if args.json:
            result = {
                "valid": is_valid,
                "errors": auditor.errors,
                "warnings": auditor.warnings,
                "stats": auditor.stats,
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("=================================================================")
            print("  ARS PEER REVIEW INTEGRITY AUDIT REPORT (#574 LINT)")
            print("=================================================================")
            status_str = "PASSED (Kepatuhan Valid)" if is_valid else "FAILED (Ditemukan Pelanggaran)"
            print(f"Status Audit         : {status_str}")
            print(f"Persona Terdeteksi   : {len(auditor.stats['detected_roles'])}/5 peran ({', '.join(auditor.stats['detected_roles'])})")
            print(f"Total Kelemahan      : {auditor.stats['total_weaknesses']} temuan")
            print(f"Anchored Weaknesses  : {auditor.stats['anchored_weaknesses']} terverifikasi bukti")
            print(f"Unanchored Weaknesses: {auditor.stats['unanchored_weaknesses']}")
            print(f"Pelanggaran Kuota    : {auditor.stats['quota_violations']}")

            if auditor.errors:
                print("\n[ERROR DITEMUKAN]:")
                for err in auditor.errors:
                    print(f"  ❌ {err}")

            if auditor.warnings:
                print("\n[PERINGATAN]:")
                for warn in auditor.warnings:
                    print(f"  ⚠️  {warn}")

            print("=================================================================")

        return 0 if is_valid else 1

    except Exception as e:
        print(f"[ERROR] Eksekusi audit gagal: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
