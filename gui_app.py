import pandas as pd
import os, threading, tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core_logic import (load_data, processing_records, compute_ranks,
                        calculate_results)
from pdf_generator import generate_pdf, SCHOOL_NAME, SCHOOL_ADDR
from generate_csv import generate_csv

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "students.csv")
NAVY, GOLD, GREEN, RED, GREY, WHITE = "#1A237E", "#C9A227", "#2E7D32", "#C62828", "#6B7280", "#FFFFFF"
LIGHT = "#EEF2F7"
F = "Segoe UI"


class ReportCardApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Student Report Card Generator")
        root.geometry("1180x720")
        self.data = self.ranks = self.cs = self.cur = pd.DataFrame()
        self._theme(); self._header(); self._sidebar(); self._preview()
        self.status = tk.StringVar(value="Ready. Load a CSV to begin.")
        tk.Label(root, textvariable=self.status, fg=GREY, bg=LIGHT,
                 font=(F, 9), anchor="w").pack(fill="x", side="bottom")
        if os.path.exists(CSV_PATH): self._load(CSV_PATH)

    def _theme(self):
        s = ttk.Style()
        try: s.theme_use("clam")
        except tk.TclError: pass
        s.configure("Treeview.Heading", font=(F, 11, "bold"),
                    background=NAVY, foreground=WHITE)
        s.configure("Treeview", font=(F, 10), rowheight=22)

    def _header(self):
        h = tk.Frame(self.root, bg=NAVY); h.pack(fill="x")
        for t, sz, fg, pady in [(SCHOOL_NAME, 16, WHITE, (12, 0)),
                                (SCHOOL_ADDR, 11, GOLD, (0, 2)),
                                ("ANNUAL PERFORMANCE REPORT  -  Session 2025-26  |  Class XI", 11, GOLD, (0, 10))]:
            tk.Label(h, text=t, font=(F, sz, "bold") if sz == 16 else (F, sz),
                     fg=fg, bg=NAVY).pack(pady=pady)

    def _sidebar(self):
        s = tk.Frame(self.root, bg=NAVY, width=320)
        s.pack(fill="y", side="left"); s.pack_propagate(False)
        def hdr(t):
            tk.Label(s, text=t, font=(F, 11, "bold"), fg=WHITE, bg=NAVY,
                     anchor="w").pack(fill="x", padx=14, pady=(12, 4))
        hdr("1.  LOAD DATA")
        ttk.Button(s, text="Browse CSV...", command=self.on_load).pack(fill="x", padx=14, pady=2)
        ttk.Button(s, text="Load Sample Data", command=self.on_sample).pack(fill="x", padx=14, pady=2)
        self.file_lbl = tk.StringVar(value="No file loaded")
        tk.Label(s, textvariable=self.file_lbl, font=(F, 9), fg=WHITE,
                 bg=NAVY, anchor="w", wraplength=290).pack(fill="x", padx=14, pady=4)
        hdr("2.  SEARCH STUDENT")
        self.q = tk.StringVar(); self.q.trace_add("write", self._search)
        ttk.Entry(s, textvariable=self.q).pack(fill="x", padx=14, pady=2)
        self.mode = tk.StringVar(value="name")
        mf = tk.Frame(s, bg=NAVY); mf.pack(fill="x", padx=14)
        for txt, val in [("By Name", "name"), ("By Roll No.", "roll")]:
            ttk.Radiobutton(mf, text=txt, value=val, variable=self.mode,
                            command=self._search).pack(side="left", padx=(0, 10))
        hdr("3.  STUDENT LIST")
        lw = tk.Frame(s, bg=NAVY); lw.pack(fill="both", expand=True, padx=14, pady=2)
        self.lb = tk.Listbox(lw, font=(F, 10), bd=0, highlightthickness=0,
                             selectbackground=GOLD, selectforeground=WHITE)
        sb = ttk.Scrollbar(lw, orient="vertical", command=self.lb.yview)
        self.lb.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        self.lb.config(yscrollcommand=sb.set)
        self.lb.bind("<<ListboxSelect>>", self._select)
        hdr("4.  ACTIONS")
        ttk.Button(s, text="Generate PDF for Selected", command=self.on_pdf).pack(fill="x", padx=14, pady=2)
        ttk.Button(s, text="Generate ALL PDFs (Batch)", command=self.on_batch).pack(fill="x", padx=14, pady=2)

    def _preview(self):
            w = ttk.Frame(self.root)
            w.pack(fill="both", expand=True, side="left", padx=(10, 12), pady=8)
            self.cv = tk.Canvas(w, bg=WHITE, highlightthickness=0)
            self.inner = ttk.Frame(self.cv)
            sb = ttk.Scrollbar(w, orient="vertical", command=self.cv.yview)
            

            self.win_id = self.cv.create_window((0, 0), window=self.inner, anchor="nw")
            self.cv.config(yscrollcommand=sb.set)
            
            self.inner.bind("<Configure>", lambda e: self.cv.config(scrollregion=self.cv.bbox("all")))
            self.cv.bind("<Configure>", lambda e: self.cv.itemconfig(self.win_id, width=e.width))
            
            self.cv.pack(side="left", fill="both", expand=True)
            sb.pack(side="right", fill="y")
            
            tk.Label(self.inner, text="\n\nNo student selected.\nLoad a CSV and pick a student.",
                    font=(F, 11), fg=GREY).pack(padx=40, pady=80)

    def on_load(self):
        p = filedialog.askopenfilename(
            title="Select students CSV",
            filetypes=[("CSV/Excel", "*.csv *.xlsx *.xls"), ("All", "*.*")])
        if p: self._load(p)

    def on_sample(self):
        if not os.path.exists(CSV_PATH):
            try: generate_csv()
            except Exception as e: messagebox.showerror("Error", str(e)); return
        self._load(CSV_PATH)

    def _load(self, path):
        try:
            self.data = processing_records(load_data(path))
            self.ranks = compute_ranks(self.data)
            d = self.data
            self.cs = {"total": round(float(d["grand_total"].mean()), 1),
                       "avg":   round(float(d["average"].mean()), 2),
                       "pct":   round(float(d["percentage"].mean()), 2),
                       "mode":  d["grade"].mode().iloc[0],
                       "pass":  round((d["status"].eq("PASS").sum() / len(d)) * 100, 1)}
        except Exception as e:
            messagebox.showerror("Load failed", str(e)); return
        self.file_lbl.set(os.path.basename(path))
        self._refresh(self.data); self.status.set(f"Loaded {len(self.data)} students.")
        self._clear()
        tk.Label(self.inner, text="\n\nSelect a student from the list.",
                 font=(F, 11), fg=GREY).pack(padx=40, pady=80)

    def _search(self, *_):
        if self.data is None: return
        q = self.q.get().strip()
        d = self.data if not q else (
            self.data[self.data["Roll Number"].astype(str).str.contains(q, na=False)]
            if self.mode.get() == "roll"
            else self.data[self.data["Student Name"].str.lower().str.contains(q.lower(), na=False)])
        self._refresh(d); self.status.set(f"{len(d)} match(es).")

    def _refresh(self, df):
        self.lb.delete(0, tk.END)
        for _, r in df.iterrows():
            self.lb.insert(tk.END, f"{r['Roll Number']:>4}  -  {r['Student Name']}")
        self._list_df = df.reset_index(drop=True)

    def _select(self, _):
        sel = self.lb.curselection()
        if not sel or self.data is None: return
        i = sel[0]
        if i >= len(self._list_df): return
        self.cur = calculate_results(self._list_df.iloc[i]); self._render()
        self.status.set(f"Selected: {self.cur['name']} (Roll {self.cur['roll']})")

    def on_pdf(self):
        if self.data is not None and not self.data.empty: messagebox.showinfo("No selection", "Pick a student first."); return
        try:
            p = generate_pdf(self.cur, self.ranks); self.status.set(f"PDF saved: {p}")
            if messagebox.askyesno("Done", f"PDF generated:\n{p}\n\nOpen folder?"):
                self._open_dir(os.path.dirname(p))
        except Exception as e: messagebox.showerror("PDF error", str(e))

    def on_batch(self):
        if self.data is None: messagebox.showinfo("No data", "Load a CSV first."); return
        if messagebox.askyesno("Confirm Batch", f"Generate report cards for ALL {len(self.data)} students?"):
            threading.Thread(target=self._batch, daemon=True).start()

    def _batch(self):
        total, ok = len(self.data), 0
        for i, (_, row) in enumerate(self.data.iterrows(), 1):
            try: generate_pdf(calculate_results(row), self.ranks); ok += 1
            except Exception: pass
            self.status.set(f"Batch progress: {i}/{total}  (OK: {ok})")
        self.status.set(f"Batch done. {ok}/{total} PDFs in output/.")
        messagebox.showinfo("Batch complete", f"{ok}/{total} PDFs generated.")

    def _clear(self):
        for c in self.inner.winfo_children(): c.destroy()

    def _sec(self, t):
        tk.Label(self.inner, text=t, font=(F, 11, "bold"), fg=NAVY,
                 bg=WHITE, anchor="w").pack(fill="x", padx=20, pady=(10, 0))
        ttk.Separator(self.inner, orient="horizontal").pack(fill="x", padx=20)

    def _render(self):
        self._clear()
        r = self.cur; rk = self.ranks["overall"].get(int(r["roll"]), "-"); n = len(self.ranks["overall"]) # type: ignore
        # Student details
        self._sec("STUDENT DETAILS")
        d = tk.Frame(self.inner, bg=LIGHT, bd=1, relief="solid"); d.pack(fill="x", padx=20, pady=4)
        rows = [("Student Name", r["name"], "Roll Number", str(r["roll"])),
                ("Class", str(r["class"]), "Section", r["section"]),
                ("Overall Rank", f"{rk} / {n}", "Result", r["status"])]
        for ri, (l1, v1, l2, v2) in enumerate(rows):
            for ci, (l, v) in enumerate([(l1, v1), (l2, v2)]):
                col = ci * 2
                tk.Label(d, text=l, font=(F, 9), fg=GREY, bg=LIGHT).grid(
                    row=ri, column=col, sticky="w", padx=(8, 4), pady=3)
                vc = GREEN if (l == "Result" and v == "PASS") else RED if (l == "Result" and v == "FAIL") else "#111"
                tk.Label(d, text=v, font=(F, 10, "bold"), fg=vc, bg=LIGHT).grid(
                    row=ri, column=col + 1, sticky="w", pady=3)
        # Subject table
        self._sec("SUBJECT-WISE PERFORMANCE")
        cols = ("subject", "theory", "practical", "total", "grade", "rank")
        tv = ttk.Treeview(self.inner, columns=cols, show="headings", height=6)
        for c, h, w in zip(cols, ["Subject", "Theory (/80)", "Practical (/20)",
                                   "Total (/100)", "Grade", "Rank"],
                           [180, 90, 110, 90, 80, 80]):
            tv.heading(c, text=h); tv.column(c, width=w, anchor="center")
        tv.column("subject", anchor="w")
        for s in r["subjects"]:
            sr = self.ranks["subjects"].get(s["name"], {}).get(r["roll"], "-")
            tv.insert("", tk.END, values=(s["name"], s["theory"], s["practical"],
                                          s["total"], s["grade"], sr),
                      tags=("fail",) if s["total"] < 33 else ())
        th = sum(s["theory"] for s in r["subjects"])
        tp = sum(s["practical"] for s in r["subjects"])
        tv.insert("", tk.END, values=("TOTAL", th, tp, r["total"], r["grade"], rk), tags=("total",))
        tv.tag_configure("total", background=GOLD, foreground=WHITE)
        tv.tag_configure("fail", background="#FFCDD2")
        tv.pack(fill="x", padx=20, pady=4)
        # Summary tiles (extra #2: class-avg comparison)
        self._sec("RESULT SUMMARY   (class avg shown alongside - extra feature)")
        self._tiles(r, rk, n)
        # Remarks
        self._sec("REMARKS")
        rm = tk.Frame(self.inner, bg="#FFF9E6", bd=1, relief="solid"); rm.pack(fill="x", padx=20, pady=4)
        tk.Label(rm, text=f"{r['remarks']}\n\nClass Teacher's Note: Performance "
                          f"reflects consistent effort.",
                 font=(F, 10), bg="#FFF9E6", anchor="w", justify="left").pack(padx=10, pady=8, fill="x")

    def _tiles(self, r, rk, n):
        cs = self.cs or {}
        def arr(s, c): return "  \u2191" if s > c else "  \u2193" if s < c else "  ="
        tiles = [("TOTAL", f"{r['total']}/{r['max_total']}", f"Class avg: {cs.get('total', '-')}", NAVY),
                 ("AVERAGE", f"{r['average']}", f"Class avg: {cs.get('avg', '-')}{arr(r['average'], cs.get('avg', 0))}", NAVY),
                 ("PERCENTAGE", f"{r['percentage']}%", f"Class avg: {cs.get('pct', '-')}%{arr(r['percentage'], cs.get('pct', 0))}", NAVY),
                 ("GRADE", r["grade"], f"Class mode: {cs.get('mode', '-')}", GOLD),
                 ("RANK", f"{rk}/{n}", f"Class size: {n}", NAVY),
                 ("STATUS", r["status"], f"Class pass%: {cs.get('pass', '-')}%",
                  GREEN if r["status"] == "PASS" else RED)]
        g = tk.Frame(self.inner, bg=WHITE); g.pack(fill="x", padx=20, pady=6)
        for i, (l, v, sub, col) in enumerate(tiles):
            t = tk.Frame(g, bg=WHITE, bd=1, relief="solid")
            t.grid(row=0, column=i, sticky="nsew", padx=4); g.columnconfigure(i, weight=1)
            tk.Label(t, text=v, font=(F, 16, "bold"), fg=col, bg=WHITE).pack()
            tk.Label(t, text=l, font=(F, 8), fg=GREY, bg=WHITE).pack()
            tk.Label(t, text=sub, font=(F, 8, "italic"), fg=NAVY, bg=WHITE).pack(pady=(2, 4))

    def _open_dir(self, p):
        try:
            import subprocess, platform
            if os.name == "nt": os.startfile(p)
            elif platform.system() == "Darwin": subprocess.Popen(["open", p])
            else: subprocess.Popen(["xdg-open", p])
        except Exception: pass


def main():
    ReportCardApp(tk.Tk()); tk.mainloop()


if __name__ == "__main__":
    main()
