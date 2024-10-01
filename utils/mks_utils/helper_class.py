class Project:
    def __init__(self, project_name, repo_location, server, config_path, is_restricted, last_cp, last_cp_date, members, subproject):
        self.shortname = project_name.strip("/project.pj").split(r"/")[-1]
        self.project_name = project_name
        self.repo_location = repo_location
        self.server = server
        self.config_path = config_path
        self.is_restricted = is_restricted
        self.last_cp = last_cp
        self.last_cp_date = last_cp_date
        self.members = members
        self.subproject = subproject

    def __str__(self):
        return f"{self.shortname}"

    def __repr__(self):
        return f"{self.shortname}"

