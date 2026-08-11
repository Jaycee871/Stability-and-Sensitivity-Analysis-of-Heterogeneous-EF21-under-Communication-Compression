#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "submission" / "mdpi_latex"

FILES = {
    "manuscript.tex": {
        "payload": "manuscript.tex.gz.b64",
        "sha256": "be4e9faa00cc48f05545d6da83df521778a14f748c83132cd9a552d16217706a",
    },
    "references.bib": {
        "payload": "references.bib.gz.b64",
        "sha256": "56d1eb6eb77845a3a5b9d85212aedd3687b59eb9105308bf7f199bacab9cb2a1",
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_payload(path: Path) -> bytes:
    encoded = "".join(path.read_text(encoding="utf-8").split())
    return gzip.decompress(base64.b64decode(encoded))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstruct the exact Phase 23b MDPI LaTeX manuscript sources."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SOURCE_DIR / "materialized",
    )
    args = parser.parse_args()

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    for filename, spec in FILES.items():
        data = decode_payload(SOURCE_DIR / spec["payload"])
        digest = sha256(data)
        if digest != spec["sha256"]:
            raise SystemExit(
                f"integrity failure for {filename}: expected {spec['sha256']}, got {digest}"
            )
        target = out / filename
        target.write_bytes(data)
        print(f"materialized {target} sha256={digest}")

    print(
        "Note: final compilation additionally requires the official MDPI ACS Definitions/ "
        "files and the publication figure PDFs from the Phase 23b package/paper-asset build."
    )


if __name__ == "__main__":
    main()
