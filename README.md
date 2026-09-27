A comprehensive desktop application built with Python and Tkinter for managing student records, courses, and examination results. This system provides an intuitive interface for educational institutions to streamline their result management process.

## 📁 Project Structure

```
Student-Result-Management-System/
│
├── dashboard.py          # Main dashboard window
├── course.py             # Course management module
├── student.py            # Student management module
├── result.py             # Add result module
├── viewresult.py         # View and manage results
├── database.py           # Database initialization
├── exit.py               # Exit confirmation utility
│
├── Images/               # Image assets
│   ├── background.jpg
│   ├── result.png
│   └── view result.jpg
│
└── app.db                # SQLite database (auto-generated)
```

## How to Use

1. Start with Dashboard
   - Launch the application from `dashboard.py`
   - Navigate to different modules using menu buttons

2. Add Courses First
   - Go to Course module
   - Add courses before registering students
   - Courses will appear in student registration dropdown

3. Register Students
   - Add student details
   - Select course from dropdown
   - Save to database

4. Add Results
   - Select student from dropdown
   - Enter marks obtained and full marks
   - Submit to save result

5. View Results
   - Search by Roll No.
   - View marks and calculated percentage
   - Delete if necessary

## 🎯 Key Features Highlight

- Data Integrity:Foreign key constraints ensure valid student-course relationships
- Input Validation: Comprehensive validation for all user inputs
- User-Friendly: Clean interface with proper spacing and visual hierarchy
- Error Handling: Graceful error messages for database operations
- Real-time Updates: Tables refresh automatically after CRUD operations
