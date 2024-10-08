import os
import logging
import sys
import shutil
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from mks_utils.mks import MKS
from utils.mks_utils.mks import MKS


class Sandbox:
    
    def __init__(self):
        logging.info('SandboxUtils', 'Init')
        self.mks = MKS()
    
    def create_sandbox(self, project: str, sandbox_folder: str, dev_path: str) -> bool:
        """
        Creates a sandbox environment for a given project.
        Args:
            project (str): The project path. It should end with '/project.pj'.
            sandbox_folder (str): The path to the sandbox folder.
            dev_path (str): The development path. If it contains 'mainline', an empty string is passed to the sandbox creation method.
        Returns:
            bool: True if the sandbox was created successfully, False otherwise.
        Raises:
            Exception: If an unexpected error occurs during sandbox creation.
        Logs:
            Errors and information related to the sandbox creation process.
        """
        try:
            logging.info("SandboxUtils", "Creating Sandbox ...")
            # Check if all arguments are provided
            if not project or not sandbox_folder or not dev_path:
                logging.error("SandboxUtils", "Project, Sandbox folder and Dev path are required")
                return False
            # Check if sandbox folder is exist
            if os.path.exists(sandbox_folder):
                # Delete folder using shutil.rmtree
                shutil.rmtree(sandbox_folder)
            # Create sandbox folder
            os.makedirs(sandbox_folder)
            # Check if project string is end with / or \ and remove it
            if project.endswith("/") or project.endswith("\\"):
                project = project[:-1]
            # Check if project string is end with /project.pj and add it
            if not project.endswith("/project.pj"):
                project += "/project.pj"
            # Create sandbox
            if "mainline" in dev_path.lower():
                response = self.mks.create_sandbox(project, sandbox_folder, "")
            else:
                response = self.mks.create_sandbox(project, sandbox_folder, dev_path)
            if "could not be located" in response.lower():
                logging.error("SandboxUtils", response)
                return False
            else:
                logging.info("SandboxUtils", response)
                return True
        except Exception as e:
            logging.error("SandboxUtils", str(e))
            raise
    
    def drop_sandbox(self, sandbox_folder: str) -> bool:
        """
        Drops the specified sandbox folder and deletes it if the operation is successful.

        Args:
            sandbox_folder (str): The path to the sandbox folder to be dropped.

        Returns:
            bool: True if the sandbox was successfully dropped and deleted, False otherwise.

        Raises:
            Exception: If an unexpected error occurs during the operation.

        Logs:
            - Error if the sandbox folder does not exist or is not a directory.
            - Error if the operation to drop the sandbox fails.
            - Info if the sandbox is successfully dropped.
        """
        try:
            logging.info("SandboxUtils", "Dropping Sandbox ...")
            # Check if sandbox folder is empty
            if not os.path.exists(sandbox_folder):
                logging.error("SandboxUtils", "Sandbox folder is empty")
                return False
            # Check if sandbox folder is exist
            if not os.path.isdir(sandbox_folder):
                logging.error("SandboxUtils", "Sandbox folder is not exist")
                return False
            # Check if sandbox folder string is end with / or \ and remove it
            if sandbox_folder.endswith("/") or sandbox_folder.endswith("\\"):
                sandbox_folder = sandbox_folder[:-1]
            sandbox_folder = f"{sandbox_folder}/project.pj"
            # Drop sandbox
            response = self.mks.drop_sandbox(sandbox_folder)
            if "failed to drop sandbox" in response.lower():
                logging.error("SandboxUtils", response)
                return False
            else:
                logging.info("SandboxUtils", response)
                # Delete folder using shutil.rmtree if exists
                if os.path.exists(sandbox_folder):
                    shutil.rmtree(sandbox_folder)
                return True
        except Exception as e:
            logging.error("SandboxUtils", str(e))
            raise
        

if __name__ == "__main__":
    sandbox = Sandbox()