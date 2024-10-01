import os
import logging
import sys
import shutil
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from mks_utils.mks import MKS
from utils.mks_utils.mks import MKS


class Sandbox:
    
    def __init__(self):
        logging.info('Sandbox', 'Init')
        self.mks = MKS()
    
    def create_sandbox(self, project: str, sandbox_folder: str, dev_path: str) -> bool:
        try:
            # Check if all arguments are provided
            if not project or not sandbox_folder or not dev_path:
                logging.error("Sandbox", "Project, Sandbox folder and Dev path are required")
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
                project = f"{project}#n="
                response = self.mks.create_sandbox(project, sandbox_folder, "")
            else:
                response = self.mks.create_sandbox(project, sandbox_folder, dev_path)
            
            if "could not be located" in response.lower():
                logging.error("Sandbox", response)
                return False
            else:
                logging.info("Sandbox", response)
                return True
            
        except Exception as e:
            logging.error("Sandbox", str(e))
            raise
    
    def drop_sandbox(self, sandbox_folder: str) -> bool:
        try:
            # Check if sandbox folder is empty
            if not os.path.exists(sandbox_folder):
                logging.error("Sandbox", "Sandbox folder is empty")
                return False
            # Check if sandbox folder is exist
            if not os.path.isdir(sandbox_folder):
                logging.error("Sandbox", "Sandbox folder is not exist")
                return False
            # Check if sandbox folder string is end with / or \ and remove it
            if sandbox_folder.endswith("/") or sandbox_folder.endswith("\\"):
                sandbox_folder = sandbox_folder[:-1]
            sandbox_folder = f"{sandbox_folder}/project.pj"
            # Drop sandbox
            response = self.mks.drop_sandbox(sandbox_folder)
            if "failed to drop sandbox" in response.lower():
                logging.error("Sandbox", response)
                return False
            else:
                logging.info("Sandbox", response)
                # Delete folder using shutil.rmtree if exists
                if os.path.exists(sandbox_folder):
                    shutil.rmtree(sandbox_folder)
                return True
        except Exception as e:
            logging.error("Sandbox", str(e))
            raise
        

if __name__ == "__main__":
    sandbox = Sandbox()
    # sandbox.mks.get_sandbox_info("sandbox")
    #n=