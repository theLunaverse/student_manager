import os
from modules.constants import DATA_FILE
from modules.student import Student

def load_students():
    """Load student data from file"""
    students = []
    try:
        with open(DATA_FILE, "r") as file:
            for line in file:
                data = line.strip().split(',')
                if len(data) == 6:
                    # Remove any extra whitespace
                    clean_data = [item.strip() for item in data]
                    student = Student(clean_data[0], clean_data[1], clean_data[2], 
                                    clean_data[3], clean_data[4], clean_data[5])
                    students.append(student)
        print(f"Loaded {len(students)} student records")
    except FileNotFoundError:
        print(f"File not found at: {DATA_FILE}")
    except Exception as e:
        print(f"Error loading data: {e}")
    return students

def save_students(students):
    """Save student data to file"""
    try:
        # Create media directory if it doesn't exist
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        with open(DATA_FILE, "w") as file:
            for student in students:
                file.write(f"{student.student_id},{student.name},{student.mark1},"
                        f"{student.mark2},{student.mark3},{student.exam_mark}\n")
        print(f"Saved {len(students)} student records")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False