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
OLD_TITLE = "Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression"
NEW_TITLE = (
    "Stability and Sensitivity Analysis of Heterogeneous Error Feedback "
    "(EF$^{21}$) under Communication Compression"
)


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


def phase24_ef_notation(manuscript: bytes) -> bytes:
    """Apply author-reviewed EF notation without changing scientific content."""
    text = manuscript.decode("utf-8")

    if OLD_TITLE not in text:
        raise SystemExit("Phase 24 EF notation transform could not locate the manuscript title")

    # The title is the first visible occurrence, so expand EF there and typeset
    # the algorithm name with the author-requested superscript 21.
    text = text.replace(OLD_TITLE, NEW_TITLE, 1)

    # Subsequent visible manuscript uses follow the same EF^{21} typography.
    # This transform operates on manuscript.tex only; references.bib, citation
    # keys, filenames, and source-paper bibliographic titles are not rewritten.
    text = text.replace("EF21", "EF$^{21}$")

    if NEW_TITLE not in text:
        raise SystemExit("Phase 24 EF first-use expansion validation failed")
    if "without claiming a general EF$^{21}$ convergence proof" not in text:
        raise SystemExit("Phase 24 EF notation validation marker was not found")
    if "EF21" in text:
        raise SystemExit("Phase 24 EF notation validation found a remaining plain EF21 token")

    return text.encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct the Phase 24 MDPI LaTeX sources with Pack Kwan Low as "
            "first author, Fu-Hsing Wang as second/corresponding author, and "
            "the author-reviewed Error Feedback (EF^{21}) notation."
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
                    "Phase 23c integrity failure before Phase 24 transforms: "
                    f"expected {PHASE23C_FINAL_SHA256[filename]}, got {phase23c_digest}"
                )
            data = phase24_ef_notation(phase24_authorship(phase23c))
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
        "Phase 24 author review applied: Pack Kwan Low first author; Fu-Hsing Wang "
        "second/corresponding author; first visible EF occurrence expanded to Error "
        "Feedback and subsequent manuscript notation typeset as EF^{21}. Scientific "
        "content is unchanged."
    )


if __name__ == "__main__":
    main()
