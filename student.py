from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from database import init_database

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")  
        self.root.geometry("1350x700+0+0")  
        self.root.config(bg="#FFFFFF")
        self.root.focus_force()

        # Initialize database (creates course + student tables if missing)
        init_database()

        # Title bar
        title = Label(self.root, text="Manage Student Details", font=("times new roman", 30, "bold"), bg="#06187D", fg="#FFFFFF")
        title.place(x=0, y=0, relwidth=1, height=50)

        # ===== STUDENT VARIABLES =====
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_admission_date = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_search_roll = StringVar()  # For search (Roll No.)

        # ===== LEFT FRAME (Student Input Fields) =====
        # Row 1: Roll No. + D.O.B
        lbl_roll = Label(self.root, text="Roll No.", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_roll.place(x=50, y=100)
        txt_roll = Entry(self.root, textvariable=self.var_roll, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_roll.place(x=180, y=100, width=200)

        lbl_dob = Label(self.root, text="D.O.B(dd-mm-yyyy)", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_dob.place(x=400, y=100)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_dob.place(x=580, y=100, width=200)

        # Row 2: Name + Contact No.
        lbl_name = Label(self.root, text="Name", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_name.place(x=50, y=140)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_name.place(x=180, y=140, width=200)

        lbl_contact = Label(self.root, text="Contact No.", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_contact.place(x=400, y=140)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_contact.place(x=580, y=140, width=200)

        # Row 3: Email + Select Course
        lbl_email = Label(self.root, text="Email", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_email.place(x=50, y=180)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_email.place(x=180, y=180, width=200)

        lbl_course = Label(self.root, text="Select Course", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_course.place(x=400, y=180)
        # Dropdown for courses (load from database)
        self.cmb_course = ttk.Combobox(self.root, textvariable=self.var_course, font=("times new roman", 15), state='readonly')
        self.cmb_course.place(x=580, y=180, width=200)
        self.load_courses()  # Load courses from DB into dropdown

        # Row 4: Gender + Admission Date
        lbl_gender = Label(self.root, text="Gender", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_gender.place(x=50, y=220)
        self.cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Male", "Female", "Other"), font=("times new roman", 15), state='readonly')
        self.cmb_gender.place(x=180, y=220, width=200)
        self.cmb_gender.current(0)

        lbl_admission = Label(self.root, text="Admission Date", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_admission.place(x=400, y=220)
        txt_admission = Entry(self.root, textvariable=self.var_admission_date, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_admission.place(x=580, y=220, width=200)

        # Row 5: State + City
        lbl_state = Label(self.root, text="State", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_state.place(x=50, y=260)
        txt_state = Entry(self.root, textvariable=self.var_state, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_state.place(x=180, y=260, width=200)

        lbl_city = Label(self.root, text="City", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_city.place(x=400, y=260)
        txt_city = Entry(self.root, textvariable=self.var_city, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_city.place(x=580, y=260, width=200)

        lbl_address = Label(self.root, text="Address",font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_address.place(x=50, y=300) 
        self.txt_address = Text(self.root, font=("times new roman", 15), bg="#FFFFFF", fg="#000000", wrap=WORD)
        self.txt_address.place(x=180, y=300, width=600, height=160)

        # ===== BUTTONS (Save, Update, Delete, Clear) =====
        btn_save = Button(self.root, text="Save", command=self.add_student, font=("times new roman", 15, "bold"), bg="#007bff", fg="white", bd=0, cursor="hand2")
        btn_save.place(x=180, y=480, width=120, height=40)

        btn_update = Button(self.root, text="Update", command=self.update_student, font=("times new roman", 15, "bold"), bg="#28a745", fg="white", bd=0, cursor="hand2")
        btn_update.place(x=320, y=480, width=120, height=40)

        btn_delete = Button(self.root, text="Delete", command=self.delete_student, font=("times new roman", 15, "bold"), bg="#dc3545", fg="white", bd=0, cursor="hand2")
        btn_delete.place(x=460, y=480, width=120, height=40)

        btn_clear = Button(self.root, text="Clear", command=self.clear_fields, font=("times new roman", 15, "bold"), bg="#6c757d", fg="white", bd=0, cursor="hand2")
        btn_clear.place(x=600, y=480, width=120, height=40)

        # ===== RIGHT SIDE (Search + Treeview) =====
        # Search Panel (Search by Roll No.)
        lbl_search = Label(self.root, text="Search Roll No.", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_search.place(x=800, y=100)
        txt_search = Entry(self.root, textvariable=self.var_search_roll, font=("times new roman", 15), bg="#FFFFFF", fg="#000000")
        txt_search.place(x=930, y=100, width=180)

        btn_search = Button(self.root, text="Search", command=self.search_student, font=("times new roman", 15, "bold"), bg="#06187D", fg="white", bd=0, cursor="hand2")
        btn_search.place(x=1120, y=100, width=100, height=28)

        # Treeview (Display Student Data)
        self.student_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.student_frame.place(x=800, y=140, width=420, height=400)

        # Scrollbars
        scrolly = Scrollbar(self.student_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.student_frame, orient=HORIZONTAL)

        # Treeview Columns (match image: Roll No., Name, Email, Gender, D.O.B)
        self.student_table = ttk.Treeview(self.student_frame, columns=("roll_no", "name", "email", "gender", "dob"),
                                          xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.config(command=self.student_table.xview)
        scrolly.config(command=self.student_table.yview)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        # Treeview Headings
        self.student_table.heading("roll_no", text="Roll No.")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="D.O.B")
        self.student_table["show"] = "headings"

        # Column Widths
        self.student_table.column("roll_no", width=80)
        self.student_table.column("name", width=100)
        self.student_table.column("email", width=120)
        self.student_table.column("gender", width=80)
        self.student_table.column("dob", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        # Bind click to select row (populate fields with DB data)
        self.student_table.bind("<ButtonRelease-1>", self.get_selected_student)

        # Load existing students from DB on startup
        self.fetch_all_students()

    # ===== DATABASE METHODS =====
    def load_courses(self):
        """Load courses from database into dropdown (critical for student-course mapping)"""
        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            cur.execute("SELECT name FROM course")  # Get all course names from DB
            courses = [row[0] for row in cur.fetchall()]
            self.cmb_course['values'] = courses  # Populate dropdown
            conn.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to load courses: {str(ex)}", parent=self.root)

    def add_student(self):
        """Add new student to database (with validation)"""
        # Mandatory field check
        if not self.var_roll.get().strip() or not self.var_name.get().strip():
            messagebox.showerror("Error", "Roll No. and Name are required!", parent=self.root)
            return

        conn = None
        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            
            # Check if Roll No. already exists
            cur.execute("SELECT * FROM student WHERE roll_no=?", (self.var_roll.get().strip(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Roll No. already exists!", parent=self.root)
                return

            # Insert student data into DB
            cur.execute("""
                INSERT INTO student (roll_no, name, dob, email, gender, contact_no, course, admission_date, state, city, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.var_roll.get().strip(),
                self.var_name.get().strip(),
                self.var_dob.get().strip(),
                self.var_email.get().strip(),
                self.var_gender.get(),
                self.var_contact.get().strip(),
                self.var_course.get(),
                self.var_admission_date.get().strip(),
                self.var_state.get().strip(),
                self.var_city.get().strip(),
                self.txt_address.get('1.0', END).strip()
            ))
            
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!", parent=self.root)
            
            # Refresh Treeview and clear fields
            self.fetch_all_students()
            self.clear_fields()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to add student: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()  # Ensure DB connection is closed

    def fetch_all_students(self):
        """Load all students from database into Treeview"""
        conn = None
        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            # Fetch only relevant columns for Treeview
            cur.execute("SELECT roll_no, name, email, gender, dob FROM student")
            rows = cur.fetchall()
            
            # Clear existing data in Treeview
            self.student_table.delete(*self.student_table.get_children())
            
            # Insert DB data into Treeview
            for row in rows:
                self.student_table.insert('', END, values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to load students: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def get_selected_student(self, event):
        """Populate input fields with selected student data from DB"""
        try:
            selected_row = self.student_table.focus()
            data = self.student_table.item(selected_row)["values"]
            
            if data:  # If a row is selected
                conn = sqlite3.connect('app.db')
                cur = conn.cursor()
                # Fetch FULL student data from DB (using Roll No. as key)
                cur.execute("SELECT * FROM student WHERE roll_no=?", (data[0],))
                student = cur.fetchone()
                conn.close()

                # Populate all input fields with DB data
                self.var_roll.set(student[0])
                self.var_name.set(student[1])
                self.var_dob.set(student[2])
                self.var_email.set(student[3])
                self.var_gender.set(student[4])
                self.var_contact.set(student[5])
                self.var_course.set(student[6])
                self.var_admission_date.set(student[7])
                self.var_state.set(student[8])
                self.var_city.set(student[9])
                self.txt_address.delete('1.0', END)
                self.txt_address.insert('1.0', student[10])
                
        except Exception as ex:
            pass  # Ignore empty clicks

    def update_student(self):
        """Update selected student in database"""
        if not self.var_roll.get().strip():
            messagebox.showerror("Error", "Select a student to update!", parent=self.root)
            return

        conn = None
        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            
            # Update student data in DB
            cur.execute("""
                UPDATE student
                SET name=?, dob=?, email=?, gender=?, contact_no=?, course=?, admission_date=?, state=?, city=?, address=?
                WHERE roll_no=?
            """, (
                self.var_name.get().strip(),
                self.var_dob.get().strip(),
                self.var_email.get().strip(),
                self.var_gender.get(),
                self.var_contact.get().strip(),
                self.var_course.get(),
                self.var_admission_date.get().strip(),
                self.var_state.get().strip(),
                self.var_city.get().strip(),
                self.txt_address.get('1.0', END).strip(),
                self.var_roll.get().strip()
            ))
            
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully!", parent=self.root)
            
            # Refresh Treeview and clear fields
            self.fetch_all_students()
            self.clear_fields()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to update student: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def delete_student(self):
        """Delete selected student from database"""
        if not self.var_roll.get().strip():
            messagebox.showerror("Error", "Select a student to delete!", parent=self.root)
            return

        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure to delete this student?", parent=self.root):
            conn = None
            try:
                conn = sqlite3.connect('app.db')
                cur = conn.cursor()
                
                # Delete student from DB (using Roll No. as key)
                cur.execute("DELETE FROM student WHERE roll_no=?", (self.var_roll.get().strip(),))
                conn.commit()
                
                messagebox.showinfo("Success", "Student deleted successfully!", parent=self.root)
                
                # Refresh Treeview and clear fields
                self.fetch_all_students()
                self.clear_fields()
                
            except Exception as ex:
                messagebox.showerror("Error", f"Failed to delete student: {str(ex)}", parent=self.root)
            finally:
                if conn:
                    conn.close()

    def search_student(self):
        """Search student by Roll No. (exact match)"""
        search_roll = self.var_search_roll.get().strip()
        conn = None
        try:
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            
            if search_roll:
                # Search for exact Roll No.
                cur.execute("SELECT roll_no, name, email, gender, dob FROM student WHERE roll_no=?", (search_roll,))
            else:
                # Show all students if search box is empty
                cur.execute("SELECT roll_no, name, email, gender, dob FROM student")
                
            rows = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            
            for row in rows:
                self.student_table.insert('', END, values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Failed to search: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        """Clear all input fields (reset form) - REMOVED var_pin"""
        self.var_roll.set("")
        self.var_name.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_contact.set("")
        self.var_course.set("")
        self.var_admission_date.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_search_roll.set("")
        self.txt_address.delete('1.0', END)

if __name__ == "__main__": 
    root = Tk()
    obj = Student(root)
    root.mainloop()