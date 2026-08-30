## graph_generator

**Libraries** ->

import os

import matplotlib

matplotlib.use("Agg")        # non-interactive backend

import matplotlib.pyplot as plt

### Paths

OUTPUT_DIR = os.path.join(dirname(__file__), "output")

### File naming

Bar chart  -> `bar_{roll}.png`

Pie chart  -> `pie_{roll}.png`

### Figure settings

| Chart | figsize       | dpi | ylim       |
|-------|---------------|-----|------------|
| Bar   | (6, 3.2)      | 120 | (0, 105)   |
| Pie   | (5.2, 3.2)    | 120 | —          |

Both use `constrained_layout=True` (do NOT also call tight_layout / bbox_inches='tight').

### Bar chart colors (based on total marks)

m >= 75  ->  "#2ECC71"   (green)

m >= 40  ->  "#F39C12"   (orange)

else     ->  "#E74C3C"   (red)

edgecolor = "black", linewidth = 0.5

### Pie chart colors (fixed 5-color palette)

["#3498DB", "#1ABC9C", "#9B59B6", "#E67E22", "#34495E"]

Order: English, Hindi, Mathematics, Science, Computer/AI

### Functions

**generate_bar_chart(res)** -> path = output/bar_{roll}.png

  - subs  = [s["name"] for s in res["subjects"]]
  - marks = [s["total"] for s in res["subjects"]]
  - bars  = ax.bar(subs, marks, color=cols, edgecolor="black", linewidth=0.5)
  - value label on top: ax.text(x_center, h+1, str(m), ha="center", va="bottom", fontsize=8, bold)
  - title: f"Subject Marks - {res['name']}", fontsize=10, bold
  - xticklabels: rotation=15, ha="right", fontsize=8
  - savefig(path, dpi=120); close(fig); returns path

**generate_pie_chart(res)** -> path = output/pie_{roll}.png

  - labels = subject names, sizes = totals
  - autopct = "%1.1f%%", startangle = 90
  - autotexts color = "white", fontsize = 7
  - title: "Weightage Share", fontsize=10, bold
  - savefig(path, dpi=120); close(fig); returns path

**generate_all_charts(res)** -> returns tuple (bar_path, pie_path)

### Notes

- `res` is the dict from `core_logic.calculate_results(row)`.
- Both charts get DELETED after PDF generation (see pdf_generator.py: `os.remove(...)` at the end of generate_pdf).
- Color thresholds (75/40) are independent of the PASS_MARK (33) used in core_logic — don't confuse them.
