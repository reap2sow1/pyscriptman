# Standard Library Imports
import os, subprocess, platform, pathlib, sys

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host
from util.printexception import PrintException


class LocalHost(Host):

    HELP_DESC = "can manipulate local directories containing git repos"
    _PATH_CMD_ARG_NAME = "path"

    def __init__(self, configholder):

        super().__init__()
        self.path = configholder.get_config_value("path")

    @classmethod
    def is_host_type(cls, identifier, configholder):

        path = os.path.expanduser(configholder.get_config_value(cls._PATH_VAR_NAME))

        try:
            return identifier == cls.__name__.lower() and pathlib.Path(path).exists()
        except PermissionError as e:
            PrintException.print_permission_denied(e.filename)
            raise

    @classmethod
    def _modify_parser(cls, parser):

        parser.add_argument(cls._PATH_VAR_NAME, help="specifies what directory you wish to target")

        return parser

    def get_user_repo_names_and_locations(self):

        local_path = os.path.expanduser(self.path)
        repos = self._get_pwd_bare_repo_names(local_path)
        for repo in repos:
            self.add_repo_name_and_location(repo, os.path.join(local_path, repo))
        return self.repo_names_and_locations
