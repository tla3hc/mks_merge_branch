from utils.mks_utils.mks import MKS
import logging
from utils.dev_brach_utils.merge_brach_utils import MergeBrach
from tkinter import messagebox

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
    
    def get_project_info(self, project_name):
        try:
            self.project = self.mks.get_project_info(project_name)
            # add "Mainline" to the list of dev paths
            if self.project:
                self.project.dev_paths.append("Mainline")
        except Exception as e:
            logging.error("AppModel", str(e))
            raise

    def set_project_name(self, project_name):
        # Check if project name end with / or \ and remove it
        if project_name.endswith("/") or project_name.endswith("\\"):
            project_name = project_name[:-1]
        # Check if the project name contain /project.pj at the end, if not add it
        if not project_name.endswith("/project.pj"):
            project_name += "/project.pj"
        self.project_name = project_name
    
    def check_branch(self, branch: str) -> bool:
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
        # Check if the source branch is valid
        if not self.check_branch(source):
            return False
        self.source_branch = source
        self.status = "Valid Source Branch"
        return True

    def set_target_branch(self, target: str) -> bool:
        # Check if the target branch is valid
        if not self.check_branch(target):
            return False
        self.target_branch = target
        self.status = "Valid Target Branch"
        return True
        
    def check_project(self):
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
        return True

    def get_dev_paths(self):
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
    
    def merge_branches(self, view, model, project_name: str, source_branch: str, target_branch: str) -> bool:
        view.update_status("Merging...", "yellow")
        if not project_name or not self.source_branch or not self.target_branch:
            self.status = "All inputs Required"
            logging.info("AppModel", self.status)
            return False
        # Check if the project name is different from the current project name
        if project_name != self.project_name:
            # Get the project info
            try:
                view.update_status("Checking Project...", "yellow")
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
        status, temp_folder = self.merge_branch.create_tmp_sandboxes(project_name, source_branch, target_branch)
        if not status:
            self.status = "Merge Failed"
            return False
        temp_source_folder = f"{temp_folder}/source"
        temp_target_folder = f"{temp_folder}/target"
        # Compare the source and target folders
        view.update_status("Comparing Folders...", "yellow")
        differences = self.merge_branch.compare_folders(temp_target_folder, temp_source_folder)
        # Popup a window to ask user to select all or manually select files
        result = messagebox.askyesno("Confirmation", "Do you want to merge ALL?")
        if result:
            # Copy and replace all files from source to target
            logging.info("AppModel", "Copying files")
            view.update_status("Copying Files...", "yellow")
        else:
            # Popup a window to ask user to select files manually
            logging.info("AppModel", "Selecting files manually")
            view.update_status("Selecting Files...", "yellow")
            selected = view.select_files(differences)
            logging.info("AppModel", selected)
            # Make sandbox writable
            view.update_status("Making Sandboxes Writable...", "yellow")
            self.mks.make_sandbox_writable(temp_source_folder)
            self.mks.make_sandbox_writable(temp_target_folder)
            # Copy selected files from source to target
            view.update_status("Copying Selected Files...", "yellow")
            self.merge_branch.merge_folder(temp_source_folder, temp_target_folder, selected)
            # Lock files
            # Checkin files
            # Release locks
            # Drop sandboxes
            view.update_status("Dropping Sandboxes...", "yellow")
            
        self.status = "Merge Complete"
        return True
