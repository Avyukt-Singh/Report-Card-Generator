## gui_app

**Libraries** ->

import pandas as pd

import os, threading, tkinter as tk

from tkinter import ttk, filedialog, messagebox

from core_logic import (load_data, processing_records, compute_ranks, calculate_results)

from pdf_generator import generate_pdf, SCHOOL_NAME, SCHOOL_ADDR

from generate_csv import generate_csv

### Paths

CSV_PATH = os.path.join(dirname(__file__), "data", "students.csv")

### Color palette

NAVY  = "#1A237E"

GOLD  = "#C9A227"

GREEN = "#2E7D32"

RED   = "#C62828"

GREY  = "#6B7280"

WHITE = "#FFFFFF"

LIGHT = "#EEF2F7"      # sidebar bg / value-tile accents

FAIL_BG  = "#FFCDD2"   # treeview fail row bg

REMARKS_BG = "#FFF9E6"

FONT = "Segoe UI"      (stored as F)

### Window

title     = "Smart Student Report Card Generator"

geometry  = "1180x720"

ttk theme = "clam"

Treeview.Heading font = (F, 11, bold), bg=NAVY, fg=WHITE

Treeview          font = (F, 10),       rowheight=22

### Layout

- Header (NAVY bg, fill="x") — three labels stacked:
    1. SCHOOL_NAME   — (F, 16, bold),  WHITE,  pady=(12, 0)
    2. SCHOOL_ADDR   — (F, 11),         GOLD,   pady=(0, 2)
    3. "ANNUAL PERFORMANCE REPORT  -  Session 2025-26  |  Class XI" — (F, 11), GOLD, pady=(0, 10)

- Sidebar (NAVY bg, width=320, pack_propagate=False, side="left")
    Section headers: (F, 11, bold), WHITE, NAVY, anchor="w", padx=14, pady=(12, 4)
    Sections:
      "1.  LOAD DATA"     -> Browse CSV button, Load Sample Data button, file_lbl (F, 9, WHITE, wraplength=290)
      "2.  SEARCH STUDENT" -> Entry bound to self.q (trace_add write -> _search), Radiobuttons "By Name" / "By Roll No." (var=self.mode)
      "3.  STUDENT LIST"   -> tk.Listbox (F, 10, bd=0, highlightthickness=0, selectbackground=GOLD, selectforeground=WHITE), Scrollbar right
      "4.  ACTIONS"        -> "Generate PDF for Selected", "Generate ALL PDFs (Batch)"

- Preview area: ttk.Frame side="left", padx=(10, 12), pady=8
    Canvas (bg=WHITE, highlightthickness=0) + inner ttk.Frame + vertical Scrollbar
    Window id stored as self.win_id; <Configure> updates scrollregion and width.

- Status bar: tk.Label at bottom, textvariable=self.status, (F, 9), GREY, LIGHT, anchor="w"

### Class state (init)

self.data, self.ranks, self.cs, self.cur  = 4 empty DataFrames initially.

self.status = tk.StringVar(value="Ready. Load a CSV to begin.")

If CSV_PATH exists at startup, auto-loads.

### Functions

**__init__(root)** -> sets up theme/header/sidebar/preview, status bar, auto-load CSV if exists.

**_theme()** -> ttk.Style, theme_use("clam") wrapped in try/except TclError; configure Treeview.Heading + Treeview fonts/rowheight.

**_header()** -> builds the NAVY header with three labels.

**_sidebar()** -> builds 4 sidebar sections (see Layout).

**_preview()** -> builds the scrollable canvas area; initial empty-state label "\n\nNo student selected.\nLoad a CSV and pick a student." (F, 11, GREY, padx=40, pady=80).

**on_load()** -> filedialog.askopenfilename(title="Select students CSV", filetypes=[("CSV/Excel", "*.csv *.xlsx *.xls"), ("All", "*.*")]).

**on_sample()** -> if CSV missing, calls generate_csv(); then _load(CSV_PATH).

**_load(path)** -> processing_records(load_data(path)); compute_ranks; computes class stats self.cs = {total, avg, pct, mode, pass%}. Shows message box on error.

**_search(*_)** -> if mode=="roll" filter on Roll Number as string.contains; else Name lower.contains; refresh listbox; status "{n} match(es)."

**_refresh(df)** -> clears listbox; inserts "  {roll:>4}  -  {name}"; stores self._list_df = df.reset_index(drop=True).

**_select(_)** -> on ListboxSelect: idx = curselection()[0]; cur = calculate_results(self._list_df.iloc[idx]); _render(); status "Selected: {name} (Roll {roll})".

**on_pdf()** -> if no cur, info box "Pick a student first."; else generate_pdf(cur, ranks); ask "Open folder?".

**on_batch()** -> confirm "Generate report cards for ALL {n} students?"; starts daemon thread _batch.

**_batch()** -> iterates self.data, calls generate_pdf(calculate_results(row), ranks); updates status "{i}/{total} (OK: {ok})"; final message box.

**_clear()** -> destroys all children of self.inner.

**_sec(t)** -> section header label (F, 11, bold, NAVY, WHITE, anchor="w", padx=20, pady=(10, 0)) + ttk.Separator (padx=20).

**_render()** -> clears, builds:
    1. STUDENT DETAILS — tk.Frame bg=LIGHT bd=1 relief="solid"; grid of label/value pairs:
       (Student Name, Roll Number), (Class, Section), (Overall Rank "{rk}/{n}", Result)
       Result value colored GREEN if PASS, RED if FAIL, else "#111".
    2. SUBJECT-WISE PERFORMANCE — ttk.Treeview cols=(subject, theory, practical, total, grade, rank), height=6
       Header texts:  ["Subject", "Theory (/80)", "Practical (/20)", "Total (/100)", "Grade", "Rank"]
       Column widths:  [180, 90, 110, 90, 80, 80]  (subject anchor="w", rest "center")
       Inserts rows from r["subjects"]; tags "fail" if total < 33
       Final TOTAL row tagged "total" (GOLD bg, WHITE fg)
       Fail row tag bg = "#FFCDD2"
    3. RESULT SUMMARY  (class avg shown alongside - extra feature) — calls _tiles(r, rk, n)
    4. REMARKS — tk.Frame bg="#FFF9E6" bd=1 relief="solid"; label "{remarks}\n\nClass Teacher's Note: Performance reflects consistent effort." (F, 10, anchor="w", justify="left", padx=10, pady=8)

**_tiles(r, rk, n)** -> builds 6 tiles in a grid row:
    Tiles (label, value, sub-text, color):
      TOTAL       — "{total}/{max_total}"         Class avg: total     NAVY
      AVERAGE     — "{average}"                   Class avg: avg↑/↓/=   NAVY
      PERCENTAGE  — "{percentage}%"               Class avg: pct%↑/↓/=  NAVY
      GRADE       — "{grade}"                     Class mode: mode     GOLD
      RANK        — "{rk}/{n}"                    Class size: n         NAVY
      STATUS      — "{status}"                    Class pass%: pass%    GREEN (PASS) / RED (FAIL)
    Tile fonts: value (F, 16, bold), label (F, 8, GREY), sub (F, 8, italic, NAVY)
    Arrow logic: ↑ if s > c, ↓ if s < c, = if equal.

**_open_dir(p)** -> os.startfile (Windows) / open (Darwin) / xdg-open (Linux), wrapped in try/except.

**main()** -> ReportCardApp(tk.Tk()); tk.mainloop()

### Notes

- Status bar updates via self.status.set(...) at every state change.
- Selection color: listbox selectbackground = GOLD.
- Treeview column widths (180/90/110/90/80/80) sum to 630 px.
- Tiles use a 6-column grid with columnconfigure(weight=1) each.
- Batch runs in daemon thread so UI stays responsive; status bar shows progress.
