import csv, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_PATH = os.path.join(DATA_DIR, "students.csv")

STUDENTS = [
    ["Aarav Sharma",   101, 11, "A", 88, 79, 95, 91, 98],
    ["Diya Patel",     102, 11, "A", 92, 85, 78, 89, 94],
    ["Vivaan Gupta",   103, 11, "A", 74, 68, 81, 77, 88],
    ["Ananya Singh",   104, 11, "A", 95, 91, 97, 93, 96],
    ["Reyansh Kumar",  105, 11, "A", 61, 55, 49, 58, 72],
    ["Ishita Reddy",   106, 11, "B", 84, 80, 88, 82, 90],
    ["Kabir Mehta",    107, 11, "B", 70, 65, 73, 68, 85],
    ["Saanvi Iyer",    108, 11, "B", 90, 88, 84, 91, 93],
    ["Arjun Nair",     109, 11, "B", 55, 28, 42, 31, 65],   
    ["Myra Khanna",    110, 11, "B", 86, 82, 89, 87, 95],
]
HEADERS = ["Student Name","Roll Number","Class","Section",
           "English","Hindi","Mathematics","Science","Computer/AI"]

def generate_csv(path=CSV_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(STUDENTS)
    print(f"[OK] CSV created with {len(STUDENTS)} records -> {path}")
    return path

if __name__ == "__main__":
    generate_csv()