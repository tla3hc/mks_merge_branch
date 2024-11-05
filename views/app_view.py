import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox, MULTIPLE, Button
import os
import logging


class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("Branch Merge Tool")
        self.root.geometry("650x235")  # Increase the width of the window
        app_bg_color = root.cget("bg")  # Get the background color of the root window

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
        
        # 4th row:
        # Add dropdown (combobox)
        # Add "Mode" label
        mode_label = tk.Label(root, text="Mode:")
        mode_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        mode_options = ["Model + Code + Test(SCA, MXAM)", "Model", "Code", "Test(SCA, MXAM)"]
        self.mode_dropdown = ttk.Combobox(root, values=mode_options, justify="left", width=35, state='readonly')
        self.mode_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.mode_dropdown.current(0)  # Set default value

        self.merge_button = ttk.Button(root, text="Merge")
        self.merge_button.grid(row=3, column=3, padx=10, pady=10)
        
        # 5th row:
        # Add status light
        self.status_light = tk.Canvas(root, width=30, height=30, bg=app_bg_color, highlightthickness=0)
        self.status_light.grid(row=4, column=0, padx=10, pady=10, sticky="ns")
        self._draw_circle("grey")  # Draw circle for status light

        self.status_text = ttk.Label(root, text="Idle")
        self.status_text.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    
    def select_branch(self, branches):
        """
        Opens a popup window with a list of branches for the user to select from.
        Args:
            branches (list): A list of branch names to display in the Listbox.
        Returns:
            str: The name of the selected branch.
        This method creates a Toplevel window containing a Listbox widget populated
        with the provided branch names. The user can select a branch from the Listbox
        and confirm their selection by clicking the "Select" button. The selected branch
        name is then returned.
        The popup window includes horizontal and vertical scrollbars for the Listbox,
        and the Listbox is configured to expand with the window resize. The method
        waits for the popup window to close before returning the selected value.
        """
        # Create a new Toplevel window (popup)
        popup = tk.Toplevel(self.root)
        popup.minsize(600, 320)
        popup.title("Select an branch")

        # Create a Listbox widget
        x_scrollbar = tk.Scrollbar(popup, orient=tk.HORIZONTAL)
        y_scrollbar = tk.Scrollbar(popup, orient=tk.VERTICAL)
        listbox = tk.Listbox(popup, height=15, width=80, selectmode=tk.SINGLE, 
                    xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        
        # Configure scrollbars
        x_scrollbar.config(command=listbox.xview)
        y_scrollbar.config(command=listbox.yview)
        
        # Grid layout for listbox and scrollbars
        listbox.grid(row=0, column=0, sticky="nsew")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Allow the listbox to expand with window resize
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)
        
        # Add options to the Listbox
        options = branches
        for option in options:
            listbox.insert(tk.END, option)

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
        select_button.grid(row=2, column=0, pady=10)
        
        # Adjust the row height for the button
        popup.grid_rowconfigure(2, weight=0)
        
        # Wait until the popup window is closed
        self.root.wait_window(popup)
        
        # Return the selected value
        return selected_value.get()
    
    def select_files(self, file_list, title):
        """
        Opens a popup window with a list of files for the user to select from.
        Args:
            file_list (list): A list of file names to display in the Listbox.
        Returns:
            list: A list of selected file names.
        The function creates a Toplevel window containing a Listbox widget with horizontal and vertical scrollbars.
        The user can select multiple files from the Listbox. Upon clicking the "Select" button, the selected file names
        are returned as a list. The popup window is closed after the selection is made.
        """
        # Create a new Toplevel window (popup)
        popup = tk.Toplevel(self.root)
        popup.minsize(600, 320)
        popup.title(title)
 
        # Create a Listbox widget
        x_scrollbar = tk.Scrollbar(popup, orient=tk.HORIZONTAL)
        y_scrollbar = tk.Scrollbar(popup, orient=tk.VERTICAL)
        # listbox = tk.Listbox(popup, height=15, width=80, selectmode=MULTIPLE, xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        # Create the Listbox
        listbox = tk.Listbox(popup, height=15, width=80, selectmode=tk.MULTIPLE, 
                    xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

        # Configure scrollbars
        x_scrollbar.config(command=listbox.xview)
        y_scrollbar.config(command=listbox.yview)
        
        # Grid layout for listbox and scrollbars
        listbox.grid(row=0, column=0, sticky="nsew")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Allow the listbox to expand with window resize
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)
       
        # Add options to the Listbox
        for file in file_list:
            listbox.insert(tk.END, file)
        # listbox.pack(pady=10)
 
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
        select_button.grid(row=2, column=0, pady=10)
        
        # Adjust the row height for the button
        popup.grid_rowconfigure(2, weight=0)
       
        # Wait until the popup window is closed
        self.root.wait_window(popup)
       
        # Return the selected values
        return selected_files
    
    def show_merge_report(self, success_obj: object, error_list: list) -> bool:
        """
        Displays a popup window with a list of successfully merged files.
        Args:
            success_obj (object): A dictionary-like object containing file paths as keys and 
                      dictionaries with 'old' and 'new' revision information as values.
        Returns:
            bool: Always returns True after the popup window is closed.
        The popup window contains a Listbox widget that displays the file names along with their 
        old and new revision numbers. The user can scroll through the list using horizontal and 
        vertical scrollbars. An "OK" button is provided to close the popup window.
        """
        # Create a new Toplevel window (popup)
        popup = tk.Toplevel(self.root)
        popup.minsize(600, 320)
        popup.title("Merge report")
 
        # Create a Listbox widget
        x_scrollbar = tk.Scrollbar(popup, orient=tk.HORIZONTAL)
        y_scrollbar = tk.Scrollbar(popup, orient=tk.VERTICAL)
        listbox = tk.Listbox(popup, height=15, width=80, selectmode=tk.MULTIPLE, 
                    xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
        
        # Configure scrollbars
        x_scrollbar.config(command=listbox.xview)
        y_scrollbar.config(command=listbox.yview)
        
        # Grid layout for listbox and scrollbars
        listbox.grid(row=0, column=0, sticky="nsew")
        x_scrollbar.grid(row=1, column=0, sticky="ew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Allow the listbox to expand with window resize
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)
       
        # Add options to the Listbox
        for file in success_obj:
            file_path = file
            old_revision = success_obj[file]['old']
            if not old_revision:
                old_revision = '?'
            new_revision = success_obj[file]['new']
            if not new_revision:
                new_revision = '?'
            # using os get file name from file path
            file_path = os.path.basename(file_path)
            listbox.insert(tk.END, f"Succesfully merged file: {file_path} - {old_revision} -> {new_revision}")
            logging.info("Succesfully merged file: ", f"{file_path} - {old_revision} -> {new_revision}")
        

        for file in error_list:
            error_message = f"Error merging file: {file}"
            listbox.insert(tk.END, error_message)
            logging.error("Error merging file: ", file)
        
        # Function to handle the selection
        def on_select():
            popup.destroy()  # Close the popup
 
        # Add a button to confirm selection
        select_button = ttk.Button(popup, text="OK", command=on_select)
        select_button.grid(row=2, column=0, pady=10)
        
        # Adjust the row height for the button
        popup.grid_rowconfigure(2, weight=0)
       
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
        self.status_text.config(text="")
        self.root.update_idletasks() 
        self._draw_circle(color)  # Draw the circle again with the new color
        self.status_text.config(text=status)
        self.root.update_idletasks() 

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
    
    def get_merge_mode(self):
        # Return index of the selected mode
        return self.mode_dropdown.current()
    
    def set_source_branch_input(self, branch):
        self.source_input.delete(0, tk.END)
        self.source_input.insert(0, branch)
    
    def set_target_branch_input(self, branch):
        self.target_input.delete(0, tk.END)
        self.target_input.insert(0, branch)
