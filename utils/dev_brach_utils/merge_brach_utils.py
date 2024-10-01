import os
import logging
import sys
from utils.dev_brach_utils.sandbox_utils import Sandbox
import time

class MergeBrach:
    _m_temp_folder = "./.tmp"
    
    def __init__(self):
        logging.info('MergeBrach', 'Init')
        self.sandbox = Sandbox()
    
    def merge_branches(self, project: str, source_branch: str, target_branch: str) -> bool:
        try:
            # Check if all arguments are provided
            if not project or not source_branch or not target_branch:
                logging.error("MergeBrach", "Project, Source Branch and Target Branch are required")
                return False
            # Create temporary sandbox folder
            source_sandbox_folder = f"{self._m_temp_folder}/source"
            target_sandbox_folder = f"{self._m_temp_folder}/target"
            # Create sandboxes
            status = self.sandbox.create_sandbox(project, source_sandbox_folder, source_branch)
            if not status:
                return False
            status = self.sandbox.create_sandbox(project, target_sandbox_folder, target_branch)
            if not status:
                return False
            # Merge branches
            # wait for 30s
            time.sleep(30)
            
            # Drop sandboxes
            status = self.sandbox.drop_sandbox(source_sandbox_folder)
            if not status:
                return False
            status = self.sandbox.drop_sandbox(target_sandbox_folder)
            if not status:
                return False
            return True
        except Exception as e:
            logging.error("MergeBrach", str(e))
            raise