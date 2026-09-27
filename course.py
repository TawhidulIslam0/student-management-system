from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from database import init_database

class Course:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")  
        self.root.geometry("1350x700+0+0")  
        self.root.config(bg="#FFFFFF")
        self.root.focus_force()

        init_database()

        # Title bar
        title = Label(self.root, text="Manage Courses Info",font=("times new roman", 30, "bold"), bg="#06187D", fg="#FFFFFF")
        title.place(x=0, y=0, relwidth=1, height=50)

        # Variables
        self.var_course_id = StringVar() 
        self.var_course_name = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search_course = StringVar()

        # Labels
        course_name = Label(self.root, text="Course Name", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        course_name.place(x=50, y=100)
        duration = Label(self.root, text="Duration", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        duration.place(x=50, y=150)
        charges = Label(self.root, text="Charges", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        charges.place(x=50, y=200)
        description = Label(self.root, text="Description", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        description.place(x=50, y=250)

        # Entry fields
        self.txt_course_name = Entry(self.root, textvariable=self.var_course_name, font=("times new roman", 20), bg="#FFFFFF", fg="#000000")
        self.txt_course_name.place(x=180, y=100, width=300)
        self.txt_duration = Entry(self.root, textvariable=self.var_duration, font=("times new roman", 20), bg="#FFFFFF", fg="#000000")
        self.txt_duration.place(x=180, y=150, width=300)
        self.txt_charges = Entry(self.root, textvariable=self.var_charges, font=("times new roman", 20), bg="#FFFFFF", fg="#000000")
        self.txt_charges.place(x=180, y=200, width=300)
        
        # Description text box
        self.txt_description = Text(self.root, font=("times new roman", 20), bg="#FFFFFF", fg="#000000")
        self.txt_description.place(x=180, y=250, height=300, width=500) 

        # Button frame
        button_frame = Frame(self.root, bg="#FFFFFF")
        button_frame.place(x=180, y=560, width=500, height=50) 
        
        # Button dimensions and spacing
        total_buttons = 4
        total_gap = total_buttons - 1  # 3 gaps between 4 buttons
        btn_width = (500 - (total_gap * 10)) // total_buttons  # 10px gap between buttons
        gap = 10  # Consistent 10px gap
        
        # Buttons
        self.btn_add = Button(button_frame, text="Add", font=("times new roman", 14, "bold"), bg="#06187D", fg="#FFFFFF", bd=0, command=self.add_course)
        self.btn_add.place(x=0, y=0, width=btn_width, height=40)
        
        self.btn_update = Button(button_frame, text="Update", font=("times new roman", 14, "bold"), bg="#06187D", fg="#FFFFFF", bd=0, command=self.update_course)
        self.btn_update.place(x=btn_width + gap, y=0, width=btn_width, height=40)
        
        self.btn_delete = Button(button_frame, text="Delete", font=("times new roman", 14, "bold"), bg="#06187D", fg="#FFFFFF", bd=0, command=self.delete_course)
        self.btn_delete.place(x=2*(btn_width + gap), y=0, width=btn_width, height=40)
        
        self.btn_clear = Button(button_frame, text="Clear", font=("times new roman", 14, "bold"), bg="#06187D", fg="#FFFFFF", bd=0, command=self.clear_fields)
        self.btn_clear.place(x=3*(btn_width + gap), y=0, width=btn_width, height=40)

        #Search Label and Entry
        search_label = Label(self.root, text="Search Course", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000", bd=2)
        search_label.place(x=700, y=100, width=140, height=40)
        
        txt_search_course = Entry(self.root, textvariable=self.var_search_course, font=("times new roman", 20), bg="#FFFFFF", fg="#000000")
        txt_search_course.place(x=850, y=100, width=250, height=40)
        
        btn_search = Button(self.root, text="Search", font=("times new roman", 14, "bold"), bg="#06187D", fg="#FFFFFF", bd=0, command=self.search_course)
        btn_search.place(x=1110, y=100, width=90, height=40)

        # Framwork for Treeview
        self.Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.Frame.place(x=700, y=150, width=500, height=400)

        scrolly = Scrollbar(self.Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.Frame, orient=HORIZONTAL)
        
        self.CourseTable = ttk.Treeview(self.Frame, columns=("course_id", "name", "duration", "charges", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        
        # Set scrollbar commands to control Treeview
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)
        
        # Place scrollbars 
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        
        self.CourseTable.heading("course_id", text="ID")
        self.CourseTable.heading("name", text="Course Name")
        self.CourseTable.heading("duration", text="Course Duration")
        self.CourseTable.heading("charges", text="Course Charges")
        self.CourseTable.heading("description", text="Course Description")
        self.CourseTable["show"]= "headings"
        
        # Set column widths 
        self.CourseTable.column("course_id", width=30)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=170)
        
        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_selected_row)

        self.fetch_all_courses()

    def add_course(self):
        conn = None
        try:
            if not self.var_course_name.get().strip():
                messagebox.showerror("Error", "Course Name is required", parent=self.root)
                return
            
            # connect to database
            conn = sqlite3.connect(database='app.db')
            cur = conn.cursor()
            
            # check if course already exists
            cur.execute("SELECT * FROM course WHERE name=?", (self.var_course_name.get().strip(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Course already exists!", parent=self.root)
                return
            
            # add course
            cur.execute(""" INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?) """,
            (
                self.var_course_name.get().strip(),
                self.var_duration.get().strip(),
                self.var_charges.get().strip(),
                self.txt_description.get('1.0', END).strip()
            ))
            
            conn.commit()
            messagebox.showinfo("Success", "Course added successfully", parent=self.root)
            
            # update table, clear fields
            self.fetch_all_courses()
            self.clear_fields()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def fetch_all_courses(self):
        conn = None
        try:
            conn = sqlite3.connect(database='app.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            
            self.CourseTable.delete(*self.CourseTable.get_children())
            
            for row in rows:
                self.CourseTable.insert('', END, values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def get_selected_row(self, event):
        try:
            selected_row = self.CourseTable.focus()
            data = self.CourseTable.item(selected_row)["values"]
            
            if data:
                self.var_course_id.set(data[0])
                self.var_course_name.set(data[1])
                self.var_duration.set(data[2])
                self.var_charges.set(data[3])
    
                self.txt_description.delete('1.0', END)
                self.txt_description.insert('1.0', data[4])
                
        except Exception as ex:
            pass

    def update_course(self):
        conn = None
        try:
            if not self.var_course_id.get():
                messagebox.showerror("Error", "Please select a course to update!", parent=self.root)
                return
            
            if not self.var_course_name.get().strip():
                messagebox.showerror("Error", "Course Name is required", parent=self.root)
                return
            
            conn = sqlite3.connect(database='app.db')
            cur = conn.cursor()
            
            cur.execute("""
                UPDATE course 
                SET name=?, duration=?, charges=?, description=? 
                WHERE course_id=?
            """, (
                self.var_course_name.get().strip(),
                self.var_duration.get().strip(),
                self.var_charges.get().strip(),
                self.txt_description.get('1.0', END).strip(),
                self.var_course_id.get()
            ))
            
            conn.commit()
            messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
            self.fetch_all_courses()
            self.clear_fields()
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def delete_course(self):
        conn = None
        try:
            if not self.var_course_id.get():
                messagebox.showerror("Error", "Please select a course to delete!", parent=self.root)
                return
            
            if messagebox.askyesno("Confirm", "Are you sure to delete this course?", parent=self.root):
                conn = sqlite3.connect(database='app.db')
                cur = conn.cursor()
                cur.execute("DELETE FROM course WHERE course_id=?", (self.var_course_id.get(),))
                conn.commit()
                messagebox.showinfo("Success", "Course deleted successfully", parent=self.root)
                self.fetch_all_courses()
                self.clear_fields()
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def search_course(self):
        conn = None
        try:
            search_term = self.var_search_course.get().strip()
            conn = sqlite3.connect(database='app.db')
            cur = conn.cursor()
            
            if search_term:
                cur.execute("SELECT * FROM course WHERE name LIKE ?", (f"%{search_term}%",))
            else:
                cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        self.var_course_id.set("")
        self.var_course_name.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search_course.set("")
        self.txt_description.delete('1.0', END)

if __name__ == "__main__": 
    root = Tk()
    obj = Course(root)
    root.mainloop()