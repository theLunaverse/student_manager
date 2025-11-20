class Student:
    def __init__(self, student_id, name, mark1, mark2, mark3, exam_mark):
        self.student_id = int(student_id)
        self.name = name
        self.mark1 = int(mark1)
        self.mark2 = int(mark2)
        self.mark3 = int(mark3)
        self.exam_mark = int(exam_mark)
    
    @property
    def coursework_total(self):
        return self.mark1 + self.mark2 + self.mark3
    
    @property
    def total_score(self):
        return self.coursework_total + self.exam_mark
    
    @property
    def percentage(self):
        return (self.total_score / 160) * 100
    
    @property
    def grade(self):
        perc = self.percentage
        if perc >= 70: return 'A'
        elif perc >= 60: return 'B'
        elif perc >= 50: return 'C'
        elif perc >= 40: return 'D'
        else: return 'F'