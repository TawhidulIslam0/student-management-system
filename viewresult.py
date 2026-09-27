from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from database import init_database

class ViewResult:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management System")  
        self.root.geometry("1350x700+0+0")  
        self.root.config(bg="#FFFFFF")
        self.root.focus_force()

        # Initialize database (creates tables if missing)
        init_database()

        # ===== VARIABLES =====
        self.var_search_roll = StringVar()
        self.selected_roll = StringVar()  # To store selected roll for deletion

        # ===== TITLE BAR =====
        title = Label(self.root, text="View Student Results",
                      font=("times new roman", 25, "bold"), bg="#06187D", fg="#FFFFFF")
        title.place(x=0, y=0, relwidth=1, height=60)

        # ===== SEARCH FRAME =====
        search_frame = Frame(self.root, bg="#FFFFFF")
        search_frame.place(x=50, y=80, width=1250, height=80)

        # Search Label + Entry + Buttons
        lbl_search = Label(search_frame, text="Search By | Roll No.", font=("times new roman", 15, "bold"), bg="#FFFFFF", fg="#000000")
        lbl_search.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.txt_search = Entry(search_frame, textvariable=self.var_search_roll, font=("times new roman", 15), bg="#F0F0F0")
        self.txt_search.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        btn_search = Button(search_frame, text="Search", command=self.search_result, font=("times new roman", 15, "bold"), bg="#007bff", fg="white", bd=0, cursor="hand2", width=10)
        btn_search.grid(row=0, column=2, padx=10, pady=20)
        
        btn_clear = Button(search_frame, text="Clear", command=self.clear_search, font=("times new roman", 15, "bold"), bg="#6c757d", fg="white", bd=0, cursor="hand2", width=10)
        btn_clear.grid(row=0, column=3, padx=10, pady=20)

        # ===== RESULT TABLE FRAME =====
        table_frame = Frame(self.root, bg="#FFFFFF", bd=2, relief=RIDGE)
        table_frame.place(x=50, y=180, width=1150, height=100)

        # Table (Treeview)
        self.result_table = ttk.Treeview(table_frame, columns=("roll_no", "name", "course", "marks_obtained", "total_marks", "percentage"), show="headings")
        
        # Configure columns
        self.result_table.heading("roll_no", text="Roll No")
        self.result_table.heading("name", text="Name")
        self.result_table.heading("course", text="Course")
        self.result_table.heading("marks_obtained", text="Marks Obtained")
        self.result_table.heading("total_marks", text="Total Marks")
        self.result_table.heading("percentage", text="Percentage")

        # Set column widths
        self.result_table.column("roll_no", width=150)
        self.result_table.column("name", width=200)
        self.result_table.column("course", width=200)
        self.result_table.column("marks_obtained", width=180)
        self.result_table.column("total_marks", width=180)
        self.result_table.column("percentage", width=180)

        # Pack table + scrollbars (add vertical scrollbar for safety)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.result_table.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.result_table.configure(yscrollcommand=scroll_y.set)
        self.result_table.pack(fill=BOTH, expand=1)
        
        # Bind table selection to get roll no.
        self.result_table.bind("<ButtonRelease-1>", self.get_selected_row)

        # ===== DELETE BUTTON =====
        btn_delete = Button(self.root, text="Delete", command=self.delete_result, font=("times new roman", 15, "bold"), bg="#DC3545", fg="white", bd=0, cursor="hand2", width=15)
        btn_delete.place(x=600, y=305, anchor="center")

        # ===== IMAGE FRAME =====
        img_frame = Frame(self.root, bg="#FFFFFF", bd=2, relief=RIDGE)
        img_frame.place(x=50, y=330, width=1150, height=300)

        try:
            # Relative path (works if Images folder is in project root)
            self.bg_img = Image.open("Images/view result.jpg")
            self.bg_img = self.bg_img.resize((1140, 290), Image.LANCZOS)  # 10px padding for frame
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            self.lbl_bg = Label(img_frame, image=self.bg_img)
            self.lbl_bg.pack(fill=BOTH, expand=1)
        except Exception as e:
            # Fallback text (matching AddResult style)
            self.lbl_bg = Label(img_frame, text=f"Results\n(Image Error: {str(e)[:30]})", font=("times new roman", 30, "bold"), bg="#FFFFFF", fg="#FF0000")
            self.lbl_bg.pack(fill=BOTH, expand=1)

    # ===== DATABASE METHODS (Full Connectivity) =====
    def search_result(self):
        """Search result by Roll No. from database"""
        roll_no = self.var_search_roll.get().strip()
        if not roll_no:
            messagebox.showerror("Error", "Enter Roll No. to search!", parent=self.root)
            return

        try:
            # Connect to database
            conn = sqlite3.connect('app.db')
            cur = conn.cursor()
            
            # Fetch result for the roll no.
            cur.execute("""
                SELECT roll_no, name, course, marks_obtained, full_marks 
                FROM result 
                WHERE roll_no=?
            """, (roll_no,))
            result = cur.fetchone()
            conn.close()  # Close connection immediately

            if result:
                # Calculate percentage
                marks = result[3]
                full_marks = result[4]
                percentage = (marks / full_marks) * 100 if full_marks > 0 else 0.0

                # Clear existing table data
                for row in self.result_table.get_children():
                    self.result_table.delete(row)
                
                # Insert result into table
                self.result_table.insert('', END, values=(
                    result[0],  # Roll No
                    result[1],  # Name
                    result[2],  # Course
                    result[3],  # Marks Obtained
                    result[4],  # Total Marks
                    f"{percentage:.2f}%"  # Percentage (2 decimal places)
                ))
                self.selected_roll.set(result[0])  # Store for deletion
            else:
                messagebox.showinfo("No Result", "No result found for this Roll No.!", parent=self.root)
                self.clear_search()

        except sqlite3.Error as ex:
            messagebox.showerror("Database Error", f"Failed to fetch result: {str(ex)}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Unexpected error: {str(ex)}", parent=self.root)

    def get_selected_row(self, event):
        """Get selected row's Roll No. for deletion"""
        selected_row = self.result_table.focus()
        if selected_row:
            data = self.result_table.item(selected_row)['values']
            if data:
                self.selected_roll.set(data[0])  # Roll No. is first column

    def delete_result(self):
        """Delete selected result from database"""
        roll_no = self.selected_roll.get().strip()
        if not roll_no:
            messagebox.showerror("Error", "Select a result first (search and click row)!", parent=self.root)
            return

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure to delete result for Roll No. {roll_no}?", parent=self.root):
            try:
                # Connect to database
                conn = sqlite3.connect('app.db')
                cur = conn.cursor()
                
                # Delete the result
                cur.execute("DELETE FROM result WHERE roll_no=?", (roll_no,))
                conn.commit()  # Commit deletion
                conn.close()   # Close connection
                
                messagebox.showinfo("Success", "Result deleted successfully!", parent=self.root)
                self.clear_search()  # Reset interface

            except sqlite3.Error as ex:
                messagebox.showerror("Database Error", f"Failed to delete result: {str(ex)}", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Unexpected error: {str(ex)}", parent=self.root)

    def clear_search(self):
        """Clear search input and table"""
        self.var_search_roll.set("")
        self.selected_roll.set("")
        for row in self.result_table.get_children():
            self.result_table.delete(row)

# ===== Run the Application =====
if __name__ == "__main__": 
    root = Tk()
    obj = ViewResult(root)
    root.mainloop()