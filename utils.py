import os

class Colors:
    HEADER    = "\033[95m"; BLUE   = "\033[94m"; CYAN   = "\033[96m"
    GREEN     = "\033[92m"; YELLOW = "\033[93m"; RED    = "\033[91m"
    BOLD      = "\033[1m";  UNDERLINE = "\033[4m"; RESET = "\033[0m"

def color(text, code):           return f"{code}{text}{Colors.RESET}"
def clear_screen():               os.system("cls" if os.name == "nt" else "clear")
def print_banner(text, ch="=", w=72):
    print(ch*w); print(text.center(w)); print(ch*w)

GRADE_TABLE = [
    (90,"A1","Outstanding performance. Keep it up!"),
    (80,"A2","Excellent work. Aim for the next band."),
    (70,"B1","Very good. Push harder in weaker subjects."),
    (60,"B2","Good effort. Solidify concepts for top grade."),
    (50,"C1","Fair. Focus on consistent practice."),
    (40,"C2","Average. Needs structured revision."),
    (0, "D", "Needs improvement. Please seek guidance."),
]
def get_grade(pct):
    for thr,g,_ in GRADE_TABLE:
        if pct >= thr: return g
    return "D"
def get_remarks(pct):
    for thr,_,r in GRADE_TABLE:
        if pct >= thr: return r
    return "Needs improvement."