## console_ui

**Libraries** ->

from utils import print_banner, clear_screen

### Constants

SCHOOL_NAME = "GD Goenka School"

SCHOOL_ADDR = "8th KM Stone, Jansath Road, Muzaffarnagar"

Banner char = "="

Separator length = 72 chars (`"="*72`)

Table dashes = 60 chars (`"-"*60`)

### Functions

**show_menu()** -> clear_screen, banner with SCHOOL_NAME + " | REPORT CARD GENERATOR", addr, "="*72, 5 menu items (1.Search, 2.List, 3.PDF, 4.Charts, 5.Exit), "="*72

**display_student_card(res, ranks)** -> Banner=SCHOOL_NAME, addr, title="ANNUAL PERFORMANCE REPORT - Class XI", "="*72

  STUDENT DETAILS block:
  - Name, Roll No., Class/Sec (e.g. "11 - A"), Overall Rank: rank/N

  SUBJECT-WISE MARKS table -> columns: Subject(14), Theory(8), Prac(6), Total(8), Max(6), Grade(7), Rank(6) — all right-aligned except Subject (left). Dashes row: "  "+"-"*60

  SUMMARY block -> Grand Total/max_total, Average, Percentage %, Grade, Result

  REMARKS block -> remarks text, "="*72

**display_all_students(data)** -> Banner=SCHOOL_NAME + " | ALL STUDENTS", header: Roll(6), Name(22), %(8), Grade(7), Rank(7), Status(9) — right-aligned except Roll and Name. Dashes: "  "+"-"*60. Percentage printed as `{r['percentage']:>7.1f}%`. Waits on `input("Press Enter...")`.

### Layout fmts (memorize)

- `f"{SCHOOL_NAME}  |  REPORT CARD GENERATOR"` — menu banner text
- `f"   Name        : {res['name']}"`
- `f"   Roll No.    : {res['roll']}"`
- `f"   Class/Sec   : {res['class']} - {res['section']}"`
- `f"   Overall Rank: {rank}/{len(ranks['overall'])}"`
- Subject row: `f"  {s['name']:<14}{s['theory']:>8}{s['practical']:>6}{t:>9}{s['max']:>6}{s['grade']:>7}{sr:>6}"`
- List row: `f"  {r['Roll Number']:<6}{r['Student Name']:<22}{r['percentage']:>7.1f}%{r['grade']:>7}{r['overall_rank']:>7}{r['status']:>9}"`

### Notes

- `res` = single-student dict from `calculate_results(row)`
- `ranks` = `{"overall": {roll: rank}, "subjects": {"English": {roll: rank}, ...}}`
- `data` arg of `display_all_students` = already-processed DataFrame
