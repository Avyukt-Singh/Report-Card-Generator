## generate_csv

**Libraries** ->

import csv, os

### Paths

DATA_DIR  = os.path.join(dirname(__file__), "data")

CSV_PATH  = os.path.join(DATA_DIR, "students.csv")

### Headers (order matters!)

HEADERS = ["Student Name", "Roll Number", "Class", "Section",

           "English", "Hindi", "Mathematics", "Science", "Computer/AI"]

### Sample Students (10 rows)

STUDENTS = [

  ["Aarav Sharma",   101, 11, "A", 88, 79, 95, 91, 98],

  ["Diya Patel",     102, 11, "A", 92, 85, 78, 89, 94],

  ["Vivaan Gupta",   103, 11, "A", 74, 68, 81, 77, 88],

  ["Ananya Singh",   104, 11, "A", 95, 91, 97, 93, 96],

  ["Reyansh Kumar",  105, 11, "A", 61, 55, 49, 58, 72],

  ["Ishita Reddy",   106, 11, "B", 84, 80, 88, 82, 90],

  ["Kabir Mehta",    107, 11, "B", 70, 65, 73, 68, 85],

  ["Saanvi Iyer",    108, 11, "B", 90, 88, 84, 91, 93],

  ["Arjun Nair",     109, 11, "B", 55, 28, 42, 31, 65],   # FAIL (Hindi 28 < 33)

  ["Myra Khanna",    110, 11, "B", 86, 82, 89, 87, 95],

]

Row format: [Name, Roll, Class, Section, English, Hindi, Math, Science, Computer/AI]

### Functions

**generate_csv(path=CSV_PATH)** -> os.makedirs(data, exist_ok=True); open(path, "w", newline="", encoding="utf-8"); csv.writer; writes HEADERS + STUDENTS rows; prints "[OK] CSV created with {N} records -> {path}"; returns path.

**__main__** -> calls generate_csv()

### Notes

- Class is always 11, Sections A (rolls 101–105) and B (rolls 106–110).
- Roll numbers 101–110 sequential.
- Marks are /100 (subject_max). Pass mark 33.
- Only Arjun Nair (109) fails (Hindi=28, Science=31, both < 33).
