class AppModel:
    def __init__(self):
        self.project_name = ""
        self.source_branch = ""
        self.target_branch = ""
        self.status = "Idle"

    def set_project_name(self, project_name):
        self.project_name = project_name

    def set_branches(self, source, target):
        self.source_branch = source
        self.target_branch = target

    def check_project(self):
        if not self.project_name:
            self.status = "Project Name Required"
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
