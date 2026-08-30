## main

**Libraries** ->

import os, sys

from generate_csv import generate_csv

from core_logic import (load_data, processing_records, search_student, calculate_results, compute_ranks)

from console_ui import show_menu, display_student_card, display_all_students

from pdf_generator import generate_pdf

from gui_app import main as gui_main   (lazy import inside launch_gui)

### Constants

DATA_FILE = os.path.join(dirname(__file__), "data", "students.csv")

### Entry behavior

```
if __name__ == "__main__":
    if "--cli" in sys.argv: cli_main()
    else:                    launch_gui()       # default
```

So `python main.py` → GUI ; `python main.py --cli` → console loop.

### Functions

**launch_gui()** -> lazy-imports `gui_app.main`; calls it.

**pick_one(matches)** -> if 1 match: return matches.iloc[0]. Else prints "{N} students found:" with numbered list "   {i}. {roll} - {name}", prompts "Enter number: " (int), returns matches.iloc[c-1] if 1<=c<=N else None. ValueError → "Invalid choice."

**action_search(data)** -> prompts "Enter Name or Roll No.: "; calls search_student(data, q); if empty prints "No student matched '{q}'."; else pick_one, then display_student_card(calculate_results(ch), compute_ranks(data)); waits on Enter.

**action_pdf(data)** -> prompts "Enter Roll No.: "; search_student; if empty "Student not found."; else generate_pdf(calculate_results(ms.iloc[0]), compute_ranks(data)); prints "[OK] PDF generated:\n   {path}" or "[ERROR] {e}". Waits on Enter.

**cli_main()** -> if no DATA_FILE: prints "No data found.", prompts "Generate sample CSV? (y/n):"; if y → generate_csv() else exit(1). Then load_data(DATA_FILE) + processing_records(raw). Loop:

  show_menu(); c = input("Enter choice (1-5): ").strip()

  | c | Action                                |
  |---|---------------------------------------|
  | 1 | action_search(data)                   |
  | 2 | display_all_students(data)            |
  | 3 | action_pdf(data)                      |
  | 4 | (pass) — charts menu item, no action   |
  | 5 | "Thank you for using the Report Card Generator!"; break |
  | * | "Invalid choice." + Enter              |

### Notes

- Option 4 in the menu (Generate Bar + Pie Charts) is intentionally a no-op in CLI; charts are only auto-generated inside PDFs.
- CSV sample is generated on first run if missing and user agrees.
- Exceptions during load → "Failed to load data: {e}" + sys.exit(1).
- All actions pause with `input("  Press Enter...")` so the user can read output before the screen clears.
