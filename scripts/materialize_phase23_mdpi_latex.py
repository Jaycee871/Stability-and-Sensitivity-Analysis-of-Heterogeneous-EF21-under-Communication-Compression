#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "submission" / "mdpi_latex"

BASE_FILES = {
    "manuscript.tex": {
        "payload": "manuscript.tex.gz.b64",
        "base_sha256": "be4e9faa00cc48f05545d6da83df521778a14f748c83132cd9a552d16217706a",
    },
    "references.bib": {
        "payload": "references.bib.gz.b64",
        "base_sha256": "56d1eb6eb77845a3a5b9d85212aedd3687b59eb9105308bf7f199bacab9cb2a1",
    },
}

FINAL_SHA256 = {
    "manuscript.tex": "2ed375aa91d7b51b10f318eb03f587ea32bd776593ed4dfeac00dbee1a4ffeb3",
    "references.bib": "56d1eb6eb77845a3a5b9d85212aedd3687b59eb9105308bf7f199bacab9cb2a1",
}

DOI_GUARD = r'''
% Submission-draft display guard: the MDPI class synthesizes a placeholder DOI
% from volume/issue/article-number defaults even in submit mode. Suppress that
% footer in the author-facing draft; the Editorial Office assigns the real DOI.
\makeatletter
\AtBeginDocument{%
  \ifthenelse{\equal{\@status}{submit}}{%
    \rfoot{}%
    \fancypagestyle{plain}{\fancyfoot[R]{}}%
  }{}%
}
\makeatother
'''


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_payload(path: Path) -> bytes:
    encoded = "".join(path.read_text(encoding="utf-8").split())
    return gzip.decompress(base64.b64decode(encoded))


def phase23c_manuscript(base: bytes) -> bytes:
    text = base.decode("utf-8")
    if "Submission-draft display guard" in text:
        return base
    marker = (
        "\\keyword{distributed optimization; error feedback; EF21; communication compression; "
        "heterogeneous optimization; convergence analysis; stability analysis; sensitivity analysis}\n"
    )
    if marker not in text:
        raise SystemExit("Phase 23c DOI-guard insertion marker not found")
    text = text.replace(marker, marker + DOI_GUARD, 1)
    return text.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstruct the exact Phase 23c MDPI LaTeX manuscript sources."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SOURCE_DIR / "materialized",
    )
    args = parser.parse_args()

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    for filename, spec in BASE_FILES.items():
        data = decode_payload(SOURCE_DIR / spec["payload"])
        base_digest = sha256(data)
        if base_digest != spec["base_sha256"]:
            raise SystemExit(
                f"base integrity failure for {filename}: expected {spec['base_sha256']}, got {base_digest}"
            )

        if filename == "manuscript.tex":
            data = phase23c_manuscript(data)

        digest = sha256(data)
        if digest != FINAL_SHA256[filename]:
            raise SystemExit(
                f"Phase 23c integrity failure for {filename}: expected {FINAL_SHA256[filename]}, got {digest}"
            )

        target = out / filename
        target.write_bytes(data)
        print(f"materialized {target} sha256={digest}")

    print(
        "Note: final compilation additionally requires the official MDPI ACS Definitions/ "
        "files and the publication figure PDFs from the Phase 23c package/paper-asset build."
    )


if __name__ == "__main__":
    main()
