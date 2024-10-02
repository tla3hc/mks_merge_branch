import subprocess
import re
import os
import logging
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mks_exception import *
from helper_class import Project


class MKS:
    def __init__(self, hostname: str = None, port: int = None, user: str = None, password: str = None):
        if hostname and port and user and password:
            logging.info('MKS', f"Connecting to {hostname}:{port}")
            connect = self.connect(hostname=hostname, port = port, user=user, password=password)
            if connect:
                logging.info('MKS', f"Connected to {hostname}:{port}")
            else:
                logging.error('MKS', f"Connection to {hostname}:{port}: FAIL! Please check manually")

        else:
            logging.info('MKS', f"Checking current connection")
            logging.info('MKS', f"Current connection status:")
            logging.info('MKS', f'{self.check_connection()}')
            
    def check_connection (self, hostname:str = None, port:int = None):
        """
        Check connection to MKS server with the provided hostname, port. 
        If not provide the information, the function will return a dict containning all current connections and status 
        example: {'example_hostname:1234': True, 'example_hostname:1234': False}

        Parameters:
            hostname (str): The hostname of the MKS server.
            port (int): The port number of the MKS server.

        Returns:
            bool: True if the connection to the hostname was successful, False otherwise.
            dict: if there is no specific hostname and port provided, all available connection with status will return
            example: {'example_hostname:1234': True, 'example_hostname:1234': False}
        """
        def __handle_server_stt_resp(cmd_response):
            out = {}
            for server in cmd_response.splitlines():
                match = re.search (r"@(.*:\d+)(.*)", server)
                if match and match.group(1):
                    out[match.group(1)] = True
                    if match.group(2) and "(Not connected)" in match.group(2):
                        out[match.group(1)] = False
            return out

        try:
            status = self.run("aa servers")
            status = __handle_server_stt_resp(status)
            if hostname and port:
                target = f"{hostname}:{port}"
                return target in status and status[target]
            else:
                return status
        except Exception as ex:
            logging.error('MKS', f"{ex}")
    
    def connect (self, hostname: str, port: int, user: str, password:str, timeout = 5) -> bool:
        """
        Connect to MKS server with the provided hostname, port, user, and password.

        Parameters:
            hostname (str): The hostname of the MKS server.
            port (int): The port number of the MKS server.
            user (str): The username for authentication.
            password (str): The password for authentication.
            timeout (int): The maximum time allowed for the connection attempt (in seconds). Default = 10s

        Returns:
            bool: True if the connection was successful, False otherwise.
        """

        cmd = f"aa connect --hostname={hostname} --port={port} --user={user} --password={password}"
        try:
            out = self.run(cmd)
            # Check connection status
            stt = self.check_connection(hostname=hostname, port=port)
            return stt
        except Exception as ex:
            logging.error('MKS', f"{ex}")
            return False

    def run(self, cmd:str, timeout:int = 30) -> str:
        """
            Run the specified command with a timeout.

            Parameters:
                command (str): The command to execute.
                timeout (int): accepted timeout
            Returns:
                string: output message will be return if no error.
        """
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            if stderr:
                if ("Invalid option" in stderr.decode('utf-8')) or ("Invalid command" in stderr.decode('utf-8')):
                    # Invalid CLI command or invalid arguments for the command
                    raise CLISyntaxError(errors = stderr.decode('utf-8'))
                else:
                    # CLI other error in runtime
                    return stderr.decode('utf-8')
            return stdout.decode('utf-8')
        except subprocess.TimeoutExpired:
            process.kill()
            raise MKSConnectTimeoutError(timeout = timeout)

    def __gen_CLI_additional_args(self, keyword_arguments: dict) -> str:
        add_args = ""
        if keyword_arguments:
            for key in keyword_arguments:
                add_args = (add_args + f" --{key}") if (keyword_arguments[key] is True) else (add_args + f" --{key}={keyword_arguments[key]}")
        return add_args

    def get_subprojects(self, project_name: str, **kwargs) -> list:
        """
            Retrieve a list of subprojects for a given project.
            
            DEFAULT CLI:    si viewproject --norecurse --project="{project_name}"
            
            Parameters:
                project_name (str): The name of the parent project.
                
                Users can pass additional keyword arguments for this function for additional purpose.
                Use only long keyword (ex: --gui) instead of short keyword (ex: -g)
                If a keyword in CLI has no value, keep it as "True" in this function
                example:  mks.get_subprojects("project_name/project.pj", gui=True) ==> si viewproject --norecurse --project="project_name/project.pj" --gui


            Returns:
                list: A list of Project objects representing the subprojects associated with the specified project.

            Reference: https://mks-ea-prod.in.audi.vwg:7021/r12.4.0.0/en/index.html#page/IntegrityHelp%2Fsi_viewproject.html%23
        """
        subprojects = []
        add_args =  self.__gen_CLI_additional_args(kwargs)
        cmd = f'si viewproject --norecurse --project="{project_name}"'
        cmd += add_args
        mks_responses = self.run(cmd)
        for response in mks_responses.splitlines():
            match = re.search (r"(.*?project.pj)", response)
            # get name
            name = match.group(1).strip() if match and match.group(1) else None
            # get project type
            subproject_name =  project_name.strip('project.pj') + name
            if name:
                subproject = self.get_project_info(subproject_name)
                subprojects.append(subproject)
        return subprojects

    def extract_development_paths(self, mks_responses: str) -> list:
        # Find the section after "Development Paths:" 
        match = re.search(r'Development Paths:(.*?)(?=\n\S|$)', mks_responses, re.DOTALL)
        
        if match:
            # Extract lines starting with a tab
            paths_section = match.group(1)
            dev_paths = re.findall(r'^\s+(.*?)(?=\s|$)', paths_section, re.MULTILINE)
            return dev_paths
        else:
            return []

    def get_project_info(self, project_name: str, **kwargs) -> Project:
        """
            Retrieve detailed information of a given project.
            
            DEFAULT CLI:    si projectinfo --project="{project_name}"
            
            Parameters:
                project_name (str): The name of the parent project.
                
                Users can pass additional keyword arguments for this function for additional purpose.
                Use only long keyword (ex: --gui) instead of short keyword (ex: -g)
                If a keyword in CLI has no value, keep it as "True" in this function
                example:  mks.get_project_info("project_name/project.pj", gui=True) ==> si projectinfo --project="project_name/project.pj" --gui


            Returns:

            Reference: https://mks-ea-prod.in.audi.vwg:7021/r12.4.0.0/en/index.html#page/IntegrityHelp%2Fsi_projectinfo.html%23
        """
        add_args =  self.__gen_CLI_additional_args(kwargs)
        cmd = f'si projectinfo --project="{project_name}"'
        cmd += add_args
        mks_responses = self.run(cmd)
        if "could not be located on the server" not in mks_responses:

            project_name = re.search (r"Project Name:\s*(.*)", mks_responses).group(1).strip()
            repo_location = re.search (r"Repository Location:\s*(.*)", mks_responses).group(1).strip()
            server = re.search (r"Server:\s*(.*)", mks_responses).group(1).strip()
            config_path = re.search (r"Configuration Path:\s*(.*)", mks_responses).group(1).strip()
            is_restricted = re.search (r"Restricted:\s*(.*)", mks_responses).group(1).strip() == 'true'
            last_cp = re.search (r"Last Checkpoint:\s*(.*)", mks_responses).group(1).strip()
            last_cp_date = re.search (r"Last Checkpoint Date:\s*(.*)", mks_responses).group(1).strip()
            members = re.search (r"Members:\s*(.*)", mks_responses).group(1).strip()
            subproject = re.search (r"Subprojects:\s*(.*)", mks_responses).group(1).strip()
            dev_paths = self.extract_development_paths(mks_responses)
            return Project( project_name = project_name,
                            repo_location = repo_location,
                            server = server,
                            config_path = config_path,
                            is_restricted = is_restricted,
                            last_cp = last_cp,
                            last_cp_date = last_cp_date,
                            members = members,
                            subproject = subproject,
                            dev_paths = dev_paths)
        else:
            raise  ProjectNotFoundError(errors=mks_responses)


    def lock_member(self, member: str) -> tuple:
        """
            Lock a member
            
            DEFAULT CLI:    si lock --cpid=:none --lockType=auto member
            
            Parameters:
                member: path path of member in your local sandbox

            Returns:
                Locked version (str) if locking is successful
                None if locking is failed

            Example: mks.lock_member("C:/My Sandboxes/path/to/member.zip")

            Reference: https://mks-ea-prod.in.audi.vwg:7021/r12.4.0.0/en/index.html#page/IntegrityHelp%2Fsi_lock.html%23
        """
        cmd = f'si lock --cpid=:none --lockType=auto "{member}"'
        mks_responses = self.run(cmd)
        match = re.search(r":\s*(locked revision \d+\.\d+)", mks_responses)
        lock_version = match.group(1) if match else None
        return mks_responses, lock_version
    
    def unlock_member(self, member: str) -> str:
        """
        Unlocks a specified member in the MKS (PTC Integrity) system.

        This method constructs and runs a command to unlock a member, 
        removing the lock if it exists. It then parses the command's 
        response to extract the locked revision version, if any.

        Args:
            member (str): The path or identifier of the member to unlock.

        Returns:
            str: The locked revision version if found, otherwise None.
        """
        cmd = f'si unlock --action=remove -forceConfirm=yes "{member}"'
        mks_responses = self.run(cmd)
        return mks_responses

    def resynchronize(self, member: str) -> str:
        """
            Lock a member
            
            DEFAULT CLI:    si resync <member or project>
            Parameters:
                member: path path of member or project (folder) in your local sandbox that you want to resync
                if member is set as a subfoder, all members in the subfoder will be resynchronized

            Returns:
                CLI response

            Example: mks.resynchronize("C:/My Sandboxes/path/to/member.zip") or mks.resynchronize("C:/My Sandboxes/path/to/project.pj")

            Reference: https://mks-ea-prod.in.audi.vwg:7021/r12.4.0.0/en/index.html#page/IntegrityHelp%2Fsi_resync.html%23
        """
        cmd = f'si resync "{member}"'
        mks_responses = self.run(cmd)
        return mks_responses
    
    def create_sandbox(self, project: str, sandbox_folder: str, dev_path: str) -> str:
        """
            Create a sandbox
            
            DEFAULT CLI:    si createsandbox --project="{project}" --sandbox="{sandbox}"
            Parameters:
                project: path of the project that you want to create sandbox
                sandbox: path of the sandbox that you want to create

            Returns:
                CLI response

            Example: mks.create_sandbox("C:/My Sandboxes/path/to/project.pj", "C:/My Sandboxes/path/to/sandbox")

            Reference: https://mks-ea-prod.in.audi.vwg:7021/r12.4.0.0/en/index.html#page/IntegrityHelp%2Fsi_createsandbox.html%23
        """
        # get current directory
        current_dir = os.getcwd()
        # cd to sandbox_folderp
        os.chdir(sandbox_folder)
        
        if len(dev_path) > 0:
            cmd = f'si createsandbox -R --project="{project}" --devpath="{dev_path}"'
        else:
            cmd = f'si createsandbox -R --project="{project}"'
        mks_responses = self.run(cmd)
        
        # cd back to current directory
        os.chdir(current_dir)
        return mks_responses
    
    def make_sandbox_writable(self, sandbox_folder: str) -> str:
        """
        Makes the specified sandbox folder writable by executing the appropriate command.
        Args:
            sandbox_folder (str): The path to the sandbox folder that needs to be made writable.
        Returns:
            str: The response from the command execution.
        Raises:
            ValueError: If the specified sandbox folder does not exist.
        """
        sandbox_folder = os.path.abspath(sandbox_folder)
        # Validate sandbox folder
        if not os.path.exists(sandbox_folder):
            raise (f"Sandbox folder {sandbox_folder} does not exist")
        # get current directory
        current_dir = os.getcwd()
        # cd to sandbox_folderp
        os.chdir(sandbox_folder)
        
        # Check if the sandbox string is end with / or \ and remove it
        if sandbox_folder.endswith("/") or sandbox_folder.endswith("\\"):
            sandbox_folder = sandbox_folder[:-1]
        
        sandbox_folder = f"{sandbox_folder}/project.pj"
        
        cmd = f'si makewritable -R --sandbox="{sandbox_folder}"'
        mks_responses = self.run(cmd)
        
        # cd back to current directory
        os.chdir(current_dir)
        return mks_responses

    def drop_sandbox(self, sandbox_folder: str) -> str:
        """_summary_
        Drop a sandbox
        Args:
            sandbox_folder (str): _description_

        Returns:
            str: _description_
        """
        sandbox_folder = os.path.abspath(sandbox_folder)
        # Validate sandbox folder
        if not os.path.exists(sandbox_folder):
            raise (f"Sandbox folder {sandbox_folder} does not exist")
        # get current directory
        current_dir = os.getcwd()
        # cd to sandbox_folderp
        os.chdir(sandbox_folder)
         # Check if the sandbox string is end with / or \ and remove it
        if sandbox_folder.endswith("/") or sandbox_folder.endswith("\\"):
            sandbox_folder = sandbox_folder[:-1]
        
        sandbox_folder = f"{sandbox_folder}/project.pj"
        cmd = f'si dropsandbox -f --delete=all --forceConfirm=yes "{sandbox_folder}"'
        
        mks_responses = self.run(cmd)
        
        # cd back to current directory
        os.chdir(current_dir)
        return mks_responses
        
        
    def create_sca_sandbox_batch_mode(self, project_name: str, target_folder: str, sub_module_list: list, dev_path_list: list) -> str:
        """
            Create a sandbox in batch mode
            
            DEFAULT CLI:    si createsandbox --project="{project}" --sandbox="{sandbox}"
            Parameters:
                project: path of the project that you want to create sandbox
                sandbox: path of the sandbox that you want to create

            Returns:
                CLI response

            Example: mks.create_sandbox("C:/My Sandboxes/path/to/project.pj", "C:/My Sandboxes/path/to/sandbox")

            Reference: https://mks-ea-prod.in.audi.vwg:7021/r12.4.0.0/en/index.html#page/IntegrityHelp%2Fsi_createsandbox.html%23
        """
        mks_project ='/SWC_{}/01_PROD/30_CG/{}/30_T/40_SCA/project.pj'
        for dev_path in dev_path_list:
            for sub_module in sub_module_list:
                project = mks_project.format(project_name, sub_module)
                sandbox_path = f"{target_folder}/{project_name}/{dev_path}/{sub_module}"
                # Check if the sandbox folder exists
                if not os.path.exists(sandbox_path):
                    logging.info('MKS', f"Creating sandbox at {sandbox_path}")
                    os.makedirs(sandbox_path)
                else:
                    logging.warning('MKS', f"{sandbox_path} already exists")
                    
                self.create_sandbox(project, sandbox_path, dev_path)


if __name__ == "__main__":
    # import sys
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    # from log.logger import Logger
    # logger = Logger()
    # mks = MKS(hostname="mks-ea-prod.in.audi.vwg", port = 7023, user="a0d9lk4", password="Rio@1094#300420") #b=1.14
    mks = MKS() 
    # b = mks.get_project_info("#/Powertrain_Functions_PreDev#PTDrvEng_LdCyc/01_PROD/04_TSI_PTDrvEng_LdCyc/10_FE_PTDrvEng_LdCyc/01_PROD/03_FMD/04_FMS#b=PTDrvEng_LdCyc_4.1.0")
    # b = mks.lock_member("C:/My Sandboxes/40_AutomationTool/HCP1_AutomationTool.zip")
    # b = mks.get_project_info(r"/Spielwiese/ITK_HCP1/00_Fortschrittsberichte/project.pj")
    # a = mks.run(r'si memberinfo "C:\My Sandboxes\20_Fahrbarkeit\PTDrvAxl_FilCord\07_SWMSWAT\04_SWMTS\PTDrvAxl_FilCord_TA.rml"')