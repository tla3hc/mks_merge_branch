import tkinter as tk
from tkinter import messagebox

class FileSelector:
    def __init__(self, master, file_list):
        self.master = master
        self.file_list = file_list
        self.selected_files = []
        
        self.create_popup()

    def create_popup(self):
        # Create a Toplevel window
        self.popup = tk.Toplevel(self.master)
        self.popup.title("Select Files")

        # Create a Listbox to display the files with MULTIPLE selection mode
        self.listbox = tk.Listbox(self.popup, selectmode=tk.MULTIPLE, width=50, height=10)
        for file in self.file_list:
            self.listbox.insert(tk.END, file)
        self.listbox.pack(pady=10)

        # Create a button to confirm the selection
        self.select_button = tk.Button(self.popup, text="Select", command=self.select_files)
        self.select_button.pack(pady=5)

    def select_files(self):
        # Get all selected files
        indices = self.listbox.curselection()
        self.selected_files = [self.file_list[i] for i in indices]

        if self.selected_files:
            messagebox.showinfo("Files Selected", f"You selected: {', '.join(self.selected_files)}")
            self.popup.destroy()  # Close the popup after selection
        else:
            messagebox.showwarning("No Selection", "Please select at least one file.")

# Main application
def main():
    root = tk.Tk()
    root.title("Multiple File Selector Example")

    # Example list of files
    file_list = [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "file4.txt",
        "file5.txt"
    ]

    # Create a button to open the file selection popup
    btn = tk.Button(root, text="Select Files", command=lambda: FileSelector(root, file_list))
    btn.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
