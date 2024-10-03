import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox, MULTIPLE, Button

class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("Branch Merge Tool")
        self.root.geometry("650x200")  # Increase the width of the window

        # 1st row: MKS Project label, input, and "Check" button
        self.project_label = ttk.Label(root, text="MKS Project:")
        self.project_label.grid(row=0, column=0, padx=10, pady=10)

        self.project_input = ttk.Entry(root, width=50)  # Increased input field width
        self.project_input.grid(row=0, column=1, padx=10, pady=10)

        self.check_pj_button = ttk.Button(root, text="Check")
        self.check_pj_button.grid(row=0, column=3, padx=10, pady=10)

        # 2nd row: Source branch label, input, and Target branch label, input
        self.source_label = ttk.Label(root, text="Source DP:")
        self.source_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.source_input = ttk.Entry(root, width=50)  # Increased input field width
        self.source_input.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        self.select_source_branch_button = ttk.Button(root, text="Select")
        self.select_source_branch_button.grid(row=1, column=2, padx=10, pady=10)
        
        self.check_source_branch_button = ttk.Button(root, text="Check")
        self.check_source_branch_button.grid(row=1, column=3, padx=10, pady=10)

        # 3rd row:
        self.target_label = ttk.Label(root, text="Target DP:")
        self.target_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.target_input = ttk.Entry(root, width=50)  # Increased width of input
        self.target_input.grid(row=2, column=1, padx=10, pady=10)
        
        self.select_target_branch_button = ttk.Button(root, text="Select")
        self.select_target_branch_button.grid(row=2, column=2, padx=10, pady=10)
        
        self.check_target_branch_button = ttk.Button(root, text="Check")
        self.check_target_branch_button.grid(row=2, column=3, padx=10, pady=10)

        # 4th row: Circular Status light, status text, and "Merge" button
        self.status_light = tk.Canvas(root, width=30, height=30, bg="white", highlightthickness=0)
        self.status_light.grid(row=3, column=0, padx=10, pady=10)
        self._draw_circle("grey")  # Draw circle for status light

        self.status_text = ttk.Label(root, text="Idle")
        self.status_text.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.merge_button = ttk.Button(root, text="Merge")
        self.merge_button.grid(row=3, column=3, padx=10, pady=10)
    
    def select_branch(self, branches):
        # Create a new Toplevel window (popup)
        popup = tk.Toplevel(self.root)
        popup.geometry("600x150")
        popup.title("Select an branch")

        # Create a Listbox widget
        listbox = tk.Listbox(popup, height=5, width=600, selectmode=tk.SINGLE)
        
        # Add options to the Listbox
        options = branches
        for option in options:
            listbox.insert(tk.END, option)
        listbox.pack(pady=10)

        # Variable to store the selected value
        selected_value = tk.StringVar()
        
        # Function to handle the selection
        def on_select():
            selected_index = listbox.curselection()  # Get the selected index
            if selected_index:
                selected_value.set(listbox.get(selected_index))  # Store the selected value
            popup.destroy()  # Close the popup

        # Add a button to confirm selection
        select_button = ttk.Button(popup, text="Select", command=on_select)
        select_button.pack(pady=10)
        
        # Wait until the popup window is closed
        self.root.wait_window(popup)
        
        # Return the selected value
        return selected_value.get()
    
    def select_files(self, file_list):
        # Create a new Toplevel window (popup)
        popup = tk.Toplevel(self.root)
        popup.geometry("600x320")
        popup.title("Select Files")
 
        # Create a Listbox widget
        listbox = tk.Listbox(popup, height=15, width=80, selectmode=MULTIPLE)
       
        # Add options to the Listbox
        for file in file_list:
            listbox.insert(tk.END, file)
        listbox.pack(pady=10)
 
        # Variable to store the selected values
        selected_files = []
 
        # Function to handle the selection
        def on_select():
            selected_indices = listbox.curselection()  # Get the selected indices
            for index in selected_indices:
                selected_files.append(listbox.get(index))  # Store the selected values
            popup.destroy()  # Close the popup
 
        # Add a button to confirm selection
        select_button = ttk.Button(popup, text="Select", command=on_select)
        select_button.pack(pady=10)
       
        # Wait until the popup window is closed
        self.root.wait_window(popup)
       
        # Return the selected values
        return selected_files
    
    def show_success_files(self, success_obj: object) -> bool:
        # Create a new Toplevel window (popup)
        popup = tk.Toplevel(self.root)
        popup.geometry("600x320")
        popup.title("Merge Success Files")
 
        # Create a Listbox widget
        listbox = tk.Listbox(popup, height=15, width=80, selectmode=MULTIPLE)
       
        # Add options to the Listbox
        for file in success_obj:
            file_path = file
            old_revision = success_obj[file][0]
            new_revision = success_obj[file][1]
            if len(file_path.split('/')) > 2:
                # Get short file name from full path ../last_parent_path/file_name
                file_path = file_path.split('/')[-2] + '/' + file_path.split('/')[-1]
            listbox.insert(tk.END, f"{file_path} - {old_revision} -> {new_revision}")
        listbox.pack(pady=10)
        
        # Function to handle the selection
        def on_select():
            popup.destroy()  # Close the popup
 
        # Add a button to confirm selection
        select_button = ttk.Button(popup, text="OK", command=on_select)
        select_button.pack(pady=10)
       
        # Wait until the popup window is closed
        self.root.wait_window(popup)
       
        # Return the selected values
        return True
    
        
    # Function to draw a circular light instead of square
    def _draw_circle(self, color):
        self.status_light.create_oval(5, 5, 25, 25, fill=color, outline=color)

    # Function to set the status light's color
    def update_status(self, status, color):
        self.status_light.delete("all")  # Clear the canvas
        self._draw_circle(color)  # Draw the circle again with the new color
        self.status_text.config(text=status)

    def set_check_pj_button_command(self, command):
        self.check_pj_button.config(command=command)
    
    def set_check_source_brach_button_command(self, command):
        self.check_source_branch_button.config(command=command)
    
    def set_select_source_branch_button_command(self, command):
        self.select_source_branch_button.config(command=command)
        
    def set_check_target_branch_button_command(self, command):
        self.check_target_branch_button.config(command=command)
    
    def set_select_target_branch_button_command(self, command):
        self.select_target_branch_button.config(command=command)

    def set_merge_button_command(self, command):
        self.merge_button.config(command=command)

    def get_project_name(self):
        return self.project_input.get()

    def get_source_branch(self):
        return self.source_input.get()

    def get_target_branch(self):
        return self.target_input.get()
    
    def set_source_branch_input(self, branch):
        self.source_input.delete(0, tk.END)
        self.source_input.insert(0, branch)
    
    def set_target_branch_input(self, branch):
        self.target_input.delete(0, tk.END)
        self.target_input.insert(0, branch)
