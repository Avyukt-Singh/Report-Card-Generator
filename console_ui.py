from utils import print_banner, clear_screen

SCHOOL_NAME = "GD Goenka School"
SCHOOL_ADDR = "8th KM Stone, Jansath Road, Muzaffarnagar"

def show_menu():
    clear_screen()
    print_banner(f"{SCHOOL_NAME}  |  REPORT CARD GENERATOR", "=")
    print(f"  {SCHOOL_ADDR}")
    print("="*72 + "\n")
    print("  1.  Search Student (Name or Roll No.)")
    print("  2.  List All Students")
    print("  3.  Generate PDF Report Card")
    print("  4.  Generate Bar + Pie Charts")
    print("  5.  Exit\n" + "="*72)

def display_student_card(res, ranks):
    clear_screen()
    print_banner(SCHOOL_NAME, "=")
    print(f"  {SCHOOL_ADDR}")
    print("  ANNUAL PERFORMANCE REPORT - Class XI")
    print("="*72)
    print("\n  STUDENT DETAILS")
    print(f"   Name        : {res['name']}")
    print(f"   Roll No.    : {res['roll']}")
    print(f"   Class/Sec   : {res['class']} - {res['section']}")
    rank = ranks["overall"].get(res["roll"], "-")
    print(f"   Overall Rank: {rank}/{len(ranks['overall'])}\n")
    
    print("  SUBJECT-WISE MARKS")
    print(f"  {'Subject':<14}{'Theory':>8}{'Prac':>6}{'Total':>8}"
          f"{'Max':>6}{'Grade':>7}{'Rank':>6}")
    print("  "+"-"*60)
    for s in res["subjects"]:
        sr = ranks["subjects"].get(s["name"],{}).get(res["roll"],"-")
        t = str(s["total"])
        print(f"  {s['name']:<14}{s['theory']:>8}{s['practical']:>6}"
              f"{t:>9}{s['max']:>6}{s['grade']:>7}{sr:>6}")
    print("\n  "+"-"*60)
    
    print("  SUMMARY")
    print(f"   Grand Total : {res['total']}/{res['max_total']}")
    print(f"   Average     : {res['average']}")
    print(f"   Percentage  : {res['percentage']}%")
    print(f"   Grade       : {res['grade']}")
    print(f"   Result      : {res['status']}")
    
    print("\n  REMARKS")
    print(f"   {res['remarks']}\n" + "="*72 + "\n")

def display_all_students(data):
    """data is the processed DataFrame — ranks, grades, status are already columns."""
    clear_screen()
    print_banner(f"{SCHOOL_NAME} | ALL STUDENTS","=")
    print(f"  {'Roll':<6}{'Name':<22}{'%':>8}{'Grade':>7}{'Rank':>7}{'Status':>9}")
    print("  "+"-"*60)
    for _, r in data.iterrows():
        print(f"  {r['Roll Number']:<6}{r['Student Name']:<22}{r['percentage']:>7.1f}%"
              f"{r['grade']:>7}{r['overall_rank']:>7}{r['status']:>9}")
    input("\n  Press Enter to return...")