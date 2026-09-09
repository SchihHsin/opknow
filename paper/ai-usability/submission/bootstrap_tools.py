#!/usr/bin/env python3
"""Install only a pinned, checksum-verified Pandoc binary inside this directory."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path
import platform
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent
PANDOC_VERSION = "3.11"
URL = "https://github.com/jgm/pandoc/releases/download/3.11/pandoc-3.11-arm64-macOS.zip"
SHA256 = "15806bedf9517bfead72e88fe6a6696635c3691efbb6e152173440e9c5bb50b4"


def main() -> None:
    if (platform.system(), platform.machine()) != ("Darwin", "arm64"):
        raise SystemExit("This bootstrap is pinned to macOS arm64. Set PANDOC to a local Pandoc 3.x binary on other systems.")
    payload = urllib.request.urlopen(URL, timeout=90).read()
    if hashlib.sha256(payload).hexdigest() != SHA256:
        raise SystemExit("Pandoc archive checksum mismatch; nothing installed.")
    directory = ROOT / ".tools"
    directory.mkdir(exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        member = next(name for name in archive.namelist() if name.endswith("/bin/pandoc"))
        binary = directory / "pandoc"
        binary.write_bytes(archive.read(member))
        binary.chmod(0o755)
        for name in archive.namelist():
            if name.endswith("/COPYRIGHT"):
                (directory / "PANDOC-COPYRIGHT").write_bytes(archive.read(name))
    print(f"Installed Pandoc {PANDOC_VERSION}: {binary}")


if __name__ == "__main__":
    main()
