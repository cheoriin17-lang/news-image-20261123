#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261123.

Writes the pre-rendered front page to /output/entry.png.
Deterministic: the same input bytes are copied on every run, so two
runs produce byte-identical output. No network, no randomness.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
DST = Path("/output/entry.png")


def main():
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST} ({DST.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
