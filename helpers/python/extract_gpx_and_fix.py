#!/usr/bin/env python3
"""
GPX: timestamp'e göre sıralı lat,lon çıktısı.
GNSS log: Fix ile başlayan satırları ayrı dosyaya yazar.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

DATA = Path(__file__).resolve().parent


def extract_gpx_latlon_sorted(gpx_path: Path, out_path: Path) -> int:
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    rows: list[tuple[str, float, float]] = []

    for elem in root.iter():
        if not elem.tag.endswith("trkpt"):
            continue
        lat = float(elem.attrib["lat"])
        lon = float(elem.attrib["lon"])
        t = ""
        for ch in elem:
            if ch.tag.endswith("time") and ch.text:
                t = ch.text.strip()
                break
        if not t:
            continue
        rows.append((t, lat, lon))

    rows.sort(key=lambda r: r[0])
    lines = [f"{t}\t{lat:.10f}\t{lon:.10f}" for t, lat, lon in rows]
    out_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(rows)


def extract_fix_only(gnss_path: Path, out_path: Path) -> int:
    text = gnss_path.read_text(encoding="utf-8", errors="replace").splitlines()
    fix_lines = [ln for ln in text if ln.startswith("Fix,")]
    out_path.write_text("\n".join(fix_lines) + ("\n" if fix_lines else ""), encoding="utf-8")
    return len(fix_lines)


def main() -> None:
    gpx = DATA / "Openstreetmap-reference-data.gpx"
    gnss = DATA / "yürümece-gnss.txt"

    out_gpx = DATA / "Openstreetmap-reference-data_latlon_by_time.txt"
    out_fix = DATA / "yürümece-gnss_FixOnly.txt"

    n1 = extract_gpx_latlon_sorted(gpx, out_gpx)
    n2 = extract_fix_only(gnss, out_fix)

    print(f"Wrote {out_gpx} ({n1} points, sorted by <time>)")
    print(f"Wrote {out_fix} ({n2} Fix lines)")


if __name__ == "__main__":
    main()
