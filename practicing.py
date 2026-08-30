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
import pandas as pd
'''doc = SimpleDocTemplate('output.pdf', pagesize = A4, leftMargin = 2.3*cm, rightMargin = 2.3*cm, topMargin = 1.2*cm, bottomMargin = 1.2*cm)

style = []
style.append(Paragraph('Above'))
style.append(HRFlowable(width='80%' ,hAlign=TA_CENTER, thickness=1, color=colors.gold, ))
style.append(Paragraph('Below'))

doc.build(style)
'''

GRADE_THRESHOLDS = {
    "A1": 90, "A2": 80, "B1": 70, "B2": 60,
    "C1": 50, "C2": 40, "D":  0,
}

Subjects =["English", "Hindi", "Mathematics", "Science", "Computer/AI"]
# ------------------------- GRADE HELPER -----------------------
def get_grade(pct):
    for grade, thr in GRADE_THRESHOLDS.items():
        if pct >= thr:
            return grade
    return "D"

def load_data(file):
    if not os.path.exists(file):
        raise FileNotFoundError('GIVE CORRECT FILE BROTHER')
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    for subject in Subjects:
        df[subject] = pd.to_numeric(df[subject], errors = 'coerce').fillna(0).astype(int)
    df['Roll Number'] = df['Roll Number'].astype(int)
    df['Class'] = df['Class'].astype(int)
    return df

def process_data(df):
    for subject in Subjects:
        df[f'{subject}_theory'] = (df[subject]*0.8).round().astype(int).clip(lower=0, upper=80)
        df[f'{subject}_internal'] = (df[subject] - df[f'{subject}_theory']).round().astype(int).clip(lower=0, upper=20)

    df['grand_total'] = df[Subjects].sum(axis=1)
    df['max_total'] = 100*len(Subjects)
    df['percentage'] = (df['grand_total']/df['max_total'] *100).round(2).astype(float)

    df['grade'] = df['percentage'].apply(get_grade)

    df['overall_rank'] = df['grand_total'].rank(ascending = False, method = 'min').astype(int)

    df['status'] = df[Subjects].apply(lambda x: 'PASS' if x.min() >= 33 else 'FAIL')

    for s in Subjects:
        df[f'{s}_rank'] = df[s].rank(ascending = False, method = 'min').astype(int)

    return df
df = load_data('students.csv')
df2 = process_data(df)

def get_ranks(df):
    overall = dict(zip(df['Roll Number'], df['overall_rank']))
    subject_ranks = {s: dict(zip(df['Roll Number'], df[f'{s}_rank'])) for s in Subjects}
    return {'overall' : overall, 'subjectwise': subject_ranks}







# PDF Generator

NAVY = colors.HexColor("#1A237E")
GOLD = colors.HexColor("#C9A227")
LIGHT = colors.HexColor("#EEF2F7")
GREEN = colors.HexColor("#2E7D32")
RED = colors.HexColor("#C62828")


def get_styles():
    ss = getSampleStyleSheet()
    return {'school' :
            ParagraphStyle('school', parent = ss['Title'], fontName = 'Helvetica-Bold', fontSize = 18, textColor = NAVY,
                           alignment = TA_CENTER)
            , 'title':
            ParagraphStyle('title', parent = ss['Title'], fontName = 'Helvetica-Bold', fontSize = 13, textColor = GOLD,
                           alignment = TA_CENTER)
            , 'addr':
            ParagraphStyle('addr', parent = ss['Normal'], fontSize = 9, textColor = colors.grey, alignment = TA_CENTER)
            , 'body':
            ParagraphStyle('body', parent = ss['Normal'], fontSize = 9, leading = 12)
            , 'remark':
            ParagraphStyle('remark', parent = ss['Normal'], fontSize = 9, leading = 13, textColor = NAVY, righindent = 4,
                           leftindent = 4)
            , 'subtitle':
            ParagraphStyle('subtitle', parent = ss['Normal'], fontSize = 10, alignment = TA_CENTER, textColor = colors.white,
                           font = 'Helvetica-Bold')
            , 'section_header':
            ParagraphStyle('section_header', parent = ss['Heading2'], leading = 14, alignment = TA_LEFT, textColor = colors.white)

            }



def _header(s:dict):
    return [
        Paragraph('SCHOOL', s['school']),
        Paragraph('ADRRESS', s['addr']),
        HRFlowable(width = '100%', thickness = 1.2, spaceBefore = 2, spaceAfter = 4, color = GOLD),

        Paragraph('TITLE', s['title']),

        Paragraph(f'Academic Session: 2026-2027 | Issued On: {datetime.now().strftime("%d %m %y")}', s['subtitle']),
        Spacer(1,4)]


def _section_header(text:str, s:dict):
    t = ([[ParagraphStyle(text, s['section_header'])]], colwidth = 16.4 *cm)
    t.setStyle(TableStyle[
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)]
    return [t, spacer(1,4)]







