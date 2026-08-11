#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from materialize_phase23_mdpi_latex import (
    BASE_FILES,
    FINAL_SHA256 as PHASE23C_FINAL_SHA256,
    SOURCE_DIR,
    decode_payload,
    phase23c_manuscript,
    sha256,
)

OLD_DISPLAY_AUTHOR_LINE = "Fu-Hsing Wang $^{1,}$* and Pack Kwan Low $^{1}$"
NEW_DISPLAY_AUTHOR_LINE = "Pack Kwan Low $^{1}$ and Fu-Hsing Wang $^{1,}$*"


def phase24_authorship(manuscript: bytes) -> bytes:
    """Apply the author-reviewed Phase 24 order without changing correspondence."""
    text = manuscript.decode("utf-8")

    if "\\abstract{" not in text:
        raise SystemExit("Phase 24 authorship transform could not locate the abstract boundary")

    front, abstract_marker, rest = text.partition("\\abstract{")

    if OLD_DISPLAY_AUTHOR_LINE not in front:
        raise SystemExit("Phase 24 authorship transform could not locate the Phase 23 author line")

    front = front.replace(OLD_DISPLAY_AUTHOR_LINE, NEW_DISPLAY_AUTHOR_LINE, 1)

    # MDPI templates may carry a separate plain-text author-name list for running
    # metadata. Keep its order synchronized with the displayed author line.
    front = front.replace(
        "Fu-Hsing Wang and Pack Kwan Low",
        "Pack Kwan Low and Fu-Hsing Wang",
        1,
    )
    front = front.replace(
        "Fu-Hsing Wang, Pack Kwan Low",
        "Pack Kwan Low, Fu-Hsing Wang",
        1,
    )

    text = front + abstract_marker + rest

    if NEW_DISPLAY_AUTHOR_LINE not in text:
        raise SystemExit("Phase 24 author-order validation failed")
    if "Correspondence: Fu-Hsing Wang" not in text:
        raise SystemExit("Phase 24 corresponding-author validation failed")

    return text.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct the Phase 24 MDPI LaTeX sources with Pack Kwan Low as "
            "first author and Fu-Hsing Wang as second/corresponding author."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SOURCE_DIR / "materialized_phase24",
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
            phase23c = phase23c_manuscript(data)
            phase23c_digest = sha256(phase23c)
            if phase23c_digest != PHASE23C_FINAL_SHA256[filename]:
                raise SystemExit(
                    "Phase 23c integrity failure before Phase 24 authorship transform: "
                    f"expected {PHASE23C_FINAL_SHA256[filename]}, got {phase23c_digest}"
                )
            data = phase24_authorship(phase23c)
        else:
            digest = sha256(data)
            if digest != PHASE23C_FINAL_SHA256[filename]:
                raise SystemExit(
                    f"reference integrity failure: expected {PHASE23C_FINAL_SHA256[filename]}, got {digest}"
                )

        digest = sha256(data)
        target = out / filename
        target.write_bytes(data)
        print(f"materialized {target} sha256={digest}")

    print(
        "Phase 24 authorship: Pack Kwan Low first author; Fu-Hsing Wang second author "
        "and corresponding author. Scientific content is unchanged."
    )


if __name__ == "__main__":
    main()
