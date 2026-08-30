## Reportlab

**Libraries** -> 

from datetime import datetime

import os

from graph_generator import generate_all_charts

from reportlab.lib import colors

from reportlab.lib.enums import TA_CENTER, TA_LEFT

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from reportlab.lib.units import cm

from reportlab.platypus import (

HRFlowable,

Image,

Paragraph,

SimpleDocTemplate,

Spacer,

Table,

TableStyle,

### Color Codes:

NAVY = colors.HexColor("#1A237E")

GOLD = colors.HexColor("#C9A227")

LIGHT = colors.HexColor("#EEF2F7")

GREEN = colors.HexColor("#2E7D32")

RED = colors.HexColor("#C62828")

FAIL = colors.HexColor("#FFCDD2"))

Remarks = colors.HexColor("#FFF9E6")

### Functions

**create_styles()** -> title, school, body, subtitle, addr, remark, small, section_header

**create_header(s)** -> SCHOOL, Addr, HRFlowable, Subtext, Spacer

**section_head(text, s)** -> Section Head, NAVY, LP (6), TP and BP (3), Spacer 

**student_details(res, ranks, s)** -> Student Name, RN, Class Section, Roll Number, Result; Light BG, lightgrey Grid (0.5), VALIGN, LP and RP (6), TP and BP (4), Spacer(1, 6)

**subject_table(res, ranks, s)** -> Head, Fail rows, Table

**summary_block(res, ranks, s)** -> til(label, value, vc=NAVY) -> One Coulmn like tile (Colwidth = 2.2*cm, Row height = 0.8*cmm, 0.4\*cm) -> Table (2.73\*cm), Box (lightgrey, 0.5), Innergrid (lightgrey, 0.5), Spacer(1, 6)

**charts_section(res, s)** -> generate_all_charts(res) -> 9 + 7.2 -> 9.2 + 7.2, Spacer(1,6)

**remarks(res, s)** -> text, Table: BG, Gold Box (0.6), LP & RP (0.8), TP & BP (0.4), Spacer(1,8) ;; sig Table (5.46\*3, 0.8,0.4), Lineabove, Center Align, 8 Font size 5, grey,Spacer(1.4); footer

**generate_pdf(res, rank, output_path = None)** 




























