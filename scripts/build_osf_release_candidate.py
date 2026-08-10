#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

STATIC_ENTRIES = (
    Path("README.md"),
    Path("requirements.txt"),
    Path("src"),
    Path("scripts"),
    Path("tests"),
    Path("results"),
    Path("wolfram"),
    Path("claims"),
    Path("literature"),
    Path("docs"),
    Path("manuscript"),
    Path("submission"),
    Path("osf/osf_metadata_template.json"),
    Path(".github/workflows/ci.yml"),
)

SKIP_NAMES = {"__pycache__", ".DS_Store", ".env", ".venv", "venv"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".key", ".pem"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_NAMES for part in path.parts) or path.suffix.lower() in SKIP_SUFFIXES


def copy_entry(source: Path, destination: Path) -> None:
    if source.is_dir():
        for item in source.rglob("*"):
            if not item.is_file():
                continue
            rel = item.relative_to(source)
            if should_skip(rel):
                continue
            target = destination / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
    elif source.is_file():
        if should_skip(source):
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    else:
        raise FileNotFoundError(source)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def current_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "UNRESOLVED"


def inventory(folder: Path, exclude: Iterable[str] = ()) -> list[dict[str, object]]:
    excluded = set(exclude)
    rows: list[dict[str, object]] = []
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        rel = path.relative_to(folder).as_posix()
        if rel in excluded:
            continue
        rows.append(
            {
                "path": rel,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return rows


def validate_scientific_gate() -> dict[str, object]:
    errors: list[str] = []

    registry_path = ROOT / "claims" / "claim_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    if registry.get("version") != 2:
        errors.append("claim registry must be version 2")
    if len(registry.get("claims", [])) != 18:
        errors.append("claim registry must contain 18 claims")

    literature = json.loads(
        (ROOT / "literature" / "phase17_primary_source_closure.json").read_text(
            encoding="utf-8"
        )
    )
    if literature.get("status") != "NAMED_REFERENCE_CHAIN_CLOSED":
        errors.append("named reference chain is not closed")
    if literature.get("universal_novelty_certified") is not False:
        errors.append("universal novelty must remain explicitly uncertified")

    certificate = json.loads(
        (ROOT / "results" / "phase13_symbolic_certificate.json").read_text(
            encoding="utf-8"
        )
    )
    if "does not prove Empirical Law 4.3 itself" not in certificate.get("guardrail", ""):
        errors.append("Phase 13 empirical-law guardrail is missing")

    manuscript = (ROOT / "manuscript" / "draft.md").read_text(encoding="utf-8")
    if "Working manuscript draft — Phase 20" not in manuscript:
        errors.append("manuscript must be Phase 20 or explicitly migrated before archive")
    for marker in (
        "figure6_mismatch_geometry.svg",
        "figure7_full_regularity_penalty.svg",
        "figure8_rate_collapse.svg",
    ):
        if marker not in manuscript:
            errors.append(f"missing manuscript figure marker: {marker}")

    return {
        "valid": not errors,
        "errors": errors,
        "claim_registry_version": registry.get("version"),
        "registered_claims": len(registry.get("claims", [])),
        "named_reference_chain": literature.get("status"),
        "universal_novelty_certified": literature.get("universal_novelty_certified"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, default=Path("osf_release_candidate"))
    parser.add_argument("--paper-assets-dir", type=Path, default=None)
    parser.add_argument("--submission-package-dir", type=Path, default=None)
    args = parser.parse_args()

    output_root = args.output_root.resolve()
    bundle = output_root / "osf_release_candidate"
    if output_root.exists():
        shutil.rmtree(output_root)
    bundle.mkdir(parents=True)

    gate = validate_scientific_gate()
    if not gate["valid"]:
        raise SystemExit("OSF scientific gate failed: " + "; ".join(gate["errors"]))

    for rel in STATIC_ENTRIES:
        source = ROOT / rel
        copy_entry(source, bundle / rel)

    generated: dict[str, object] = {
        "paper_assets_included": False,
        "submission_package_included": False,
    }

    if args.paper_assets_dir is not None:
        source = args.paper_assets_dir.resolve()
        if not source.exists():
            raise FileNotFoundError(source)
        copy_entry(source, bundle / "generated" / "paper_assets")
        required_figures = [
            source / "phase19_full_regularity" / "figure6_mismatch_geometry.svg",
            source / "phase19_full_regularity" / "figure7_full_regularity_penalty.svg",
            source / "phase19_full_regularity" / "figure8_rate_collapse.svg",
        ]
        if not all(path.exists() for path in required_figures):
            raise RuntimeError("generated paper assets are missing Figures 6-8")
        generated["paper_assets_included"] = True

    if args.submission_package_dir is not None:
        source = args.submission_package_dir.resolve()
        if not source.exists():
            raise FileNotFoundError(source)
        copy_entry(source, bundle / "generated" / "submission_package")
        if not (source / "manuscript_free_format.md").exists():
            raise RuntimeError("generated submission package lacks manuscript_free_format.md")
        generated["submission_package_included"] = True

    archive_readme = """# OSF Release Candidate

This folder is a deterministic release candidate for later upload to the Open Science Framework (OSF).

It is **not** itself an OSF registration, DOI, or permanent public archive. The external OSF identifier remains unresolved until the human researcher uploads the bundle, verifies the record, and intentionally chooses the desired visibility/registration state.

## Scientific scope

The archive preserves code, tests, committed numerical and symbolic evidence, claim-to-evidence records, primary-source literature-audit records, manuscript sources, submission metadata, and—when provided to the builder—the generated publication assets and MDPI free-format package.

## Integrity

`OSF_ARCHIVE_MANIFEST.json` records the source Git commit and SHA-256 digest of every bundled file except the manifest itself.

## Claim guardrail

The archive characterizes consequences of the inherited two-agent Empirical Law 4.3. It does not convert that empirical law into a proved general EF21 convergence theorem and does not certify universal bibliographic novelty.
"""
    (bundle / "ARCHIVE_README.md").write_text(archive_readme, encoding="utf-8")

    files = inventory(bundle, exclude={"OSF_ARCHIVE_MANIFEST.json"})
    manifest = {
        "phase": 22,
        "status": "READY_FOR_OSF_DRAFT_UPLOAD",
        "source_git_commit": current_commit(),
        "scientific_gate": gate,
        "generated_artifacts": generated,
        "file_count": len(files),
        "total_bytes": sum(int(row["size_bytes"]) for row in files),
        "files": files,
        "osf": {
            "record_created": False,
            "registered": False,
            "doi": None,
            "identifier": None,
            "public": False,
        },
        "guardrail": (
            "READY_FOR_OSF_DRAFT_UPLOAD means only that the local release candidate passed the repository gate. "
            "Do not claim OSF archival, registration, DOI assignment, or public permanence until the external record exists and its identifier is verified."
        ),
    }
    (bundle / "OSF_ARCHIVE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    zip_base = output_root / "osf_release_candidate"
    archive_path = shutil.make_archive(str(zip_base), "zip", root_dir=bundle)

    build_report = {
        "status": manifest["status"],
        "bundle": str(bundle),
        "zip": archive_path,
        "file_count": manifest["file_count"],
        "total_bytes": manifest["total_bytes"],
        "source_git_commit": manifest["source_git_commit"],
        "paper_assets_included": generated["paper_assets_included"],
        "submission_package_included": generated["submission_package_included"],
        "external_osf_record_created": False,
    }
    (output_root / "build_report.json").write_text(
        json.dumps(build_report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(build_report, indent=2))


if __name__ == "__main__":
    main()
