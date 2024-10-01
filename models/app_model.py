from utils.mks_utils.mks import MKS


class AppModel:
    def __init__(self):
        self.project_name = ""
        self.source_branch = ""
        self.target_branch = ""
        self.status = "Idle"
        self.mks = MKS()
        self.project = None
    
    def get_project_info(self, project_name):
        try:
            self.project = self.mks.get_project_info(project_name)
        except Exception as e:
            raise

    def set_project_name(self, project_name):
        # Check if the project name contain /project.pj at the end, if not add it
        if not project_name.endswith("/project.pj"):
            project_name += "/project.pj"
        self.project_name = project_name
    
    def check_branch(self, branch: str) -> bool:
        if not branch:
            self.status = "Branch(es) Required"
            return False
        # Check the source branch in MKS
        if self.project:
            if branch in self.project.branches:
                self.status = "Checked"
                return True
        else:
            if self.project_name:
                try:
                    self.get_project_info(self.project_name)
                    if branch in self.project.branches:
                        self.status = "Checked"
                        return True
                except Exception as e:
                    self.status = str(e)
                    return False
            else:
                self.status = "Project Required"
                return False
        self.status = "Branch Not Found"
        return False

    def set_branches(self, source: str, target: str) -> bool:
        # Check if the source and target branches are valid
        if not self.check_branch(source) or not self.check_branch(target):
            return False
        self.source_branch = source
        self.target_branch = target
        return True
    
    def set_source_branch(self, source: str) -> bool:
        # Check if the source branch is valid
        if not self.check_branch(source):
            return False
        self.source_branch = source
        return True

    def set_target_branch(self, target: str) -> bool:
        # Check if the target branch is valid
        if not self.check_branch(target):
            return False
        self.target_branch = target
        return True
        
    def check_project(self):
        if not self.project_name:
            self.status = "Project Required"
            return False
        # Check the project in MKS
        try:
            self.project = self.mks.get_project_info(self.project_name)
        except Exception as e:
            self.status = str(e)
            return False
        self.status = "Checked"
        return True

    def merge_branches(self):
        if not self.source_branch or not self.target_branch:
            self.status = "Branches Required"
            return False
        self.status = "Merge Complete"
        return True

    def get_status(self):
        return self.status
