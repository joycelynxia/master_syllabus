import re
import pdfplumber

pdf_path = "syllabus_samples/example1.pdf"

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

def extract_professor_info(text: str) -> dict:
    lines = text.splitlines()
    professor_info = {}

    for line in lines:
        line = line.strip()
        
        name_match = re.search(
            r'\b(?:Instructor|Lecturer|Professor|Prof\.?|Dr\.?):?\s+([A-Z][a-zA-Z\'\-]+(?:\s[A-Z][a-zA-Z\'\-]+)+)',
            line
        )
        if name_match:
            professor_info["name"] = name_match.group(1).strip()
            if '@' in line:
                email_match = re.search(r'[\w\.-]+@[\w\.-]+', line)
                professor_info["email"] = email_match.group()
                return professor_info
                
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', line)
        if "Email:" in line:
            professor_info["email"] = email_match.group()
        
            
        # if "Office Hours" in line:
        #     matches = re.findall(r'\b(?:Mon|Tue|Tues|Wed|Thu|Thurs|Fri|Sat|Sun)(?:day)?s?\.?\b[^:\n]*\d{1,2}:\d{2}', line)
        #     professor_info["office_hours"] = matches
    return professor_info


def extract_assignments(text: str) -> list[dict]:
    lines = text.splitlines()
    
    assignments = []
    date_pattern = r'(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s?\d{1,2})|\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?'
    keywords = ["homework", "hw", "exam", "midterm", "final", "assigment", "test", "project", "quiz", "lab", "discussion board", "discussion forum"]
    
    for line in lines: 
        lower = line.lower()
        if any(word in lower for word in keywords):
            date_match = re.search(date_pattern, line)
            if date_match:
                assignments.append({
                    "title": line.strip(),
                    "due_date": date_match.group()
                })
                
    return assignments

def extract_exams(text: str) -> list[dict]:
    return 


prof_info = (extract_professor_info(full_text))
assignments = (extract_assignments(full_text))

for key, val in prof_info.items():
    print(key + ': ' + val)
    
for assignment in assignments:
    title, due_date = assignment.values()
    print(title)
    print("\tdue date:", due_date)
        