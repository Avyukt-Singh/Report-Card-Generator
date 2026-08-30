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
)

SCHOOL_NAME = "GD Goenka School, Muzaffarnagar"
SCHOOL_ADDR = "8th km Stone, Jansath Road, Muzaffarnagar"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

NAVY = colors.HexColor("#1A237E")
GOLD = colors.HexColor("#C9A227")
LIGHT = colors.HexColor("#EEF2F7")
GREEN = colors.HexColor("#2E7D32")
RED = colors.HexColor("#C62828")


def _build_styles():
  ss = getSampleStyleSheet()
  return {
      "school": ParagraphStyle(   
          "school",
          parent=ss["Title"],
          fontName="Helvetica-Bold",
          fontSize=18,
          textColor=NAVY,
          alignment=TA_CENTER,
      ),
      "addr": ParagraphStyle(
          "addr",
          parent=ss["Normal"],
          fontSize=9,
          textColor=colors.grey,
          alignment=TA_CENTER,
      ),
      "title": ParagraphStyle(
          "title",
          parent=ss["Title"],
          fontName="Helvetica-Bold",
          fontSize=13,
          textColor=GOLD,
          alignment=TA_CENTER,
      ),
      "subtitle": ParagraphStyle(
          "subtitle",
          parent=ss["Normal"],
          fontSize=9,
          textColor=NAVY,
          alignment=TA_CENTER,
      ),
      "section_head": ParagraphStyle(
          "section_head",
          parent=ss["Heading2"],
          fontName="Helvetica-Bold",
          fontSize=10,
          textColor=colors.white,
          alignment=TA_LEFT,
          leftIndent=4,
          leading=14,
      ),
      "body": ParagraphStyle("body", parent=ss["Normal"], fontSize=9, leading=12),
      "small": ParagraphStyle(
          "small", parent=ss["Normal"], fontSize=8, textColor=colors.grey
      ),
      "remark": ParagraphStyle(
          "remark",
          parent=ss["Normal"],
          fontSize=9,
          leading=13,
          textColor=NAVY,
          leftIndent=4,
          rightIndent=4,
      ),
  }


def _header(s):
  return [
      Paragraph(SCHOOL_NAME, s["school"]),
      Paragraph(SCHOOL_ADDR, s["addr"]),
      HRFlowable(
          width="100%", thickness=1.2, color=GOLD, spaceBefore=2, spaceAfter=4
      ),
      Paragraph("ANNUAL PERFORMANCE REPORT", s["title"]),
      Paragraph(
          f"Session 2026-27 | Class XI | Issued:"
          f" {datetime.now().strftime('%d %B %Y')}",
          s["subtitle"],
      ),
      Spacer(1, 4),
  ]


def _section_head(text, s):
  t = Table([[Paragraph(text, s["section_head"])]], colWidths=[16.4 * cm])
  t.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, -1), NAVY),
          ("LEFTPADDING", (0, 0), (-1, -1), 6),
          ("TOPPADDING", (0, 0), (-1, -1), 3),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
      ])
  )
  return [t, Spacer(1, 4)]


def _student_details(res, ranks, s):
  rk = ranks["overall"].get(res["roll"], "-")
  n = len(ranks["overall"])
  data = [
      [
          Paragraph("<b>Student Name</b>", s["body"]),
          Paragraph(res["name"], s["body"]),
          Paragraph("<b>Roll Number</b>", s["body"]),
          Paragraph(str(res["roll"]), s["body"]),
      ],
      [
          Paragraph("<b>Class</b>", s["body"]),
          Paragraph(str(res["class"]), s["body"]),
          Paragraph("<b>Section</b>", s["body"]),
          Paragraph(res["section"], s["body"]),
      ],
      [
          Paragraph("<b>Overall Rank</b>", s["body"]),
          Paragraph(f"{rk} / {n}", s["body"]),
          Paragraph("<b>Result</b>", s["body"]),
          Paragraph(f"<b>{res['status']}</b>", s["body"]),
      ],
  ]
  t = Table(data, colWidths=[3.2 * cm, 5 * cm, 3.2 * cm, 5 * cm])
  t.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (0, -1), LIGHT),
          ("BACKGROUND", (2, 0), (2, -1), LIGHT),
          ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("LEFTPADDING", (0, 0), (-1, -1), 6),
          ("RIGHTPADDING", (0, 0), (-1, -1), 6),
          ("TOPPADDING", (0, 0), (-1, -1), 4),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
      ])
  )
  return [t, Spacer(1, 6)]


def _subject_table(res, ranks, s):
  head = [
      "Subject",
      "Theory\n(/80)",
      "Practical\n(/20)",
      "Total\n(/100)",
      "Grade",
      "Rank",
  ]
  rows = [head]
  for sub in res["subjects"]:
    sr = ranks["subjects"].get(sub["name"], {}).get(res["roll"], "-")
    rows.append([
        sub["name"],
        str(sub["theory"]),
        str(sub["practical"]),
        str(sub["total"]),
        sub["grade"],
        str(sr),
    ])
  th = sum(x["theory"] for x in res["subjects"])
  tp = sum(x["practical"] for x in res["subjects"])
  rows.append([
      "TOTAL",
      str(th),
      str(tp),
      str(res["total"]),
      res["grade"],
      str(ranks["overall"].get(res["roll"], "-")),
  ])

  t = Table(rows, colWidths=[4.2 * cm, 2.4 * cm, 2.4 * cm, 2.4 * cm, 2 * cm, 3 * cm], repeatRows=1)
  fail_rows = [
      ("BACKGROUND", (0, i + 1), (-1, i + 1), colors.HexColor("#FFCDD2"))
      for i, x in enumerate(res["subjects"])
      if x["total"] < 33
  ]
  t.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, 0), NAVY),
          ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
          ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
          ("FONTSIZE", (0, 0), (-1, 0), 9),
          ("ALIGN", (0, 0), (-1, 0), "CENTER"),
          ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
          ("FONTSIZE", (0, 1), (-1, -1), 9),
          ("ALIGN", (1, 1), (-1, -1), "CENTER"),
          ("ALIGN", (0, 1), (0, -1), "LEFT"),
          ("BACKGROUND", (0, -1), (-1, -1), GOLD),
          ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
          ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
          ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
          ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, LIGHT]),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 4),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
      ] + fail_rows)
  )
  return [t, Spacer(1, 6)]


def _summary_block(res, ranks, s):
  rk = ranks["overall"].get(res["roll"], "-")
  n = len(ranks["overall"])

  def tile(label, value, vc=NAVY):
    return Table(
        [
            [
                Paragraph(
                    f"<b>{value}</b>",
                    ParagraphStyle(
                        "v", parent=s["body"], fontSize=12, textColor=vc, alignment=TA_CENTER
                    ),
                )
            ],
            [
                Paragraph(
                    label, ParagraphStyle("l", parent=s["small"], alignment=TA_CENTER)
                )
            ],
        ],
        colWidths=[2.6 * cm],
        rowHeights=[0.8 * cm, 0.4 * cm],
    )

  sc = GREEN if res["status"] == "PASS" else RED
  row = [
      tile("TOTAL", f"{res['total']}/{res['max_total']}"),
      tile("AVERAGE", f"{res['average']}"),
      tile("PERCENTAGE", f"{res['percentage']}%"),
      tile("GRADE", res["grade"], GOLD),
      tile("RANK", f"{rk}/{n}"),
      tile("STATUS", res["status"], sc),
  ]
  t = Table([row], colWidths=[2.73 * cm] * 6)
  t.setStyle(
      TableStyle([
          ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
          ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
      ])
  )
  return [t, Spacer(1, 6)]


def _charts_section(res, s):
  bar, pie = generate_all_charts(res)
  bi = Image(bar, width=9 * cm, height=4.8 * cm)
  pi = Image(pie, width=7.2 * cm, height=4.8 * cm)
  t = Table([[bi, pi]], colWidths=[9.2 * cm, 7.2 * cm])
  t.setStyle(
      TableStyle([
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("ALIGN", (0, 0), (-1, -1), "CENTER"),
      ])
  )
  return [t, Spacer(1, 6)]


def _remarks_block(res, s):
  text = (
      f"<b>Remarks:</b> {res['remarks']}<br/>"
      f"<b>Class Teacher's Note:</b> Performance reflects consistent effort."
  )
  panel = Table([[Paragraph(text, s["remark"])]], colWidths=[16.4 * cm])
  panel.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF9E6")),
          ("BOX", (0, 0), (-1, -1), 0.6, GOLD),
          ("LEFTPADDING", (0, 0), (-1, -1), 8),
          ("RIGHTPADDING", (0, 0), (-1, -1), 8),
          ("TOPPADDING", (0, 0), (-1, -1), 4),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
      ])
  )
  sig = Table(
      [["", "", ""], ["Class Teacher", "Principal", "Parent / Guardian"]],
      colWidths=[5.46 * cm] * 3,
      rowHeights=[0.8 * cm, 0.4 * cm],
  )
  sig.setStyle(
      TableStyle([
          ("LINEABOVE", (0, 0), (0, 0), 0.6, colors.black),
          ("LINEABOVE", (1, 0), (1, 0), 0.6, colors.black),
          ("LINEABOVE", (2, 0), (2, 0), 0.6, colors.black),
          ("ALIGN", (0, 1), (-1, 1), "CENTER"),
          ("FONTSIZE", (0, 1), (-1, 1), 8),
          ("TEXTCOLOR", (0, 1), (-1, 1), colors.grey),
      ])
  )
  footer = Paragraph(
      "<i>Computer-generated report card. Generated by Smart Student Report"
      " Card Generator.</i>",
      s["small"],
  )
  return [panel, Spacer(1, 8), sig, Spacer(1, 4), footer]


def generate_pdf(res, ranks, output_path=None):
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  if output_path is None:
    safe_name = res["name"].replace(" ", "_")
    output_path = os.path.join(
        OUTPUT_DIR, f"ReportCard_{res['roll']}_{safe_name}.pdf"
    )
  doc = SimpleDocTemplate(
      output_path,
      pagesize=A4,
      leftMargin=2.3 * cm,
      rightMargin=2.3 * cm,
      topMargin=1.2 * cm,
      bottomMargin=1.2 * cm,
      title=f"Report Card - {res['name']}",
      author=SCHOOL_NAME,
  )
  s = _build_styles()
  story = []
  story += _header(s)
  story += _section_head("STUDENT DETAILS", s)
  story += _student_details(res, ranks, s)
  story += _section_head("SUBJECT-WISE PERFORMANCE", s)
  story += _subject_table(res, ranks, s)
  story += _section_head("RESULT SUMMARY", s)
  story += _summary_block(res, ranks, s)
  story += _section_head("PERFORMANCE CHARTS", s)
  story += _charts_section(res, s)
  story += _section_head("REMARKS & SIGNATURES", s)
  story += _remarks_block(res, s)
  doc.build(story)
  return output_path