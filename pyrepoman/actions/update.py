# Standard Library Imports
import os, subprocess, sys, re

# Third Party Imports

# Local Application Imports
from .action import Action

class Update(Action):

    def __init__(self):

        super().__init__()

    @classmethod
    def add_parser(cls, subparser_container):

        parser_update = subparser_container.add_parser('update', help='update all Git repos in your current directory from remote repos')
        parser_update.set_defaults(action='update')
        parser_update.set_defaults(host='')
        return parser_update

    def run(self):

        nonbare_repo_names = super()._get_pwd_local_nonbare_repo_names()
        for nonbare_repo_name in nonbare_repo_names:
            os.chdir(nonbare_repo_name)
            completed_process = subprocess.run(['git',  'pull'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stderr.rstrip()
            completed_process.check_returncode()
            os.chdir("..")
