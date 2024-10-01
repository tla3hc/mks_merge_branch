import tkinter as tk
from tkinter import ttk

def show_popup():
    # Create a new Toplevel window (popup)
    popup = tk.Toplevel(root)
    popup.geometry("200x150")
    popup.title("Select an Option")

    # Create a Listbox widget
    listbox = tk.Listbox(popup, height=5, selectmode=tk.SINGLE)
    
    # Add options to the Listbox
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    for option in options:
        listbox.insert(tk.END, option)
    listbox.pack(pady=10)

    # Function to handle the selection
    def on_select():
        selected_index = listbox.curselection()  # Get the selected index
        if selected_index:
            selected_value = listbox.get(selected_index)
            print(f"Selected: {selected_value}")
            popup.destroy()  # Close the popup window

    # Add a button to confirm selection
    select_button = ttk.Button(popup, text="Select", command=on_select)
    select_button.pack(pady=10)

root = tk.Tk()
root.geometry("300x200")

# Button to open the popup list
open_button = ttk.Button(root, text="Open Popup List", command=show_popup)
open_button.pack(pady=50)

root.mainloop()
