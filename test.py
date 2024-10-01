import tkinter as tk
from tkinter import ttk

def open_listbox_popup():
    # Create a new Toplevel window (popup)
    popup = tk.Toplevel(root)
    popup.geometry("300x200")
    popup.title("Select an Option")

    # Variable to store the selected value
    selected_value = tk.StringVar()

    # Create a Listbox widget
    listbox = tk.Listbox(popup, height=5, selectmode=tk.SINGLE)
    
    # Add options to the Listbox
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    for option in options:
        listbox.insert(tk.END, option)
    listbox.pack(pady=10)

    # Function to handle selection
    def on_select():
        selected_index = listbox.curselection()  # Get the selected index
        if selected_index:
            selected_value.set(listbox.get(selected_index))  # Store the selected value
        popup.destroy()  # Close the popup

    # Add a button to confirm selection
    select_button = ttk.Button(popup, text="Select", command=on_select)
    select_button.pack(pady=10)

    # Wait until the popup window is closed
    root.wait_window(popup)

    # Return the selected value
    return selected_value.get()

def show_popup_result():
    # Open the popup and get the selected value
    selected = open_listbox_popup()
    if selected:
        result_label.config(text=f"You selected: {selected}")
    else:
        result_label.config(text="No selection made")

root = tk.Tk()
root.geometry("400x300")

# Button to open the popup
open_button = ttk.Button(root, text="Open Popup List", command=show_popup_result)
open_button.pack(pady=50)

# Label to display the result
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
