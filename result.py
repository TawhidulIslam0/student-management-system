from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from database import init_database

class AddResult:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management System")  
        self.root.geometry("1350x700+0+0")  
        self.root.config(bg="#FFFFFF")
        self.root.focus_force()

        # Initialize database (creates all tables: course, student, result)
        init_database()

        # ===== VARIABLES =====
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()

        # ===== TITLE BAR =====
        title = Label(self.root, text="Add Student Result", font=("times new roman", 25, "bold"), bg="#06187D", fg="#FFFFFF")
        title.place(x=0, y=0, relwidth=1, height=60)

        # ===== LEFT FRAME (Input Fields) =====
        input_frame = Frame(self.root, bg="#FFFFFF", bd=2, relief=RIDGE)
        input_frame.place(x=50, y=80, width=700, height=450)

        # 1. Select Student (Dropdown + Search)
        lbl_select_student = Label(input_frame, text="Select Student", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_select_student.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Dropdown (loads student Roll Nos from DB)
        self.cmb_roll = ttk.Combobox(input_frame, textvariable=self.var_roll, font=("times new roman", 15), state='readonly', width=20)
        self.cmb_roll.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        # Search Button
        btn_search = Button(input_frame, text="Search", command=self.load_student_details, font=("times new roman", 13, "bold"), bg="#007bff", fg="white", bd=0, cursor="hand2", width=10)
        btn_search.grid(row=0, column=2, padx=10, pady=20)

        # 2. Name
        lbl_name = Label(input_frame, text="Name", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_name.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        
        self.txt_name = Entry(input_frame, textvariable=self.var_name, font=("times new roman", 15), bg="#F0F0F0", state='disabled', width=35)
        self.txt_name.grid(row=1, column=1, columnspan=2, padx=10, pady=20, sticky="w")

        # 3. Course 
        lbl_course = Label(input_frame, text="Course",font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_course.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        
        self.txt_course = Entry(input_frame, textvariable=self.var_course, font=("times new roman", 15), bg="#F0F0F0", state='disabled', width=35)
        self.txt_course.grid(row=2, column=1, columnspan=2, padx=10, pady=20, sticky="w")

        # 4. Marks Obtained
        lbl_marks = Label(input_frame, text="Marks Obtained", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_marks.grid(row=3, column=0, padx=20, pady=20, sticky="w")
        
        self.txt_marks = Entry(input_frame, textvariable=self.var_marks, font=("times new roman", 15), bg="#FFFFFF", width=35)
        self.txt_marks.grid(row=3, column=1, columnspan=2, padx=10, pady=20, sticky="w")

        # 5. Full Marks
        lbl_full_marks = Label(input_frame, text="Full Marks", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_full_marks.grid(row=4, column=0, padx=20, pady=20, sticky="w")
        
        self.txt_full_marks = Entry(input_frame, textvariable=self.var_full_marks, font=("times new roman", 15), bg="#FFFFFF", width=35)
        self.txt_full_marks.grid(row=4, column=1, columnspan=2, padx=10, pady=20, sticky="w")

        # ===== Buttons =====
        btn_submit = Button(input_frame, text="Submit", command=self.add_result, font=("times new roman", 15, "bold"), bg="#28a745", fg="white", bd=0, cursor="hand2", width=9)
        btn_submit.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        btn_clear = Button(input_frame, text="Clear", command=self.clear_fields, font=("times new roman", 15, "bold"), bg="#6c757d", fg="white", bd=0, cursor="hand2", width=9)
        btn_clear.grid(row=5, column=2, padx=5, pady=5, sticky="w")

        # ===== RIGHT FRAME (Image) =====
        img_frame = Frame(self.root, bg="#FFFFFF", bd=2, relief=RIDGE)
        img_frame.place(x=700, y=80, width=500, height=450)
        
        try:
            # Replace with your image path (or remove this block if no image)
            self.bg_img = Image.open("Images/result.png")
            self.bg_img = self.bg_img.resize((490, 440), Image.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            self.lbl_bg = Label(img_frame, image=self.bg_img)
            self.lbl_bg.pack(fill=BOTH, expand=1)
        except Exception as e:
            # Fallback text if image is missing
            self.lbl_bg = Label(img_frame, text=f"Results\n(Image Error: {str(e)[:30]})", 
                               font=("times new roman", 30, "bold"), bg="#FFFFFF", fg="#FF0000")
            self.lbl_bg.pack(fill=BOTH, expand=1)

        # ===== Load student rolls on startup =====
        self.load_student_rolls()

    # ===== DATABASE METHODS =====
    def load_student_rolls(self):
        """Load student Roll Nos from DB into dropdown"""
        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            cur.execute("SELECT roll_no FROM student")
            rolls = [row[0] for row in cur.fetchall()]
            self.cmb_roll['values'] = rolls
            conn.close()
            
            # Warning if no students exist
            if not rolls:
                messagebox.showwarning("No Students", 
                                      "No students found in database!\nPlease add students first (via student.py)", 
                                      parent=self.root)
        except Exception as ex:
            messagebox.showerror("Database Error", f"Failed to load students: {str(ex)}", parent=self.root)

    def load_student_details(self):
        """Load selected student's Name/Course from DB (on Search click)"""
        roll_no = self.var_roll.get().strip()
        if not roll_no:
            messagebox.showerror("Error", "Select a Student first!", parent=self.root)
            return

        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            cur.execute("SELECT name, course FROM student WHERE roll_no=?", (roll_no,))
            student = cur.fetchone()
            
            if student:
                # Temporarily enable fields to update values
                self.txt_name.config(state='normal')
                self.txt_course.config(state='normal')
                
                self.var_name.set(student[0])
                self.var_course.set(student[1])
                
                # Disable again to prevent manual editing
                self.txt_name.config(state='disabled')
                self.txt_course.config(state='disabled')
            else:
                messagebox.showerror("Error", "Student not found in database!", parent=self.root)
                self.clear_fields()
            conn.close()
        except Exception as ex:
            messagebox.showerror("Database Error", f"Failed to load details: {str(ex)}", parent=self.root)

    def add_result(self):
        """Add student result to database (with full validation)"""
        # Step 1: Basic validation
        roll_no = self.var_roll.get().strip()
        name = self.var_name.get().strip()
        marks = self.var_marks.get().strip()
        full_marks = self.var_full_marks.get().strip()

        if not roll_no or not name:
            messagebox.showerror("Error", "Please select and search for a student first!", parent=self.root)
            return
            
        if not marks or not full_marks:
            messagebox.showerror("Error", "Marks Obtained and Full Marks are required!", parent=self.root)
            return
        
        # Step 2: Validate marks are numbers
        try:
            marks_int = int(marks)
            full_marks_int = int(full_marks)
        except ValueError:
            messagebox.showerror("Error", "Marks must be valid numbers (0-9)!", parent=self.root)
            return

        # Step 3: Validate marks range
        if marks_int < 0 or full_marks_int <= 0:
            messagebox.showerror("Error", "Marks must be positive numbers!\nFull Marks cannot be zero!", parent=self.root)
            return
        
        if marks_int > full_marks_int:
            messagebox.showerror("Error", "Marks Obtained cannot exceed Full Marks!", parent=self.root)
            return

        # Step 4: Insert into database
        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            
            # Insert result data
            cur.execute("""
                INSERT INTO result (roll_no, name, course, marks_obtained, full_marks)
                VALUES (?, ?, ?, ?, ?)
            """, (
                roll_no,
                name,
                self.var_course.get().strip(),
                marks_int,
                full_marks_int
            ))
            
            conn.commit()
            messagebox.showinfo("Success", "Result added to database successfully!", parent=self.root)
            self.clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Duplicate result entry!\nA result for this student already exists.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Database Error", f"Failed to add result: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        """Clear all input fields (fix for disabled Name/Course)"""
        self.var_roll.set("")
        
        # Temporarily enable to clear values
        self.txt_name.config(state='normal')
        self.txt_course.config(state='normal')
        
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
        
        # Disable again
        self.txt_name.config(state='disabled')
        self.txt_course.config(state='disabled')

if __name__ == "__main__": 
    root = Tk()
    obj = AddResult(root)
    root.mainloop()