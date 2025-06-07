import tkinter as tk
from tkinter import filedialog

def get_file_name():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=[("Text Files", "*.txt")]
    )
    return file_path

if __name__ == "__main__":
    filename = get_file_name()
    print("Selected file:", filename)
