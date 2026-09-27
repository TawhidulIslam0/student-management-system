from tkinter import *
from PIL import Image, ImageTk
from course import Course
from student import Student
from result import AddResult
from viewresult import ViewResult
from exit import exit
from tkinter import messagebox
import sys
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")  
        self.root.geometry("1350x700+0+0")  
        self.root.config(bg="#FFFFFF")

        # Window dimensions
        self.window_width = 1350
        self.window_height = 700

        # Title bar
        title = Label(self.root, text="Student Result Management System",font=("times new roman", 30, "bold"), bg="#06187D", fg="#FFFFFF")
        title.place(x=0, y=0, relwidth=1, height=50)

        #Menu Frame
        menu_frame_width = 1280
        menu_frame_height = 80 
        menu_frame_x = 10
        M_Frame = LabelFrame(self.root, font=("times new roman", 15, "bold"),bg="#FFFFFF", bd=2, relief=GROOVE)
        M_Frame.place(x=menu_frame_x, y=70, width=menu_frame_width, height=menu_frame_height)

        #Menu Buttons 
        btn_width = 180
        btn_height = 40
        btn_spacing = 8
        btn_count = 4
        btn_count = 5
        button_texts = ["Student", "Course", "Result", "View Result", "Exit"]
        button_commands = [self.add_student, self.add_course, self.add_result, self.add_viewresult, self.exit_app]

        total_btn_area_width = (btn_width * btn_count) + (btn_spacing * (btn_count - 1))
        start_btn_x = (menu_frame_width - total_btn_area_width) // 2
        start_btn_y = (menu_frame_height - btn_height) // 2

        for i in range(btn_count):
            btn = Button(M_Frame, text=button_texts[i], font=("times new roman", 15, "bold"), bg="#06187D", fg="#FFFFFF", command=button_commands[i])
            btn.place(x=start_btn_x + i*(btn_width + btn_spacing), y=start_btn_y, width=btn_width, height=btn_height)

        # Background Image
        self.bg_width = 920
        self.bg_height = 350
        self.bg_x = (self.window_width - self.bg_width) // 2
        self.bg_y = 180

        # Load and display background image
        try:
            self.bg_img = Image.open("Images/background.jpg")
            self.bg_img = self.bg_img.resize((self.bg_width, self.bg_height), Image.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
            self.lbl_bg = Label(self.root, image=self.bg_img)
            self.lbl_bg.place(x=self.bg_x, y=self.bg_y, width=self.bg_width, height=self.bg_height)
        except FileNotFoundError:
            self.lbl_bg = Label(self.root, text="Background Image Not Found", font=("times new roman", 20), bg="#f0f0f0")
            self.lbl_bg.place(x=self.bg_x, y=self.bg_y, width=self.bg_width, height=self.bg_height)

        #Statistic Labels
        self.label_width = 300
        self.label_height = 80
        self.label_spacing = 10
        total_labels_width = 3 * self.label_width + 2 * self.label_spacing
        start_label_x = (self.window_width - total_labels_width) // 2
        label_y = self.bg_y + self.bg_height + 20

        # Footer
        footer = Label(self.root, text="Student Result Management System | Developed by Yu | Contact:1234567890", 
                       font=("times new roman", 12), bg="#06187D", fg="#FFFFFF") 
        footer.pack(side=BOTTOM, fill=X)

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.app = Course(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.app = Student(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.app = AddResult(self.new_win)

    def add_viewresult(self):
        self.new_win = Toplevel(self.root)
        self.app = ViewResult(self.new_win)

    def exit_app(self):
        """Exit the application"""
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            sys.exit(0)

if __name__ == "__main__": 
    root = Tk()
    obj = Dashboard(root)
    root.mainloop()