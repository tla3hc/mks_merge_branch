import os
import logging
from utils.dev_brach_utils.sandbox_utils import Sandbox
from typing import Tuple
import filecmp
from tkinter import messagebox
import shutil
from utils.mks_utils.mks import MKS

class MergeBrach:
    _m_temp_folder = "./.tmp"
    _m_current_temp_folder = ""
    
    def __init__(self):
        logging.info('MergeBrach', 'Init')
        self.sandbox = Sandbox()
        self.mks = MKS()
        # Check if temp folder is exist, if not create it
        if not os.path.exists(self._m_temp_folder):
            os.makedirs(self._m_temp_folder)
    
    def merge_branches(self, project: str, source_branch: str, target_branch: str) -> Tuple[bool, str]:
        try:
            # Check if all arguments are provided
            if not project or not source_branch or not target_branch:
                logging.error("MergeBrach", "Project, Source Branch and Target Branch are required")
                return False, ""
            # Get number of folder in temp folder
            temp_folder_count = len(os.listdir(self._m_temp_folder))
            self._m_current_temp_folder = f"{self._m_temp_folder}/{temp_folder_count}"
            # Create temporary sandbox folder
            source_sandbox_folder = f"{self._m_current_temp_folder}/source"
            target_sandbox_folder = f"{self._m_current_temp_folder}/target"
            # Create sandboxes
            status = self.sandbox.create_sandbox(project, source_sandbox_folder, source_branch)
            if not status:
                return False, ""
            status = self.sandbox.create_sandbox(project, target_sandbox_folder, target_branch)
            if not status:
                return False, ""
            # Merge branches
            differences = self.compare_folders(source_sandbox_folder, target_sandbox_folder)
            # Popup a window to ask user to select all or manually select files
            result = messagebox.askyesno("Confirmation", "Do you want to merge ALL?")
            if result:
                # Copy and replace all files from source to target
                for file in differences:
                    file_name = file.replace(source_sandbox_folder, "")
                    target_file = f"{target_sandbox_folder}{file_name}"
                    # Check if file is exist in target folder
                    if os.path.exists(target_file):
                        # Delete file using os.remove
                        os.remove(target_file)
                    # Copy file using shutil.copy
                    shutil.copy(file, target_file)
            else:
                # Popup a window to ask user to select files manually
                tk = tk.Tk()
                
            # for file in differences:
            #     print(file)
            
            # Drop sandboxes
            # status = self.sandbox.drop_sandbox(source_sandbox_folder)
            # if not status:
            #     return False, ""
            # status = self.sandbox.drop_sandbox(target_sandbox_folder)
            # if not status:
            #     return False, ""
            return True, self._m_current_temp_folder
        except Exception as e:
            logging.error("MergeBrach", str(e))
            raise
    
    def create_tmp_sandboxes(self, project: str, source_branch: str, target_branch: str) -> Tuple[bool, str]:
        """
        Creates temporary sandboxes for the given project and branches.

        Args:
            project (str): The name of the project.
            source_branch (str): The name of the source branch.
            target_branch (str): The name of the target branch.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating success or failure, 
                              and a string with the path to the current temporary folder.

        Raises:
            Exception: If an error occurs during the creation of the sandboxes.

        Notes:
            - Logs an error if any of the required arguments are missing.
            - Creates a unique temporary folder for the sandboxes based on the current count of folders in the temp directory.
            - Creates separate sandboxes for the source and target branches.
        """
        try:
            # Check if all arguments are provided
            if not project or not source_branch or not target_branch:
                logging.error("MergeBrach", "Project, Source Branch and Target Branch are required")
                return False, ""
            # Get number of folder in temp folder
            temp_folder_count = len(os.listdir(self._m_temp_folder))
            self._m_current_temp_folder = f"{self._m_temp_folder}/{temp_folder_count}"
            # Create temporary sandbox folder
            source_sandbox_folder = f"{self._m_current_temp_folder}/source"
            target_sandbox_folder = f"{self._m_current_temp_folder}/target"
            # Create sandboxes
            status = self.sandbox.create_sandbox(project, source_sandbox_folder, source_branch)
            if not status:
                return False, ""
            status = self.sandbox.create_sandbox(project, target_sandbox_folder, target_branch)
            if not status:
                return False, ""
            return True, self._m_current_temp_folder
        except Exception as e:
            logging.error("MergeBrach", str(e))
            raise
    
    def compare_folders(self, folder_a: str, folder_b: str) -> list:
        """
        Compare two folders recursively and list all different files, including new files.
        
        :param folder_a: The path to the first folder (older version)
        :param folder_b: The path to the second folder (newer version)
        :return: A list of file paths that differ between the two folders.
        """
        differences = []

        # Compare the directories
        comparison = filecmp.dircmp(folder_a, folder_b)

        # Files only in folder_a (deleted in folder_b)
        for file in comparison.left_only:
            differences.append(os.path.join(folder_a, file))

        # Files only in folder_b (new files in the new version)
        for file in comparison.right_only:
            differences.append(os.path.join(folder_b, file))

        # Files that exist in both folders but differ
        for file in comparison.diff_files:
            differences.append(os.path.join(folder_b, file))  # Append the path from the new version

        # Recursively compare subdirectories
        for subdir in comparison.common_dirs:
            differences.extend(self.compare_folders(os.path.join(folder_a, subdir), os.path.join(folder_b, subdir)))

        return differences
    
    def merge_folder(self, source_folder: str, target_folder: str, diffent: list) -> bool:
        """_summary_
        Copy and replace all files from source to target folder based on differences list ( file path in source folder )
        Args:
            source_folder (str): _description_
            target_folder (str): _description_

        Returns:
            bool: _description_
        """
        # ./.tmp/0/source
        # ./.tmp/0/target
        # Check if source and target folder is exist
        if not os.path.exists(source_folder) or not os.path.exists(target_folder):
            logging.error("MergeBrach", "Source or Target folder is not exist")
            return False
        try:
            # Copy and replace all files from source to target
            for file in diffent:
                file = os.path.abspath(file)
                source_file = file
                target_file = file.replace('/source/', '/target/')  # Replace source with target
                # Check if file is exist in target folder 
                if os.path.exists(target_file):
                    # Delete file using os.remove
                    os.remove(target_file)
                # Copy file using shutil.copy
                if os.path.exists(source_file):
                    shutil.copy(source_file, target_file)
                    logging.info("MergeBrach", f"File {source_file} copied to {target_file}")
            return True
        except Exception as e:
            logging.error("MergeBrach", str(e))
            return False
    
    def lock_files(self, files: list) -> bool:
        """_summary_
        Lock files in the given list.
        Args:
            files (list): _description_

        Returns:
            bool: _description_
        """
        for file in files:
            file = os.path.abspath(file)
            # Lock file
            response, lock_version = self.mks.lock_member(file)
            if "error has occurred" in response.lower():
                logging.error("MergeBrach", response)
                return False
        return True
    
    def remove_lock_files(self, files: list) -> bool:
        """_summary_
        Remove lock from files in the given list.
        Args:
            files (list): _description_

        Returns:
            bool: _description_
        """
        for file in files:
            file = os.path.abspath(file)
            # Remove lock from file
            response = self.mks.unlock_member(file)
            if "error has occurred" in response.lower():
                logging.error("MergeBrach", response)
                return False
        return True