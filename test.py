import tkinter as tk
from tkinter import messagebox

def popup_file_selector(file_list):
    """
    Pop up a Tkinter window to let the user select multiple files from a given list.
    The function waits for user input and returns the selected files.
    """
    # Create a new Tkinter window
    popup = tk.Tk()
    popup.title("Select Files")

    # Variable to store the selected files
    selected_files = []

    # Create a Listbox to display the files with MULTIPLE selection mode
    listbox = tk.Listbox(popup, selectmode=tk.MULTIPLE, width=50, height=10)
    for file in file_list:
        listbox.insert(tk.END, file)
    listbox.pack(pady=10)

    # Function to handle file selection and close the popup
    def confirm_selection():
        nonlocal selected_files
        indices = listbox.curselection()
        selected_files = [file_list[i] for i in indices]

        if selected_files:
            popup.destroy()  # Close the popup after selection
        else:
            messagebox.showwarning("No Selection", "Please select at least one file.")

    # Create a button to confirm the selection
    select_button = tk.Button(popup, text="Select", command=confirm_selection)
    select_button.pack(pady=10)

    # Start the Tkinter event loop and wait until the popup is closed
    popup.mainloop()

    # Return the selected files after the window is closed
    return selected_files

# Example usage of the function
if __name__ == "__main__":
    file_list = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]
    selected_files = popup_file_selector(file_list)
    print("Selected files:", selected_files)
