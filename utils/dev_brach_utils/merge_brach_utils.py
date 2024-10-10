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
            source_sandbox_folder = os.path.abspath(source_sandbox_folder)
            target_sandbox_folder = f"{self._m_current_temp_folder}/target"
            target_sandbox_folder = os.path.abspath(target_sandbox_folder)  
            # Create sandboxes
            logging.info("MergeBrach", "Creating temporary sandboxes")
            logging.info("MergeBrach", f"Source branch: {source_branch}")  
            logging.info("MergeBrach", f"Source sandbox folder: {source_sandbox_folder}")
            status = self.sandbox.create_sandbox(project, source_sandbox_folder, source_branch)
            logging.info("MergeBrach", f"Created source sandbox: {status}")
            if not status:
                return False, ""
            logging.info("MergeBrach", f"Creating target sandbox")
            logging.info("MergeBrach", f"Target branch: {target_branch}")
            logging.info("MergeBrach", f"Target sandbox folder: {target_sandbox_folder}")
            status = self.sandbox.create_sandbox(project, target_sandbox_folder, target_branch)
            logging.info("MergeBrach", f"Created target sandbox: {status}")
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
            logging.info("MergeBrach", "Start merging folders")
            # Copy and replace all files from source to target
            for file in diffent:
                file = os.path.abspath(file)
                source_file = file
                if f'{os.path.sep}source{os.path.sep}' in file:
                    target_file = file.replace(f'{os.path.sep}source{os.path.sep}', f'{os.path.sep}target{os.path.sep}')  # Replace source with target
                else:
                    logging.error("MergeBrach", f"File path is not valid: {file}")
                    return False
                # Check if file is exist in target folder 
                if os.path.exists(target_file):
                    logging.info("MergeBrach", f"File {target_file} is exist in target folder")
                    # Delete file using os.remove
                    os.remove(target_file)
                    logging.info("MergeBrach", f"File {target_file} deleted")
                # Copy file using shutil.copy
                if os.path.exists(source_file):
                    shutil.copy(source_file, target_file)
                    logging.info("MergeBrach", f"File {source_file} copied to {target_file}")
                else:
                    logging.error("MergeBrach", f"File {source_file} is not exist")
                    return False
            logging.info("MergeBrach", "Merge folders completed")
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
        try:
            for file in files:
                file = os.path.abspath(file)
                file_name = os.path.basename(file)
                logging.info("MergeBrach", f"Locking file {file_name}")
                # Lock file
                response, lock_version = self.mks.lock_member(file)
                if "error has occurred" in response.lower():
                    logging.error("MergeBrach", response)
                    return False
                else:
                    logging.info("MergeBrach", f"File {file_name} locked with version {lock_version}")
            return True
        except Exception as e:
            logging.error("MergeBrach", str(e))
            return False
    
    def remove_lock_files(self, files: list) -> bool:
        """_summary_
        Remove lock from files in the given list.
        Args:
            files (list): _description_

        Returns:
            bool: _description_
        """
        try:
            for file in files:
                file = os.path.abspath(file)
                file_name = os.path.basename(file)
                logging.info("MergeBrach", f"Removing lock from file {file_name}")
                # Remove lock from file
                response = self.mks.unlock_member(file)
                if "error has occurred" in response.lower():
                    logging.error("MergeBrach", response)
                    return False
                else:
                    logging.info("MergeBrach", f"Lock removed from file {file_name}")
            return True
        except Exception as e:
            logging.error("MergeBrach", str(e))
            return False
        
    def checkin_members(self, member_path_list: list, description: str) -> tuple:
        """
        Checks in a list of members to the repository.

        Args:
            member_path_list (list): A list of file paths to the members to be checked in.
            description (str): A description for the check-in operation.

        Returns:
            bool: True if all members are successfully checked in, False if any error occurs.

        Logs:
            Errors if a member does not exist or if an error occurs during the check-in process.
        """
        success_list = []
        error_list = []
        for member in member_path_list:
            member_path = os.path.abspath(member)
            file_name = os.path.basename(member_path)   
            logging.info("MergeBrach", f"Checking in member {file_name}")
            # Check if member is exist
            if not os.path.exists(member_path):
                logging.error("MergeBrach", f"Member {member_path} does not exist")
                error_list.append(member_path)
                continue
            # check if file is member, if not, add to member
            member_revision = self.mks.get_member_revision(member_path)
            if not member_revision:
                response = self.mks.add_member(member_path)
                if 'added' not in response.lower():
                    logging.error("MergeBrach", f"Error occurred while adding member {member_path}")
                    error_list.append(member_path)
                else:
                    logging.info("MergeBrach", f"Member {file_name} added")
                    success_list.append(member_path)
            else:
                response = self.mks.checkin_member(member_path, description)
                if "error has occurred" in response.lower():
                    logging.error("MergeBrach", f"Error occurred while checking in member {member_path}")
                    error_list.append(member_path)
                else:
                    logging.info("MergeBrach", f"Member {file_name} checked in")
                    logging.info("MergeBrach", response)
                    success_list.append(member_path)
        return success_list, error_list
    
    def get_current_temp_folder(self) -> str:
        return self._m_current_temp_folder