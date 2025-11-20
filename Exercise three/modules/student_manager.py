import tkinter as tk
from .constants import *
from .student import Student
from .file_manager import load_students, save_students

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        
        self.bg = self.load_image(BG_IMAGE, WIDTH, HEIGHT)  # Change to self.load_image
        self.selected_student = None
        self.students = load_students()
        self.setup_ui()

    def load_image(self, path, width, height):
        """Load and resize image"""
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            img = img.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def setup_ui(self):
        """Setup UI"""
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        if self.bg:
            self.canvas.create_image(0, 0, image=self.bg, anchor="nw")
        
        self.setup_title()
        self.setup_stats()
        self.setup_buttons()
        self.setup_student_list()
        self.setup_details()

    def setup_title(self):
        """Create title"""
        title = tk.Label(self.canvas, text="Student Manager", bg=COLORS['title'],
                        fg='black', font=(FONT, FONT_SIZES['title'], 'bold'))
        self.canvas.create_window(WIDTH / 2, POS['title_y'], window=title)

    def setup_stats(self):
        """Create stats with real data"""
        total = len(self.students)
        
        if total > 0:
            avg_percentage = sum(s.percentage for s in self.students) / total
            highest_percentage = max(s.percentage for s in self.students)
            passing = sum(1 for s in self.students if s.percentage >= 40)
            a_plus = sum(1 for s in self.students if s.grade == 'A')
            f_count = sum(1 for s in self.students if s.grade == 'F')
            
            passing_percentage = (passing / total) * 100
        else:
            avg_percentage = highest_percentage = passing_percentage = 0
            a_plus = f_count = 0
        
        stats = [
            ("Students", str(total)),
            ("Average", f"{avg_percentage:.1f}%"),
            ("Highest", f"{highest_percentage:.1f}%"),
            ("Passing", f"{passing_percentage:.1f}%"),
            ("A+", str(a_plus)),
            ("F", str(f_count))
        ]
        
        for i, (label, value) in enumerate(stats):
            x = 120 + (i * 200)
            frame = tk.Frame(self.canvas, bg=COLORS['content'])
            self.canvas.create_window(x, POS['stats_y'], window=frame)
            
            tk.Label(frame, text=label, bg=COLORS['content'],
                    fg='black', font=(FONT, FONT_SIZES['stats_label'], 'bold')).pack()
            tk.Label(frame, text=value, bg=COLORS['content'],
                    fg='black', font=(FONT, FONT_SIZES['stats_value'])).pack()

    def create_btn(self, text, cmd, x, y):
        """Create button with hover effects"""
        btn = tk.Label(self.canvas, text=text, bg=COLORS['button'],
                    fg='black', font=(FONT, FONT_SIZES['button'], 'bold'), cursor='hand2')
        
        btn.bind('<Enter>', lambda e: btn.config(bg=COLORS['hover']))
        btn.bind('<Leave>', lambda e: btn.config(bg=COLORS['button']))
        btn.bind('<Button-1>', lambda e: cmd())
        
        self.canvas.create_window(x, y, window=btn)
        return btn

    def setup_buttons(self):
        """Create buttons with custom spacing for text length"""
        buttons = [
            ("View Student", self.view),
            ("Add Student", self.add),
            ("Edit Student", self.edit),
            ("Delete Student", self.delete),
            ("Show Highest", self.highest),
            ("Show Lowest", self.lowest),
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            x = POSITIONS[i]
            self.create_btn(text, cmd, x, POS['buttons_y'])

    def setup_student_list(self):
        """Setup student list in spreadsheet style"""
        # Create main frame for the entire student list section
        main_frame = tk.Frame(self.canvas, bg=COLORS['content'])
        self.canvas.create_window(POS['list_x'], POS['list_y'], window=main_frame, 
                                width=POS['list_w'], height=POS['list_h'])
        
        # Add sorting controls at the top
        sort_frame = tk.Frame(main_frame, bg=COLORS['content'])
        sort_frame.pack(fill='x', pady=(0, 5))
        
        # Sort label
        tk.Label(sort_frame, text="Sort by:", bg=COLORS['content'],
                fg='black', font=(FONT, FONT_SIZES['header'], 'bold')).pack(side='left', padx=(10, 5))
        
        # Sorting variable
        self.sort_var = tk.StringVar(value="id")  # Default sort by ID
        
        # ID radio button
        id_radio = tk.Radiobutton(sort_frame, text="ID", variable=self.sort_var,
                                value="id", bg=COLORS['content'], fg='black',
                                font=(FONT, FONT_SIZES['cell']), command=self.apply_sorting)
        id_radio.pack(side='left', padx=(0, 15))
        
        # Name radio button  
        name_radio = tk.Radiobutton(sort_frame, text="Name", variable=self.sort_var,
                                value="name", bg=COLORS['content'], fg='black',
                                font=(FONT, FONT_SIZES['cell']), command=self.apply_sorting)
        name_radio.pack(side='left', padx=(0, 15))
        
        # Percentage radio button
        perc_radio = tk.Radiobutton(sort_frame, text="Percentage", variable=self.sort_var,
                                value="percentage", bg=COLORS['content'], fg='black',
                                font=(FONT, FONT_SIZES['cell']), command=self.apply_sorting)
        perc_radio.pack(side='left')
        
        # Create frame for student list (with scrollbars)
        list_frame = tk.Frame(main_frame, bg=COLORS['content'])
        list_frame.pack(fill='both', expand=True)
        
        # Create canvas with scrollbars for the list
        list_canvas = tk.Canvas(list_frame, bg=COLORS['content'], highlightthickness=0)
        
        # Vertical scrollbar
        v_scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=list_canvas.yview)
        
        # Horizontal scrollbar
        h_scrollbar = tk.Scrollbar(list_frame, orient="horizontal", command=list_canvas.xview)
        
        self.scrollable_frame = tk.Frame(list_canvas, bg=COLORS['content'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(
                scrollregion=list_canvas.bbox("all")
            )
        )
        
        list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        list_canvas.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Pack the canvas and scrollbars
        list_canvas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights for proper resizing
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Create headers
        for col, header in enumerate(TABLE['headers']):
            label = tk.Label(self.scrollable_frame, text=header, bg=COLORS['button'],
                            fg='black', font=(FONT, FONT_SIZES['header'], 'bold'), 
                            width=TABLE['col_w'], relief='ridge')
            label.grid(row=0, column=col, sticky='ew', padx=1, pady=1)
        
        self.student_rows = {}  # Store row widgets by student
        self.refresh_student_list()

    def refresh_student_list(self):
        """Refresh the student list with current data"""
        # Clear existing student rows
        for row_widgets in self.student_rows.values():
            for widget in row_widgets:
                widget.destroy()
        self.student_rows.clear()
        
        # Add student rows
        for row, student in enumerate(self.students, start=1):
            student_data = [
                student.student_id, student.name, student.mark1, student.mark2,
                student.mark3, student.coursework_total, student.exam_mark,
                student.total_score, student.grade
            ]
            
            # Store labels for this row to highlight together
            row_labels = []
            
            for col, data in enumerate(student_data):
                label = tk.Label(self.scrollable_frame, text=str(data), 
                            bg=COLORS['content'], fg='black', font=(FONT, FONT_SIZES['cell']),
                            width=TABLE['col_w'], relief='solid', cursor='hand2')
                label.grid(row=row, column=col, sticky='ew', padx=1, pady=1)
                
                # Bind click event to select student
                label.bind('<Button-1>', lambda e, s=student: self.select_student(s))
                label.bind('<Enter>', lambda e, lbl=label: self.hover_label(lbl, True))
                label.bind('<Leave>', lambda e, lbl=label: self.hover_label(lbl, False))
                
                row_labels.append(label)
            
            self.student_rows[student] = row_labels
        
        # Re-highlight selected student if any
        if self.selected_student and self.selected_student in self.student_rows:
            self.highlight_student_row(self.selected_student)

    def hover_label(self, label, is_hovering):
        """Handle label hover effects"""
        if is_hovering and label not in self.student_rows.get(self.selected_student, []):
            label.config(bg=COLORS['hover'])
        elif not is_hovering and label not in self.student_rows.get(self.selected_student, []):
            label.config(bg=COLORS['content'])

    def highlight_student_row(self, student):
        """Highlight a student's row"""
        # Clear previous highlights
        for row_widgets in self.student_rows.values():
            for widget in row_widgets:
                widget.config(bg=COLORS['content'])
        
        # Highlight selected student
        if student in self.student_rows:
            for label in self.student_rows[student]:
                label.config(bg=TABLE['select_color'])

    def select_student(self, student):
        """Select a student from the list"""
        self.selected_student = student
        self.highlight_student_row(student)

    def apply_sorting(self):
        """Apply sorting based on selected radio button"""
        sort_by = self.sort_var.get()
        
        if sort_by == "id":
            self.students.sort(key=lambda s: s.student_id)
        elif sort_by == "name":
            self.students.sort(key=lambda s: s.name.lower())
        elif sort_by == "percentage":
            self.students.sort(key=lambda s: s.percentage)
        
        self.refresh_student_list()
        
        # Clear selection since order changed
        self.selected_student = None
        self.highlight_student_row(None)

    def setup_details(self):
        """Setup details panel"""
        self.detail_frame = tk.Frame(self.canvas, bg=COLORS['content'])
        self.canvas.create_window(POS['details_x'], POS['details_y'], window=self.detail_frame, 
                                width=POS['details_w'], height=POS['details_h'])
        
        self.title = tk.Label(self.detail_frame, text="Student Details", 
                            bg=COLORS['content'], fg='black', 
                            font=(FONT, FONT_SIZES['title'], 'bold'))
        self.title.pack(pady=10)
        
        self.content = tk.Frame(self.detail_frame, bg=COLORS['content'])
        self.content.pack(fill='both', expand=True, padx=20)
        
        self.show_empty()

    def show_details(self, student):
        """Show student details"""
        for w in self.content.winfo_children():
            w.destroy()
        self.title.config(text="Student Details")
        
        info = [
            ("ID:", student.student_id), ("Name:", student.name),
            ("CW1:", f"{student.mark1}/20"), ("CW2:", f"{student.mark2}/20"),
            ("CW3:", f"{student.mark3}/20"), ("CW Total:", f"{student.coursework_total}/60"),
            ("Exam:", f"{student.exam_mark}/100"), ("Total:", f"{student.total_score}/160"),
            ("Percentage:", f"{student.percentage:.1f}%"), ("Grade:", student.grade)
        ]
        
        for label, value in info:
            row = tk.Frame(self.content, bg=COLORS['content'])
            row.pack(fill='x', pady=2)
            
            tk.Label(row, text=label, bg=COLORS['content'], fg='black',
                    font=(FONT, FONT_SIZES['detail_label'], 'bold'), width=12, anchor='w').pack(side='left')
            tk.Label(row, text=value, bg=COLORS['content'], fg='black',
                    font=(FONT, FONT_SIZES['detail_value']), anchor='w').pack(side='left')

    def add(self):
        """Show add form"""
        self.title.config(text="Add Student")
        
        for w in self.content.winfo_children():
            w.destroy()
        
        # Scrollable frame
        scroll_frame = tk.Frame(self.content, bg=COLORS['content'])
        scroll_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(scroll_frame, bg=COLORS['content'], highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        form_frame = tk.Frame(canvas, bg=COLORS['content'])
        
        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        self.fields = {}
        
        # Student ID
        tk.Label(form_frame, text="Student ID:", bg=COLORS['content'],
                fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
        id_entry = tk.Entry(form_frame, font=(FONT, FONT_SIZES['form']), width=30)
        id_entry.pack(fill='x', pady=(0, 10))
        self.fields['id'] = id_entry
        
        # Name
        tk.Label(form_frame, text="Name:", bg=COLORS['content'],
                fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
        name_entry = tk.Entry(form_frame, font=(FONT, FONT_SIZES['form']), width=30)
        name_entry.pack(fill='x', pady=(0, 10))
        self.fields['name'] = name_entry
        
        # Coursework marks
        for i in range(1, 4):
            tk.Label(form_frame, text=f"CW{i} (0-20):", bg=COLORS['content'],
                    fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
            mark_entry = tk.Entry(form_frame, font=(FONT, FONT_SIZES['form']), width=30)
            mark_entry.pack(fill='x', pady=(0, 10))
            self.fields[f'mark{i}'] = mark_entry
        
        # Exam mark
        tk.Label(form_frame, text="Exam (0-100):", bg=COLORS['content'],
                fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
        exam_entry = tk.Entry(form_frame, font=(FONT, FONT_SIZES['form']), width=30)
        exam_entry.pack(fill='x', pady=(0, 20))
        self.fields['exam'] = exam_entry
        
        # Buttons
        btn_frame = tk.Frame(self.content, bg=COLORS['content'])
        btn_frame.pack(fill='x', pady=10)
        
        save_btn = tk.Label(btn_frame, text="Save", bg=COLORS['success'],
                        fg='white', font=(FONT, FONT_SIZES['form'], 'bold'), cursor='hand2')
        save_btn.pack(side='left', padx=(0, 10))
        save_btn.bind('<Button-1>', lambda e: self.save_new())
        save_btn.bind('<Enter>', lambda e: save_btn.config(bg='#219955'))
        save_btn.bind('<Leave>', lambda e: save_btn.config(bg=COLORS['success']))
        
        cancel_btn = tk.Label(btn_frame, text="Cancel", bg=COLORS['danger'],
                        fg='white', font=(FONT, FONT_SIZES['form'], 'bold'), cursor='hand2')
        cancel_btn.pack(side='left')
        cancel_btn.bind('<Button-1>', lambda e: self.show_empty())
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.config(bg='#A93226'))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.config(bg=COLORS['danger']))
        
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def save_new(self):
        """Save new student"""
        try:
            student_id = int(self.fields['id'].get().strip())
            name = self.fields['name'].get().strip()
            marks = [int(self.fields[f'mark{i}'].get()) for i in range(1, 4)]
            exam = int(self.fields['exam'].get())
            
            # Validation
            if not name:
                self.show_msg("Error: Please enter a name", "error")
                return
            
            if student_id < 1000 or student_id > 9999:
                self.show_msg("Error: Student ID must be between 1000-9999", "error")
                return
            
            if any(m < 0 or m > 20 for m in marks):
                self.show_msg("Error: Coursework marks must be 0-20", "error")
                return
            
            if exam < 0 or exam > 100:
                self.show_msg("Error: Exam mark must be 0-100", "error")
                return
            
            if any(s.student_id == student_id for s in self.students):
                self.show_msg("Error: Student ID already exists", "error")
                return
            
            # Create and save
            new_student = Student(student_id, name, *marks, exam)
            self.students.append(new_student)
            save_students(self.students)
            
            # Update UI
            self.refresh_stats()
            self.selected_student = new_student
            self.show_details(new_student)
            self.title.config(text=f"✓ Added: {name}")
            
        except ValueError:
            self.show_msg("Error: Please enter valid numbers", "error")

    def show_popup(self):
        """Show no selection popup"""
        popup = tk.Toplevel(self.root)
        popup.title("No Selection")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        popup.transient(self.root)
        popup.grab_set()
        
        content = tk.Frame(popup, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(content, text="⚠️", bg='white', fg='orange', 
                font=(FONT, 24)).pack(pady=(10, 5))
        
        tk.Label(content, text="No Student Selected", bg='white', 
                fg='black', font=(FONT, 14, 'bold')).pack(pady=5)
        
        tk.Label(content, text="Please select a student first", bg='white',
                fg='black', font=(FONT, 10)).pack(pady=5)
        
        ok_btn = tk.Label(content, text="OK", bg=COLORS['button'],
                        fg='black', font=(FONT, 12, 'bold'), cursor='hand2')
        ok_btn.pack(pady=10)
        ok_btn.bind('<Button-1>', lambda e: popup.destroy())
        ok_btn.bind('<Enter>', lambda e: ok_btn.config(bg=COLORS['hover']))
        ok_btn.bind('<Leave>', lambda e: ok_btn.config(bg=COLORS['button']))
        
        popup.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")

    def view(self):
        """View selected student"""
        if self.selected_student is None:
            self.show_popup()
        else:
            self.show_details(self.selected_student)

    def edit(self):
        """Edit selected student"""
        if self.selected_student is None:
            self.show_popup()
        else:
            self.show_edit_form(self.selected_student)

    def show_edit_form(self, student):
        """Show edit form"""
        self.title.config(text=f"Edit: {student.name}")
        
        for w in self.content.winfo_children():
            w.destroy()
        
        # Scrollable frame
        scroll_frame = tk.Frame(self.content, bg=COLORS['content'])
        scroll_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(scroll_frame, bg=COLORS['content'], highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        form_frame = tk.Frame(canvas, bg=COLORS['content'])
        
        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        self.edit_fields = {}
        
        # Student ID (read-only)
        tk.Label(form_frame, text="Student ID:", bg=COLORS['content'],
                fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
        id_label = tk.Label(form_frame, text=str(student.student_id), 
                        bg=COLORS['content'], fg='black', font=(FONT, FONT_SIZES['form']))
        id_label.pack(anchor='w', pady=(0, 10))
        
        # Name
        tk.Label(form_frame, text="Name:", bg=COLORS['content'],
                fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
        name_entry = tk.Entry(form_frame, font=(FONT, FONT_SIZES['form']), width=30)
        name_entry.insert(0, student.name)
        name_entry.pack(fill='x', pady=(0, 10))
        self.edit_fields['name'] = name_entry
        
        # Coursework marks
        marks = [student.mark1, student.mark2, student.mark3]
        for i in range(1, 4):
            tk.Label(form_frame, text=f"CW{i} (0-20):", bg=COLORS['content'],
                    fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
            mark_entry = tk.Entry(form_frame, font=(FONT, FONT_SIZES['form']), width=30)
            mark_entry.insert(0, str(marks[i-1]))
            mark_entry.pack(fill='x', pady=(0, 10))
            self.edit_fields[f'mark{i}'] = mark_entry
        
        # Exam mark
        tk.Label(form_frame, text="Exam (0-100):", bg=COLORS['content'],
                fg='black', font=(FONT, FONT_SIZES['form'], 'bold')).pack(anchor='w', pady=(5, 0))
        exam_entry = tk.Entry(form_frame, font=(FONT, FONT_SIZES['form']), width=30)
        exam_entry.insert(0, str(student.exam_mark))
        exam_entry.pack(fill='x', pady=(0, 20))
        self.edit_fields['exam'] = exam_entry
        
        # Buttons
        btn_frame = tk.Frame(self.content, bg=COLORS['content'])
        btn_frame.pack(fill='x', pady=10)
        
        save_btn = tk.Label(btn_frame, text="Save", bg=COLORS['success'],
                        fg='white', font=(FONT, FONT_SIZES['form'], 'bold'), cursor='hand2')
        save_btn.pack(side='left', padx=(0, 10))
        save_btn.bind('<Button-1>', lambda e: self.save_edit(student))
        save_btn.bind('<Enter>', lambda e: save_btn.config(bg='#219955'))
        save_btn.bind('<Leave>', lambda e: save_btn.config(bg=COLORS['success']))
        
        cancel_btn = tk.Label(btn_frame, text="Cancel", bg=COLORS['danger'],
                            fg='white', font=(FONT, FONT_SIZES['form'], 'bold'), cursor='hand2')
        cancel_btn.pack(side='left')
        cancel_btn.bind('<Button-1>', lambda e: self.show_details(student))
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.config(bg='#A93226'))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.config(bg=COLORS['danger']))
        
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def save_edit(self, student):
        """Save edited student"""
        try:
            name = self.edit_fields['name'].get().strip()
            marks = [int(self.edit_fields[f'mark{i}'].get()) for i in range(1, 4)]
            exam = int(self.edit_fields['exam'].get())
            
            # Validation
            if not name:
                self.show_msg("Error: Please enter a name", "error")
                return
            
            if any(m < 0 or m > 20 for m in marks):
                self.show_msg("Error: Coursework marks must be 0-20", "error")
                return
            
            if exam < 0 or exam > 100:
                self.show_msg("Error: Exam mark must be 0-100", "error")
                return
            
            # Update student
            student.name = name
            student.mark1, student.mark2, student.mark3 = marks
            student.exam_mark = exam
            
            # Save to file
            save_students(self.students)
            
            # Update UI
            self.refresh_stats()
            self.show_details(student)
            self.title.config(text=f"✓ Updated: {name}")
            
        except ValueError:
            self.show_msg("Error: Please enter valid numbers", "error")

    def delete(self):
        """Delete selected student"""
        if self.selected_student is None:
            self.show_popup()
        else:
            self.show_delete_confirm(self.selected_student)

    def show_delete_confirm(self, student):
        """Show delete confirmation"""
        self.title.config(text="Confirm Delete")
        
        for w in self.content.winfo_children():
            w.destroy()
        
        # Warning message
        warn_frame = tk.Frame(self.content, bg=COLORS['content'])
        warn_frame.pack(fill='x', pady=20)
        
        tk.Label(warn_frame, text="⚠️", bg=COLORS['content'], fg='orange',
                font=(FONT, 36)).pack(pady=(0, 10))
        
        tk.Label(warn_frame, text=f"Delete {student.name}?", 
                bg=COLORS['content'], fg='black', font=(FONT, 16, 'bold')).pack()
        
        tk.Label(warn_frame, text=f"ID: {student.student_id}", 
                bg=COLORS['content'], fg='black', font=(FONT, 12)).pack(pady=5)
        
        tk.Label(warn_frame, text="This action cannot be undone!", 
                bg=COLORS['content'], fg='red', font=(FONT, 10, 'bold')).pack()
        
        # Buttons
        btn_frame = tk.Frame(self.content, bg=COLORS['content'])
        btn_frame.pack(fill='x', pady=20)
        
        del_btn = tk.Label(btn_frame, text="DELETE", bg=COLORS['danger'],
                        fg='white', font=(FONT, 14, 'bold'), cursor='hand2')
        del_btn.pack(side='left', padx=(0, 10))
        del_btn.bind('<Button-1>', lambda e: self.confirm_delete(student))
        del_btn.bind('<Enter>', lambda e: del_btn.config(bg='#A93226'))
        del_btn.bind('<Leave>', lambda e: del_btn.config(bg=COLORS['danger']))
        
        cancel_btn = tk.Label(btn_frame, text="Cancel", bg=COLORS['button'],
                            fg='black', font=(FONT, 14, 'bold'), cursor='hand2')
        cancel_btn.pack(side='left')
        cancel_btn.bind('<Button-1>', lambda e: self.show_details(student))
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.config(bg=COLORS['hover']))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.config(bg=COLORS['button']))

    def confirm_delete(self, student):
        """Actually delete student"""
        self.students.remove(student)
        save_students(self.students)
        
        if self.selected_student == student:
            self.selected_student = None
        
        self.refresh_stats()
        self.show_empty()
        self.title.config(text=f"✓ Deleted: {student.name}")

    def highest(self):
        """Show highest scoring student"""
        if not self.students:
            self.show_msg("No students in database", "error")
            return
        
        # Find student with highest percentage
        highest_student = max(self.students, key=lambda s: s.percentage)
        self.selected_student = highest_student
        self.show_details(highest_student)
        self.title.config(text=f"{highest_student.name}")

    def lowest(self):
        """Show lowest scoring student"""
        if not self.students:
            self.show_msg("No students in database", "error")
            return
        
        # Find student with lowest percentage
        lowest_student = min(self.students, key=lambda s: s.percentage)
        self.selected_student = lowest_student
        self.show_details(lowest_student)
        self.title.config(text=f"{lowest_student.name}")

    def show_msg(self, msg, type="info"):
        """Show temporary message"""
        original = self.title.cget("text")
        
        if type == "error":
            self.title.config(text=f"❌ {msg}", fg="red")
        else:
            self.title.config(text=f"✓ {msg}", fg="green")
        
        self.root.after(3000, lambda: self.title.config(text=original, fg="black"))

    def show_empty(self):
        """Show empty details panel"""
        for w in self.content.winfo_children():
            w.destroy()
        self.title.config(text="")

    def refresh_stats(self):
        """Refresh statistics and student list"""
        # Remember current sort
        current_sort = self.sort_var.get()
        
        self.refresh_student_list()
        
        # Re-apply current sort
        self.apply_sorting()
        
        # Update the stats display
        for widget in self.canvas.winfo_children():
            if hasattr(widget, 'winfo_children'):
                children = widget.winfo_children()
                if children and any('frame' in str(child) for child in children):
                    widget_info = str(widget)
                    if 'frame' in widget_info.lower() and 'canvas' not in widget_info.lower():
                        widget.destroy()
        
        self.setup_stats()