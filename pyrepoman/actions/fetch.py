# Standard Library Imports
import subprocess, os

# Third Party Imports

# Local Application Imports
from .action import Action

class Fetch(Action):

    def __init__(self, host):

        super().__init__()
        self.host = host

    def run(self):

        repo_names_and_locations = self.host.get_repo_names_and_locations()
        for repo_name in repo_names_and_locations:
            completed_process = subprocess.run(['git', 'clone', f"{self.host.get_location_from_repo_name(repo_name)}", f"{repo_name}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
            completed_process.check_returncode()
