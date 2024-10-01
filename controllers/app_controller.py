import logging


class AppController:
    def __init__(self, model, view):
        logging.info('AppController', 'Init')
        self.model = model
        self.view = view

        # Set up button commands
        self.view.set_check_pj_button_command(self.check_project)
        self.view.set_check_source_brach_button_command(self.check_source_branch)
        self.view.set_select_source_brach_button_command(self.select_source_branch)
        self.view.set_check_target_brach_button_command(self.check_target_branch)
        self.view.set_merge_button_command(self.merge_branches)

    def check_project(self):
        # Get project name from view
        project_name = self.view.get_project_name()
        self.model.set_project_name(project_name)

        # Check project in the model
        if self.model.check_project():
            self.view.update_status(self.model.get_status(), "green")
        else:
            self.view.update_status(self.model.get_status(), "red")
    
    def check_source_branch(self):
        # Get source branch from view
        source_branch = self.view.get_source_branch()
        status = self.model.set_source_branch(source_branch)

        # Check project in the model
        if status:
            self.view.update_status(self.model.get_status(), "green")
        else:
            self.view.update_status(self.model.get_status(), "red")
    
    def check_target_branch(self):
        # Get target branch from view
        target_branch = self.view.get_target_branch()
        status = self.model.set_target_branch(target_branch)

        # Check project in the model
        if status:
            self.view.update_status(self.model.get_status(), "green")
        else:
            self.view.update_status(self.model.get_status(), "red")
    
    def select_source_branch(self):
        # Read all branches from mks and show them in a list
        branches = self.model.get_dev_paths()
        # Show the branches in a popup window
        source_branch = self.view.select_branch(branches)
        self.model.set_source_branch(source_branch)
        # Fill the source branch input with the selected branch
        self.view.set_source_branch_input(source_branch)

    def merge_branches(self):
        # Get source and target branches from view
        source_branch = self.view.get_source_branch()
        target_branch = self.view.get_target_branch()
        self.model.set_branches(source_branch, target_branch)

        # Merge branches in the model
        if self.model.merge_branches():
            self.view.update_status(self.model.get_status(), "green")
        else:
            self.view.update_status(self.model.get_status(), "red")
