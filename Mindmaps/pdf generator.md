## pdf_generator (ReportLab)

**Libraries** ->

from datetime import datetime

import os

from graph_generator import generate_all_charts

from reportlab.lib import colors

from reportlab.lib.enums import TA_CENTER, TA_LEFT

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from reportlab.lib.units import cm

from reportlab.platypus import (HRFlowable, Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

### Constants

SCHOOL_NAME = "GD Goenka School, Muzaffarnagar"

SCHOOL_ADDR = "8th km Stone, Jansath Road, Muzaffarnagar"

OUTPUT_DIR  = os.path.join(dirname(__file__), "output")

File pattern -> `ReportCard_{roll}_{name_with_underscores}.pdf`

### Color Codes (HexColor)

NAVY  = #1A237E    (headers, section heads, default tile)

GOLD  = #C9A227    (HR, title, GRADE tile, total row, signature box border)

LIGHT = #EEF2F7    (label cols, summary bg, alt row stripe)

GREEN = #2E7D32    (PASS status)

RED   = #C62828    (FAIL status)

FAIL_BG     = #FFCDD2    (failing subject row bg)

REMARKS_BG = #FFF9E6    (remarks panel bg)

Other: colors.white, colors.grey, colors.lightgrey, colors.black

### Document setup (SimpleDocTemplate)

pagesize    = A4

leftMargin  = 2.3 cm

rightMargin = 2.3 cm

topMargin    = 1.2 cm

bottomMargin = 1.2 cm

title = f"Report Card - {res['name']}",  author = SCHOOL_NAME

### Styles (ParagraphStyle, parent=ss[...])

| Name          | Parent       | Font            | Size | Color        | Align      | Extras |
|---------------|--------------|-----------------|------|--------------|------------|--------|
| school        | ss["Title"]  | Helvetica-Bold  | 18   | NAVY         | TA_CENTER  | — |
| addr          | ss["Normal"] | —               | 9    | colors.grey  | TA_CENTER  | — |
| title         | ss["Title"]  | Helvetica-Bold  | 13   | GOLD         | TA_CENTER  | — |
| subtitle      | ss["Normal"] | —               | 9    | NAVY         | TA_CENTER  | — |
| section_head  | ss["Heading2"] | Helvetica-Bold | 10  | colors.white | TA_LEFT    | leftIndent=4, leading=14 |
| body          | ss["Normal"] | —               | 9    | —            | —          | leading=12 |
| small         | ss["Normal"] | —               | 8    | colors.grey  | —          | — |
| remark        | ss["Normal"] | —               | 9    | NAVY         | —          | leading=13, leftIndent=4, rightIndent=4 |

### Functions

**_build_styles()** -> returns dict of 8 ParagraphStyle objects (see table above).

**_header(s)** -> [Paragraph(SCHOOL_NAME, school), Paragraph(SCHOOL_ADDR, addr), HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceBefore=2, spaceAfter=4), Paragraph("ANNUAL PERFORMANCE REPORT", title), Paragraph(f"Session 2026-27 | Class XI | Issued: {datetime.now().strftime('%d %B %Y')}", subtitle), Spacer(1, 4)]

**_section_head(text, s)** -> Table([[Paragraph(text, section_head)]], colWidths=[16.4*cm]) with TableStyle:
  - BACKGROUND NAVY (0,0)–(-1,-1)
  - LEFTPADDING 6
  - TOPPADDING 3, BOTTOMPADDING 3
  Returns [t, Spacer(1, 4)]

**_student_details(res, ranks, s)** -> 3x4 grid Table:

  Row 1: Name | value | Roll Number | value

  Row 2: Class | value | Section | value

  Row 3: Overall Rank | f"{rk}/{n}" | Result | f"<b>{status}</b>"

  colWidths = [3.2, 5, 3.2, 5] cm

  TableStyle:
  - BACKGROUND col 0 and col 2 = LIGHT (label cols)
  - GRID (0,0)–(-1,-1) 0.5, colors.lightgrey
  - VALIGN MIDDLE
  - LEFTPADDING/RIGHTPADDING 6
  - TOPPADDING/BOTTOMPADDING 4

  Returns [t, Spacer(1, 6)]

**_subject_table(res, ranks, s)** -> Table with header + 5 subject rows + TOTAL row.

  Columns: Subject, Theory(/80), Practical(/20), Total(/100), Grade, Rank

  colWidths = [4.2, 2.4, 2.4, 2.4, 2, 3] cm   (sum = 16.4 cm, repeatRows=1)

  TableStyle:
  - Header row (0,0)–(-1,0): BG NAVY, TEXTCOLOR white, Helvetica-Bold, size 9, CENTER align
  - Body (0,1)–(-1,-2): Helvetica, size 9, (1,1)–(-1,-1) CENTER, (0,1)–(0,-1) LEFT
  - Total row (0,-1)–(-1,-1): BG GOLD, white, Helvetica-Bold
  - GRID (0,0)–(-1,-1) 0.5, colors.grey
  - ROWBACKGROUNDS (0,1)–(-1,-2) [white, LIGHT]   (zebra stripes)
  - VALIGN MIDDLE, TOPPADDING/BOTTOMPADDING 4
  - Fail rows (subject total < 33): BACKGROUND #FFCDD2

  Returns [t, Spacer(1, 6)]

**_summary_block(res, ranks, s)** -> 6 tiles in one row.

  Inner `tile(label, value, vc=NAVY)`:
    Table([
      [Paragraph(f"<b>{value}</b>", ParagraphStyle("v", parent=body, fontSize=12, textColor=vc, alignment=TA_CENTER))],
      [Paragraph(label, ParagraphStyle("l", parent=small, alignment=TA_CENTER))],
    ], colWidths=[2.6*cm], rowHeights=[0.8*cm, 0.4*cm])

  Tiles: TOTAL / AVERAGE / PERCENTAGE / GRADE(vc=GOLD) / RANK / STATUS(vc=GREEN if PASS else RED)

  Outer Table([row], colWidths=[2.73*cm]*6)   (sum ≈ 16.4 cm)

  TableStyle: BOX 0.5 lightgrey, INNERGRID 0.5 lightgrey, VALIGN MIDDLE, BACKGROUND LIGHT.

  Returns [t, Spacer(1, 6)]

**_charts_section(res, s)** -> bar, pie = generate_all_charts(res)

  bi = Image(bar, width=9*cm, height=4.8*cm)

  pi = Image(pie, width=7.2*cm, height=4.8*cm)

  Table([[bi, pi]], colWidths=[9.2*cm, 7.2*cm])

  TableStyle: VALIGN MIDDLE, ALIGN CENTER

  Returns [t, Spacer(1, 6)]

**_remarks_block(res, s)** -> text = f"<b>Remarks:</b> {remarks}<br/><b>Class Teacher's Note:</b> __________________"

  Panel Table([[Paragraph(text, remark)]], colWidths=[16.4*cm])
  TableStyle: BACKGROUND #FFF9E6, BOX 0.6 GOLD, LEFTPADDING/RIGHTPADDING 8, TOPPADDING/BOTTOMPADDING 4

  Signature Table: 2 rows × 3 cols
  Row 0: empty (with LINEABOVE 0.6 black on each cell) — height 0.8*cm
  Row 1: ["Class Teacher", "Principal", "Parent / Guardian"] — height 0.4*cm, ALIGN CENTER, FONTSIZE 8, TEXTCOLOR grey
  colWidths = [5.46*cm]*3   (sum ≈ 16.4 cm)

  Footer Paragraph: "<i>Computer-generated report card. Generated by Smart Student Report Card Generator.</i>" (small)

  Returns [panel, Spacer(1, 8), sig, Spacer(1, 4), footer]

**generate_pdf(res, ranks, output_path=None)** -> os.makedirs(OUTPUT_DIR, exist_ok=True)
  If output_path is None:
    safe_name = res["name"].replace(" ", "_")
    output_path = OUTPUT_DIR/f"ReportCard_{res['roll']}_{safe_name}.pdf"
  Builds SimpleDocTemplate, then story:
    _header(s) → _section_head("STUDENT DETAILS") → _student_details
    _section_head("SUBJECT-WISE PERFORMANCE") → _subject_table
    _section_head("RESULT SUMMARY") → _summary_block
    _section_head("PERFORMANCE CHARTS") → _charts_section
    _section_head("REMARKS & SIGNATURES") → _remarks_block
  doc.build(story)
  CLEANUP: os.remove(bar_{roll}.png); os.remove(pie_{roll}.png)
  Returns output_path

### Width math (memorize)

- Page width A4 = 21 cm ; minus 2×2.3 cm margins = 16.4 cm usable. Most "full-width" tables use 16.4*cm.
- Subject table cols: 4.2 + 2.4 + 2.4 + 2.4 + 2 + 3 = 16.4 cm ✓
- Summary tiles: 2.73 × 6 = 16.38 cm ≈ 16.4 cm ✓
- Chart row: 9.2 + 7.2 = 16.4 cm ✓
- Signature row: 5.46 × 3 = 16.38 cm ≈ 16.4 cm ✓
- Student details: 3.2 + 5 + 3.2 + 5 = 16.4 cm ✓

### Notes

- Chart PNGs are deleted at end of generate_pdf — they are intermediate artifacts only.
- Date format string: `"%d %B %Y"`  (e.g. "31 August 2026").
- Session string is hardcoded "Session 2026-27" (NOT current year).
- All "value" labels use `<b>...</b>` for emphasis inside Paragraph.
- Section heads always: NAVY bg, white text, Helvetica-Bold 10, leftIndent 4, leading 14, padding 3/3.
