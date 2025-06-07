import tkinter as tk
from tkinter import filedialog

def get_file_name():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    return filename

if __name__ == "__main__":
    fname = get_file_name()
    if fname:
        print("Selected file:", fname)
    else:
        print("No file selected.")
