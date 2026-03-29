#!/usr/bin/env python3
"""
ENS 491 proje takvimi için Gantt grafiği üretir.

- Her zaman: SVG (sadece standart kütüphane, ek paket gerekmez)
- İsteğe bağlı: PNG ve PDF — matplotlib yüklüyse
      pip install matplotlib

Çalıştırma:
    python scripts/generate_gantt.py

Çıktı (Mock_Proposal_ENS491/images/):
    ens491_gantt.svg
    ens491_gantt.png   (matplotlib varsa)
    ens491_gantt.pdf   (matplotlib varsa)
"""

from __future__ import annotations

import html
import textwrap
from pathlib import Path

MEMBER_COLORS = {
    "Mustafa Bozyel": "#2563eb",
    "Ömer Mert Özel": "#059669",
    "Senih Kırmaç": "#d97706",
}

# draft_proposal tablosu ile uyumlu: (görev, başlangıç haftası W1=1, süre hafta, lider)
TASKS: list[tuple[str, int, int, str]] = [
    ("Literature extension", 1, 3, "Mustafa Bozyel"),
    ("Prototype: modes & UI polish", 2, 5, "Ömer Mert Özel"),
    ("Design concepts (figures / docs)", 4, 4, "Senih Kırmaç"),
    ("Pilot evaluation / heuristics", 8, 4, "Mustafa Bozyel"),
    ("Draft report & presentation", 11, 3, "Senih Kırmaç"),
]


def write_svg(path: Path) -> None:
    """Matplotlib gerektirmez; tarayıcıda veya Inkscape'te açılabilir."""
    label_w = 260
    margin_top = 72
    row_h = 44
    week_w = 42
    total_weeks = 14
    chart_w = total_weeks * week_w
    legend_h = 56
    width = label_w + chart_w + 48
    height = margin_top + len(TASKS) * row_h + legend_h + 24

    title = "ENS 491 — Draft schedule (task leaders)"
    subtitle = "AI-driven uncertainty-aware visualization · GPS visualization track"

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'font-family="Helvetica Neue, Helvetica, Arial, sans-serif">',
        '<rect width="100%" height="100%" fill="#fafafa"/>',
        f'<text x="{width // 2}" y="32" text-anchor="middle" font-size="18" font-weight="bold" fill="#111">'
        f"{html.escape(title)}</text>",
        f'<text x="{width // 2}" y="54" text-anchor="middle" font-size="12" fill="#475569">'
        f"{html.escape(subtitle)}</text>",
    ]

    # Hafta ekseni
    axis_y = margin_top - 8
    for w in range(total_weeks):
        x = label_w + w * week_w + week_w / 2
        parts.append(
            f'<text x="{x:.1f}" y="{axis_y}" text-anchor="middle" font-size="11" fill="#64748b">W{w + 1}</text>'
        )
    parts.append(
        f'<line x1="{label_w}" y1="{margin_top}" x2="{label_w + chart_w}" y2="{margin_top}" '
        f'stroke="#cbd5e1" stroke-width="1"/>'
    )

    for i, (name, week_start, duration, leader) in enumerate(TASKS):
        y = margin_top + i * row_h
        color = MEMBER_COLORS[leader]
        left = label_w + (week_start - 1) * week_w
        bar_w = duration * week_w - 4
        parts.append(
            f'<text x="{label_w - 8}" y="{y + row_h // 2 + 4}" text-anchor="end" font-size="11" fill="#0f172a">'
            f"{html.escape(name)}</text>"
        )
        parts.append(
            f'<rect x="{left + 2}" y="{y + 8}" width="{bar_w}" height="{row_h - 16}" rx="6" '
            f'fill="{color}" stroke="#1f2937" stroke-width="0.8"/>'
        )
        short = html.escape(leader.split()[0])
        parts.append(
            f'<text x="{left + 2 + bar_w / 2}" y="{y + row_h // 2 + 5}" text-anchor="middle" '
            f'font-size="10" font-weight="bold" fill="white">{short}</text>'
        )

    # Dikey grid
    for w in range(total_weeks + 1):
        gx = label_w + w * week_w
        gy2 = margin_top + len(TASKS) * row_h
        parts.append(f'<line x1="{gx}" y1="{margin_top}" x2="{gx}" y2="{gy2}" stroke="#e2e8f0" stroke-width="1"/>')

    # Lejant
    ly = margin_top + len(TASKS) * row_h + 20
    parts.append(f'<text x="24" y="{ly + 14}" font-size="12" font-weight="bold" fill="#334155">Task leader</text>')
    lx = 24
    for member, hex_c in MEMBER_COLORS.items():
        parts.append(
            f'<rect x="{lx}" y="{ly}" width="14" height="14" fill="{hex_c}" stroke="#1f2937" stroke-width="0.6"/>'
        )
        parts.append(
            f'<text x="{lx + 22}" y="{ly + 12}" font-size="11" fill="#1e293b">{html.escape(member)}</text>'
        )
        lx += 210

    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def write_matplotlib_png_pdf(out_dir: Path) -> bool:
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Patch
    except ImportError:
        return False

    fig, ax = plt.subplots(figsize=(12, 4.2), dpi=120)
    n = len(TASKS)

    for i, (name, week_start, duration, leader) in enumerate(TASKS):
        color = MEMBER_COLORS[leader]
        left = week_start - 1
        ax.barh(
            i,
            duration,
            left=left,
            height=0.55,
            color=color,
            edgecolor="#1f2937",
            linewidth=0.85,
            alpha=0.92,
        )
        short = leader.split()[0]
        ax.text(
            left + duration / 2,
            i,
            short,
            ha="center",
            va="center",
            fontsize=9,
            color="white",
            fontweight="bold",
        )

    ax.set_yticks(range(n))
    ax.set_yticklabels([t[0] for t in TASKS], fontsize=10)
    ax.set_xlabel("Project week (indicative)", fontsize=11)
    ax.set_xlim(-0.2, 14.2)
    ax.set_xticks(range(14))
    ax.set_xticklabels([f"W{k}" for k in range(1, 15)])
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle=":", alpha=0.55, color="#64748b")
    ax.set_axisbelow(True)

    handles = [Patch(facecolor=c, edgecolor="#1f2937", label=m) for m, c in MEMBER_COLORS.items()]
    ax.legend(handles=handles, loc="lower right", title="Task leader", framealpha=0.95)
    ax.set_title(
        "ENS 491 — AI-driven uncertainty-aware visualization (GPS track)\nDraft schedule — task leaders",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )
    fig.tight_layout()

    png = out_dir / "ens491_gantt.png"
    pdf = out_dir / "ens491_gantt.pdf"
    fig.savefig(png, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {png}")
    print(f"Wrote {pdf}")
    return True


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    out_dir = base / "images"
    out_dir.mkdir(parents=True, exist_ok=True)

    svg_path = out_dir / "ens491_gantt.svg"
    write_svg(svg_path)
    print(f"Wrote {svg_path}")

    if not write_matplotlib_png_pdf(out_dir):
        print(
            textwrap.dedent(
                """
                (Matplotlib yok — sadece SVG üretildi. PNG/PDF için:
                    python3 -m venv .venv && source .venv/bin/activate
                    pip install matplotlib
                    python scripts/generate_gantt.py)
                """
            ).strip()
        )


if __name__ == "__main__":
    main()
