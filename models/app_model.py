from utils.mks_utils.mks import MKS
import logging
from utils.dev_brach_utils.merge_brach_utils import MergeBrach
from tkinter import messagebox
import os

class AppModel:
    def __init__(self):
        logging.info('AppModel', 'Init')
        self.project_name = ""
        self.source_branch = ""
        self.target_branch = ""
        self.status = "Idle"
        self.mks = MKS()
        self.project = None
        self.merge_branch = MergeBrach()
        self.mks_locked_files = []
    
    def get_project_info(self, project_name):
        """
        Retrieves project information for the specified project name and adds "Mainline" to the list of development paths.

        Args:
            project_name (str): The name of the project to retrieve information for.

        Raises:
            Exception: If an error occurs while retrieving the project information, it logs the error and re-raises the exception.
        """
        try:
            logging.info("AppModel", "Getting project info")
            self.project = self.mks.get_project_info(project_name)
            # add "Mainline" to the list of dev paths
            if self.project:
                self.project.dev_paths.append("Mainline")
        except Exception as e:
            logging.error("AppModel", str(e))
            raise

    def set_project_name(self, project_name):
        """
        Sets the project name for the instance, ensuring it follows a specific format.

        This method performs the following steps:
        1. Removes any trailing '/' or '\' from the provided project name.
        2. Ensures the project name ends with '/project.pj'. If not, appends '/project.pj' to the project name.

        Args:
            project_name (str): The name of the project to be set.

        Attributes:
            project_name (str): The formatted project name.
        """
        # Check if project name end with / or \ and remove it
        if project_name.endswith("/") or project_name.endswith("\\"):
            project_name = project_name[:-1]
        # Check if the project name contain /project.pj at the end, if not add it
        if not project_name.endswith("/project.pj"):
            project_name += "/project.pj"
        self.project_name = project_name
    
    def check_branch(self, branch: str) -> bool:
        """
        Checks if the given branch exists in the project's development paths.

        Args:
            branch (str): The name of the branch to check.

        Returns:
            bool: True if the branch is valid and exists in the project's development paths, False otherwise.

        Raises:
            Exception: If there is an error retrieving project information.

        Logs:
            - "Branch(es) Required": If the branch parameter is empty.
            - "Valid Branch": If the branch exists in the project's development paths.
            - "Project Not Found or Invalid Branch": If the project is not found or the branch is invalid.
            - "Project Required": If the project name is not provided.
            - "Branch Not Found": If the branch does not exist in the project's development paths.
        """
        if not branch:
            self.status = "Branch(es) Required"
            logging.error("AppModel", self.status)
            return False
        # Check the source branch in MKS
        if self.project:
            if branch in self.project.dev_paths:
                self.status = "Valid Branch"
                logging.info("AppModel", self.status)
                return True
        else:
            if self.project_name:
                try:
                    self.get_project_info(self.project_name)
                    if branch in self.project.dev_paths:
                        self.status = "Valid Branch"
                        logging.info("AppModel", self.status)
                        return True
                except Exception as e:
                    self.status = "Project Not Found or Invalid Branch"
                    logging.error("AppModel", str(e))
                    return False
            else:
                self.status = "Project Required"
                logging.error("AppModel", self.status)
                return False
        self.status = "Branch Not Found"
        logging.error("AppModel", self.status)
        return False
    
    def set_source_branch(self, source: str) -> bool:
        """
        Sets the source branch if it is valid.

        Args:
            source (str): The name of the source branch to set.

        Returns:
            bool: True if the source branch is valid and set successfully, False otherwise.
        """
        # Check if the source branch is valid
        if not self.check_branch(source):
            logging.error("AppModel", "Invalid Source Branch")
            return False
        self.source_branch = source
        self.status = "Valid Source Branch"
        logging.info("AppModel", f'Valid Source Branch: {source}')
        return True

    def set_target_branch(self, target: str) -> bool:
        """
        Sets the target branch if it is valid.

        Args:
            target (str): The name of the target branch to set.

        Returns:
            bool: True if the target branch is valid and set successfully, False otherwise.
        """
        # Check if the target branch is valid
        if not self.check_branch(target):
            logging.error("AppModel", "Invalid Target Branch")
            return False
        self.target_branch = target
        self.status = "Valid Target Branch"
        logging.info("AppModel", f'Valid Target Branch: {target}')  
        return True
        
    def check_project(self):
        """
        Checks if the project name is set and validates the project in MKS.

        This method performs the following steps:
        1. Checks if the `project_name` attribute is set. If not, sets the `status` attribute to "Project Required",
           logs an error, and returns False.
        2. Attempts to retrieve project information using the `get_project_info` method. If an exception occurs,
           sets the `status` attribute to "Project Not Found", logs the exception, and returns False.
        3. If the project is successfully validated, sets the `status` attribute to "Valid Project" and returns True.

        Returns:
            bool: True if the project is valid, False otherwise.
        """
        if not self.project_name:
            self.status = "Project Required"
            logging.error("AppModel", self.status)
            return False
        # Check the project in MKS
        try:
            self.get_project_info(self.project_name)
        except Exception as e:
            self.status = "Project Not Found"
            logging.error("AppModel", str(e))
            return False
        self.status = "Valid Project"
        logging.info("AppModel", f'Valid Project: {self.project_name}')
        return True

    def get_dev_paths(self):
        """
        Retrieves the development paths for the current project.

        This method checks if the project is set and retrieves the project information
        if necessary. It handles various error conditions and logs appropriate error
        messages. If the project has no development paths, it updates the status and
        logs an error.

        Returns:
            list: A list of development paths for the current project. Returns an empty
            list if the project is not found, not set, or has no development paths.
        """
        if not self.project:
            # if the project name is set, get the project info
            if self.project_name:
                try:
                    self.get_project_info(self.project_name)
                except Exception as e:
                    self.status = "Project Not Found"
                    logging.error("AppModel", str(e))
                    return []
            else:
                self.status = "Project Required, input and press 'Check'"
                logging.error("AppModel", self.status)
                return []
        if len(self.project.dev_paths) == 0:
            self.status = "No branches found"
            logging.error("AppModel", self.status)
            return []
        return self.project.dev_paths

    def get_status(self):
        return self.status
    
    def __check_diff_is_code(self, diff: str) -> bool:
        """
        Check if the given diff path corresponds to a code file.

        This method determines if the provided diff path string contains the folder "20_IMPL" 
        and if the child folder of "20_IMPL" contains "SW_".

        Args:
            diff (str): The diff path string to check.

        Returns:
            bool: True if the diff path contains "20_IMPL" and its child folder contains "SW_", 
                  False otherwise.
        """
        # The different file is code if its path contains folder "20_IMPL" and the foder child of "20_IMPL" contains "SW_"
        # Split the path by os path separator
        diff = diff.split(os.sep)
        # Check if the path contains "20_IMPL" and "SW_"
        if "20_IMPL" in diff:
            if "SW_" in diff[diff.index("20_IMPL")+1]: 
                return True
        return False
    
    def __check_diff_is_model(self, diff: str) -> bool:
        """
        Check if the given file path corresponds to a model file.

        A file is considered a model file if its path contains the folder "20_IMPL" 
        and one of the following folders: "DataDic", "Model", or "Library".

        Args:
            diff (str): The file path to check.

        Returns:
            bool: True if the file path corresponds to a model file, False otherwise.
        """
        # The different file is model if its path contains folder "20_IMPL" and "DataDic" or "Model" or "Library"
        # Split the path by os path separator
        diff = diff.split(os.sep)
        # Check if the path contains "20_IMPL" and "DataDic" or "Model" or "Library"
        if "20_IMPL" in diff:
            if "DataDic" in diff or "Model" in diff or "Library" in diff:
                return True
        return False
    
    def __check_diff_is_test(self, diff: str) -> bool:
        """
        Check if the given file path corresponds to a test file.

        A file is considered a test file if its path contains the folder "30_T" 
        and either "20_MGC" or "40_SCA".

        Args:
            diff (str): The file path to check.

        Returns:
            bool: True if the file path is a test file, False otherwise.
        """
        # The different file is test if its path contains folder "30_T" and "20_MGC" or "40_SCA"
        # Split the path by os path separator
        diff = diff.split(os.sep)
        # Check if the path contains "30_T" and "20_MGC" or "40_SCA"
        if "30_T" in diff:
            if "20_MGC" in diff or "40_SCA" in diff:
                return True
        return False
            
    def __merge(self, view: object, differences: list, temp_source_folder: str, temp_target_folder: str, source_branch: str, target_branch: str) -> bool:
        """
        Merges differences from a source branch to a target branch.
        Args:
            view (object): The view object to update status and show success files.
            differences (list): List of files that have differences to be merged.
            temp_source_folder (str): Temporary folder path for the source branch.
            temp_target_folder (str): Temporary folder path for the target branch.
            source_branch (str): The name of the source branch.
            target_branch (str): The name of the target branch.
        Returns:
            bool: True if the merge is successful, False otherwise.
        Raises:
            Exception: If any error occurs during the merge process.
        The method performs the following steps:
        1. Makes the sandboxes writable.
        2. Copies selected files from the source to the target folder.
        3. Locks the copied files.
        4. Gets the member revisions before check-in.
        5. Checks in the copied files.
        6. Gets the member revisions after check-in.
        7. Releases the locks on the files.
        8. Drops the sandboxes.
        9. Shows a popup window with the files that were successfully merged.
        """
        try:
            selected = differences
            logging.info("AppModel", selected)
            # Make sandbox writable
            view.update_status("Making Sandboxes Writable...", "yellow")
            # self.status = "Making Sandboxes Writable..."
            logging.info("AppModel", "Making Sandboxes Writable")
            response = self.mks.make_sandbox_writable(temp_source_folder)
            logging.info("AppModel", response)
            response = self.mks.make_sandbox_writable(temp_target_folder)
            logging.info("AppModel", response)
            # Copy selected files from source to target
            view.update_status("Copying Selected Files...", "yellow")
            self.status = "Copying Selected Files..."
            logging.info("AppModel", "Copying Selected Files")
            status = self.merge_branch.merge_folder(temp_source_folder, temp_target_folder, selected)
            if not status:
                self.status = "Merge Failed"
                # Drop sandboxes
                view.update_status("Dropping Sandboxes...", "yellow")
                # self.status = "Dropping Sandboxes..."
                logging.info("AppModel", "Dropping Sandboxes")
                response = self.mks.drop_sandbox(temp_source_folder)
                logging.info("AppModel", f"Drop source sandbox: {response}")
                response = self.mks.drop_sandbox(temp_target_folder)
                logging.info("AppModel", f"Drop target sandbox: {response}")
                return False
            logging.info("AppModel", f"Merge status: {status}")
            # List files that are copied
            copied_files = []
            for file in selected:
                file = file.replace('source', 'target')
                # get absolute path of the file
                file = os.path.abspath(file)
                copied_files.append(file)
            # Lock files
            logging.info("AppModel", "Locking Files")
            view.update_status("Locking Files...", "yellow")
            # self.status = "Locking Files..."
            logging.info("AppModel", "Locking Files")
            status = self.merge_branch.lock_files(copied_files)
            self.mks_locked_files = copied_files
            if not status:
                self.status = "Merge Failed"
                logging.error("AppModel", f"Lock files failed: {status}")
                return False
            # Get members revision before checkin
            mem_revision = {}
            for file in copied_files:
                if not file in mem_revision:
                    mem_revision[file] = {}
                mem_revision[file]['old'] = self.mks.get_member_revision(file)
            # Checkin files
            logging.info("AppModel", "Checkin Files")
            view.update_status("Checkin Files...", "yellow")
            # self.status = "Checkin Files..."
            logging.info("AppModel", "Checkin Files")
            discprition = "Merged files from branch " + source_branch + " to " + target_branch
            success_list, error_list = self.merge_branch.checkin_members(copied_files, discprition)
            # Get members revision after checkin
            for file in success_list:
                if file in mem_revision:
                    mem_revision[file]['new'] = self.mks.get_member_revision(file)
            # Release locks
            view.update_status("Releasing Locks...", "yellow")
            # self.status = "Releasing Locks..."
            logging.info("AppModel", "Releasing Locks")
            status = self.merge_branch.remove_lock_files(copied_files)
            if not status:
                self.status = "Merge Failed"
                logging.error("AppModel", f"Release locks failed: {status}")
            else:
                self.mks_locked_files = []
            # Drop sandboxes
            view.update_status("Dropping Sandboxes...", "yellow")
            # self.status = "Dropping Sandboxes..."
            logging.info("AppModel", "Dropping Sandboxes")
            response = self.mks.drop_sandbox(temp_source_folder)
            logging.info("AppModel", f"Drop source sandbox: {response}")
            response = self.mks.drop_sandbox(temp_target_folder)
            logging.info("AppModel", f"Drop target sandbox: {response}")
            
            #Popup a window showing the files that are successfully merged
            view.show_merge_report(mem_revision, error_list)
            return True
        except Exception as e:
            self.status = "Merge Failed"
            logging.error("AppModel", str(e))
            raise
    
    def merge_branches(self, view, model, project_name: str, source_branch: str, target_branch: str, merge_mode: int) -> bool:
        """
        Merges the source branch into the target branch for a given project.
        Args:
            view: The view object to update the status and interact with the user.
            model: The model object to interact with the project data.
            project_name (str): The name of the project.
            source_branch (str): The name of the source branch to merge from.
            target_branch (str): The name of the target branch to merge into.
        Returns:
            bool: True if the merge is successful, False otherwise.
        Raises:
            Exception: If there is an error while getting project info or during the merge process.
        Steps:
            1. Update the status to "Merging...".
            2. Validate the inputs.
            3. Normalize the project name.
            4. Check if the project name is different from the current project name and update project info if needed.
            5. Validate the source and target branches.
            6. Create temporary sandboxes for the merge.
            7. Compare the source and target folders.
            8. Ask the user to confirm if they want to merge all files or select files manually.
            9. Copy and replace files based on user selection.
            10. Make sandboxes writable if needed.
            11. Drop the temporary sandboxes.
            12. Update the status to "Merge Complete".
        """
        try:
            view.update_status("Merging...", "yellow")
            # self.status = "Merging..."
            logging.info("AppModel", "#"*150)
            logging.info("AppModel", "Merging...")
            if not project_name or not self.source_branch or not self.target_branch:
                self.status = "All inputs Required"
                logging.info("AppModel", self.status)
                return False
            # Check if project name is end with / or \ and remove it
            if project_name.endswith("/") or project_name.endswith("\\"):
                project_name = project_name[:-1]
            # Check if project name is end with /project.pj and add it if not
            if not project_name.endswith("/project.pj"):
                project_name += "/project.pj"
            # Check if the project name is different from the current project name
            if project_name != self.project_name:
                # Get the project info
                try:
                    view.update_status("Checking Project...", "yellow")
                    # self.status = "Checking Project..."
                    logging.info("AppModel", "Checking Project")
                    self.get_project_info(project_name)
                except Exception as e:
                    self.status = "Project Not Found"
                    logging.error("AppModel", str(e))
                    return False
            # Check if the source and target branches are valid
            if not self.set_source_branch(source_branch) or not self.set_target_branch(target_branch):
                self.status = "Invalid Source or Target Branch"
                logging.error("AppModel", self.status)
                return False
            # Merge the source branch into the target branch
            view.update_status("Creating Sandboxes...", "yellow")
            # self.status = "Creating Sandboxes..."
            logging.info("AppModel", "Creating Sandboxes")
            status, temp_folder = self.merge_branch.create_tmp_sandboxes(project_name, source_branch, target_branch)
            if not status:
                self.status = "Merge Failed"
                logging.error("AppModel", "Create Sandboxes Failed")
                return False
            temp_source_folder = f"{temp_folder}/source"
            temp_source_folder = os.path.abspath(temp_source_folder)
            temp_target_folder = f"{temp_folder}/target"
            temp_target_folder = os.path.abspath(temp_target_folder)
            # Compare the source and target folders
            view.update_status("Comparing Folders...", "yellow")
            # self.status = "Comparing Folders..."
            modified, new_files, deleted_files = self.merge_branch.compare_folders(temp_target_folder, temp_source_folder)
            original_modified_len = len(modified)
            original_new_files_len = len(new_files)
            original_deleted_files_len = len(deleted_files)
            if original_modified_len == 0 and original_new_files_len == 0 and original_deleted_files_len == 0:
                view.update_status("2 sandboxes are identical", "red")
                logging.info("AppModel", "2 sandboxes are identical, merge canceled")
                return False
            # TODO: Handle merge_mode
            # Mode 0: Merge Model + Code + Test(SCA, MXAM)
            if merge_mode == 0:
                logging.debug("AppModel", f"Merge mode: {merge_mode} - Merge All")
                # Filter modified based on the merge mode
                for diff in modified:
                    if not self.__check_diff_is_code(diff) and not self.__check_diff_is_model(diff) and not self.__check_diff_is_test(diff):
                        logging.debug("AppModel", f"Remove {diff}")
                        modified.remove(diff)
                # Check if there are no modified left
                if len(modified) == 0 and original_modified_len > 0:
                    view.update_status("No files to merge", "red")
                    logging.info("AppModel", "No files to merge, merge canceled")
                    return False
                # Filter new files based on the merge mode
                for diff in new_files:
                    if not self.__check_diff_is_code(diff) and not self.__check_diff_is_model(diff) and not self.__check_diff_is_test(diff):
                        logging.debug("AppModel", f"Remove {diff}")
                        new_files.remove(diff)
                # Check if there are no new files left
                if len(new_files) == 0 and original_new_files_len > 0:
                    view.update_status("No new files to merge", "red")
                    logging.info("AppModel", "No new files to merge, merge canceled")
                    return False
                # Filter deleted files based on the merge mode
                for diff in deleted_files:
                    if not self.__check_diff_is_code(diff) and not self.__check_diff_is_model(diff) and not self.__check_diff_is_test(diff):
                        logging.debug("AppModel", f"Remove {diff}")
                        deleted_files.remove(diff)
                # Check if there are no deleted files left
                if len(deleted_files) == 0 and original_deleted_files_len > 0:
                    view.update_status("No deleted files to merge", "red")
                    logging.info("AppModel", "No deleted files to merge, merge canceled")
                    return False
                
            # Mode 1: Merge Model
            elif merge_mode == 1:
                logging.debug("AppModel", f"Merge mode: {merge_mode} - Merge Model")
                # Filter modified based on the merge mode
                for diff in modified:
                    if not self.__check_diff_is_model(diff):
                        modified.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no modified left
                if len(modified) == 0 and original_modified_len > 0:
                    view.update_status("No model files to merge", "red")
                    logging.info("AppModel", "No model files to merge, merge canceled")
                    return False
                # Filter new files based on the merge mode
                for diff in new_files:
                    if not self.__check_diff_is_model(diff):
                        new_files.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no new files left
                if len(new_files) == 0 and original_new_files_len > 0:
                    view.update_status("No new model files to merge", "red")
                    logging.info("AppModel", "No new model files to merge, merge canceled")
                    return False
                # Filter deleted files based on the merge mode
                for diff in deleted_files:
                    if not self.__check_diff_is_model(diff):
                        deleted_files.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no deleted files left
                if len(deleted_files) == 0 and original_deleted_files_len > 0:
                    view.update_status("No deleted model files to merge", "red")
                    logging.info("AppModel", "No deleted model files to merge, merge canceled")
                    return False
            
            # Mode 2: Merge Code
            elif merge_mode == 2:
                logging.debug("AppModel", f"Merge mode: {merge_mode} - Merge Code")
                # Filter modified based on the merge mode
                for diff in modified:
                    if not self.__check_diff_is_code(diff):
                        modified.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no modified left
                if len(modified) == 0 and original_modified_len > 0:
                    view.update_status("No code files to merge", "red")
                    logging.info("AppModel", "No code files to merge, merge canceled")
                    return False
                # Filter new files based on the merge mode
                for diff in new_files:
                    if not self.__check_diff_is_code(diff):
                        new_files.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no new files left
                if len(new_files) == 0 and original_new_files_len > 0:
                    view.update_status("No new code files to merge", "red")
                    logging.info("AppModel", "No new code files to merge, merge canceled")
                    return False
                # Filter deleted files based on the merge mode
                for diff in deleted_files:
                    if not self.__check_diff_is_code(diff):
                        deleted_files.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no deleted files left
                if len(deleted_files) == 0 and original_deleted_files_len > 0:
                    view.update_status("No deleted code files to merge", "red")
                    logging.info("AppModel", "No deleted code files to merge, merge canceled")
                    return False
                
            # Mode 3: Merge Test(SCA, MXAM)
            elif merge_mode == 3:
                logging.debug("AppModel", f"Merge mode: {merge_mode} - Merge Test")
                # Filter modified based on the merge mode
                for diff in modified:
                    if not self.__check_diff_is_test(diff):
                        modified.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no modified left
                if len(modified) == 0 and original_modified_len > 0:
                    view.update_status("No test files to merge", "red")
                    logging.info("AppModel", "No test files to merge, merge canceled")
                    return False
                # Filter new files based on the merge mode
                for diff in new_files:
                    if not self.__check_diff_is_test(diff):
                        new_files.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no new files left
                if len(new_files) == 0 and original_new_files_len > 0:
                    view.update_status("No new test files to merge", "red")
                    logging.info("AppModel", "No new test files to merge, merge canceled")
                    return False
                # Filter deleted files based on the merge mode
                for diff in deleted_files:
                    if not self.__check_diff_is_test(diff):
                        deleted_files.remove(diff)
                        logging.debug("AppModel", f"Remove {diff}")
                # Check if there are no deleted files left
                if len(deleted_files) == 0 and original_deleted_files_len > 0:
                    view.update_status("No deleted test files to merge", "red")
                    logging.info("AppModel", "No deleted test files to merge, merge canceled")
                    return False
            
            logging.debug("AppModel", f"Modified files reduced from {original_modified_len} to {len(modified)}")
            # Popup a window to ask user to select all or manually select files
            result = messagebox.askyesno("Confirmation", "Do you want to merge ALL?")
            if result:
                # Copy and replace all files from source to target
                logging.info("AppModel", "Merge all files")
                self.status = "Merging All Files..."
                self.__merge(view, modified, temp_source_folder, temp_target_folder, source_branch, target_branch)
            else:
                # Popup a window to ask user to select files manually
                logging.info("AppModel", "Selecting files manually")
                view.update_status("Selecting Files...", "yellow")
                # self.status = "Selecting Files..."
                logging.info("AppModel", "Selecting Files...")
                selected = []
                # Select new files
                if len(new_files) > 0:
                    selected += view.select_files(new_files, "Select new files")
                    logging.info("AppModel", f'Selected new files: {selected}')
                # Select deleted files
                if len(deleted_files) > 0:
                    selected += view.select_files(deleted_files, "Select deleted files")
                    logging.info("AppModel", f'Selected deleted files: {selected}')
                # Select modified files
                if len(modified) > 0:
                    logging.debug("AppModel", f"Modified files: {len(modified)}")
                    selected += view.select_files(modified, "Select modified files")
                    logging.info("AppModel", f'Selected modified files: {selected}')
                logging.info("AppModel", selected)
                if selected:
                    self.__merge(view, selected, temp_source_folder, temp_target_folder, source_branch, target_branch)
                else:
                    self.status = "Merge Canceled"
                    # Raise exception to drop sandboxes
                    raise Exception("Merge Canceled")
                
            self.status = "Merge Complete"
            logging.info("AppModel", self.status)
            return True
        except Exception as ex:
            logging.error("AppModel", f"Merge Failed: {str(ex)}")
            # Try to release locks and drop sandboxes if merge failed
            try:
                if self.mks_locked_files:
                    self.merge_branch.remove_lock_files(self.mks_locked_files)
                if not temp_source_folder:
                    current_tmp_folder = self.merge_branch.get_current_temp_folder()
                    temp_source_folder = f"{current_tmp_folder}/source"
                self.mks.drop_sandbox(temp_source_folder)
                if not temp_target_folder:
                    current_tmp_folder = self.merge_branch.get_current_temp_folder()
                    temp_target_folder = f"{current_tmp_folder}/target"
                self.mks.drop_sandbox(temp_target_folder)
            except Exception as e:
                logging.error("AppModel", f"Cleanup failed: {str(e)}")
                return False