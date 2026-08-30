import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def generate_bar_chart(res):
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  path = os.path.join(OUTPUT_DIR, f"bar_{res['roll']}.png")
  subs = [s["name"] for s in res["subjects"]]
  marks = [s["total"] for s in res["subjects"]]
  cols = [
      "#2ECC71" if m >= 75 else "#F39C12" if m >= 40 else "#E74C3C" for m in marks
  ]

  fig, ax = plt.subplots(figsize=(6, 3.2), constrained_layout=True)
  bars = ax.bar(subs, marks, color=cols, edgecolor="black", linewidth=0.5)
  for b, m in zip(bars, marks):
    ax.text(
        b.get_x() + b.get_width() / 2,
        b.get_height() + 1,
        str(m),
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )
  ax.set_ylim(0, 105)
  ax.set_title(
      f"Subject Marks - {res['name']}", fontsize=10, fontweight="bold"
  )
  plt.setp(ax.get_xticklabels(), rotation=15, ha="right", fontsize=8)
  fig.savefig(path, dpi=120)
  plt.close(fig)
  return path


def generate_pie_chart(res):
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  path = os.path.join(OUTPUT_DIR, f"pie_{res['roll']}.png")
  labels = [s["name"] for s in res["subjects"]]
  sizes = [s["total"] for s in res["subjects"]]
  cols = ["#3498DB", "#1ABC9C", "#9B59B6", "#E67E22", "#34495E"]

  fig, ax = plt.subplots(figsize=(5.2, 3.2), constrained_layout=True)
  _, _, autotexts = ax.pie(
      sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=cols
  )
  for t in autotexts:
    t.set_color("white")
    t.set_fontsize(7)
  ax.set_title("Weightage Share", fontsize=10, fontweight="bold")
  fig.savefig(path, dpi=120)
  plt.close(fig)
  return path


def generate_all_charts(res):
  return generate_bar_chart(res), generate_pie_chart(res)