import tkinter as tk
from tkinter import Listbox, MULTIPLE, Button

def select_files_from_list(file_list):
    def on_select():
        # Get the selected files
        selected = [file_list[i] for i in listbox.curselection()]
        selected_files.extend(selected)
        root.quit()  # Close the window

    selected_files = []
    
    # Create the main window
    root = tk.Tk()
    root.title("Select Files")
    
    # Create a Listbox with multiple selection
    listbox = Listbox(root, selectmode=MULTIPLE, height=10, width=50)
    
    # Add files to the Listbox
    for file in file_list:
        listbox.insert(tk.END, file)
    
    listbox.pack(padx=10, pady=10)

    # Add a button to confirm the selection
    button = Button(root, text="Select", command=on_select)
    button.pack(pady=10)
    
    root.mainloop()  # Wait for user action
    
    return selected_files

# Example usage
file_list = ["file1.txt", "file2.pdf", "file3.jpg", "file4.docx", "file5.png"]
selected = select_files_from_list(file_list)
print("Selected files:", selected)
