import sqlite3

def init_database():
    """Create core tables (course, student, result) - for main system functionality"""
    try:
        # Connect to/Create app.db database
        conn = sqlite3.connect(database='app.db')
        cur = conn.cursor()
        
        # 1. Create Course Table (if not exists)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS course(
                course_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                duration TEXT, 
                charges TEXT, 
                description TEXT
            )
        """)
        
        # 2. Create Student Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student(
                roll_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                dob TEXT,
                email TEXT,
                gender TEXT,
                contact_no TEXT,
                course TEXT,
                admission_date TEXT,
                state TEXT,
                city TEXT,
                address TEXT
            )
        """)
        
        # 3. Create Result Table (critical for ViewResult)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS result(
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT,
                name TEXT,
                course TEXT,
                marks_obtained INTEGER,
                full_marks INTEGER,
                FOREIGN KEY (roll_no) REFERENCES student(roll_no)
            )
        """)
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        print("✅ Core database initialized (course + student + result tables created)")
    except Exception as e:
        print(f"❌ Core Database Error: {str(e)}")
        # Optional: Show pop-up error for user visibility
        import tkinter.messagebox as messagebox
        messagebox.showerror("Database Initialization Error", f"Failed to create core tables: {str(e)}")

if __name__ == "__main__":
    init_database()