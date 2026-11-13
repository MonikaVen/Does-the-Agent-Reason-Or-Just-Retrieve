#!/usr/bin/env python3
"""Download DiscoveryBench, SecOps-ES, AIT-ADS, SOC-AgentBench, and ExCyTIn-Bench."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "benchmarks"
ROOT.mkdir(parents=True, exist_ok=True)


def main() -> int:
    from huggingface_hub import hf_hub_download, snapshot_download

    print("DiscoveryBench…")
    snapshot_download(
        repo_id="allenai/discoverybench",
        repo_type="dataset",
        local_dir=str(ROOT / "discoverybench"),
        allow_patterns=["README.md", "discoverybench/real/**", "discoverybench/synth/**", "answer_key/**"],
    )
    print("SecOps-ES benchmark…")
    snapshot_download(
        repo_id="TocharianOU/secops-es-benchmark",
        repo_type="dataset",
        local_dir=str(ROOT / "secops-es-benchmark"),
        allow_patterns=[
            "README.md",
            "ATTACK_MAPPING.csv",
            "benchmark/**",
            "corpus/cases/**",
            "dataset/*/manifest.json",
            "dataset/*/security.ndjson.gz",
        ],
    )
    sealed = ROOT / "secops-es-benchmark" / "benchmark" / "ANSWERS.sealed"
    if sealed.exists():
        subprocess.check_call(
            [sys.executable, str(ROOT / "secops-es-benchmark" / "benchmark" / "lib" / "seal.py"), "unseal"],
            cwd=str(ROOT / "secops-es-benchmark"),
        )
    print("AIT-ADS…")
    zip_path = ROOT / "ait_ads.zip"
    if not zip_path.exists():
        subprocess.check_call(
            [
                "curl",
                "-L",
                "-o",
                str(zip_path),
                "https://zenodo.org/records/8263181/files/ait_ads.zip?download=1",
            ]
        )
    labels = ROOT / "ait_labels.csv"
    if not labels.exists():
        subprocess.check_call(
            [
                "curl",
                "-L",
                "-o",
                str(labels),
                "https://zenodo.org/records/8263181/files/labels.csv?download=1",
            ]
        )
    ads = ROOT / "ait-ads"
    ads.mkdir(exist_ok=True)
    # Extract only compact aminer JSON files.
    subprocess.check_call(["unzip", "-o", "-q", str(zip_path), "*_aminer.json", "-d", str(ads)])

    print("SOC-AgentBench…")
    snapshot_download(
        repo_id="alirezaaminzadeh/soc-agent-bench",
        repo_type="dataset",
        local_dir=str(ROOT / "soc-agent-bench"),
        allow_patterns=[
            "README.md",
            "manifest.json",
            "benchmark_report.json",
            "data/*.parquet",
            "packages/soc_agent_bench/schema.py",
        ],
    )

    print("ExCyTIn-Bench…")
    exc = ROOT / "excytin-bench"
    exc.mkdir(parents=True, exist_ok=True)
    for rel in (
        "README.md",
        "TRANSPARENCY_DOC.md",
        "data.zip",
        *[
            f"questions/{split}/incident_{inc}_qa_incident_o1-ga_c42.json"
            for split in ("test", "train")
            for inc in (5, 34, 38, 39, 55, 134, 166, 322)
        ],
    ):
        hf_hub_download(
            "anandmudgerikar/excytin-bench",
            rel,
            repo_type="dataset",
            local_dir=str(exc),
        )

    print("DiscoveryWorld: pip install discoveryworld")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "discoveryworld"])
    print("done ->", ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
