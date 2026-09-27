import tkinter as tk
from tkinter import messagebox
import sys

def exit(root=None):
    # Get the root if not provided
    if root is None:
        root = tk._default_root
    
    # Confirm exit with user
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        try:
            # Close main dashboard window
            if root:
                root.destroy()
            
            # Terminate Python process
            sys.exit(0)
        
        except Exception as e:
            # If something goes wrong, try force quit
            try:
                root.quit()
            except:
                pass
            sys.exit(1)