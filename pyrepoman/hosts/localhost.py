# Standard Library Imports
import os
import pathlib
from os.path import expanduser

# Third Party Imports

# Local Application Imports
from pyrepoman.hosts.host import Host
from util.message import Message


class LocalHost(Host):

    HELP_DESC = "can manipulate local directories containing git repos"
    PATH_CMD_ARG_NAME = "path"

    def __init__(self, configholder):

        super().__init__()
        self.path = configholder.get_config_value(self.PATH_CMD_ARG_NAME)

    @classmethod
    def is_host_type(cls, chosen_host, configholder):

        path = configholder.get_config_value(cls.PATH_CMD_ARG_NAME)
        path = "" if path == configholder.NON_EXISTANT_CONFIG else expanduser(path)

        try:
            return (
                chosen_host == cls._get_host_name() and pathlib.Path(path).exists()
            )  # TODO pathlib.Path(path).exists() will have permission issues if directory does not have proper permissions. However, this is only the case of the 'dot' character is used vs the full path
        except PermissionError as e:  # TODO THE 'dot' SYMBOL WILL NOT BE SUPPORTED CURRENTLY
            Message.print_permission_denied(e.filename)
            raise

    @classmethod
    def _modify_parser(cls, parser):

        parser.add_argument(
            cls.PATH_CMD_ARG_NAME, help="specifies what directory you wish to target"
        )

        return parser

    def get_user_repo_names_and_locations(self):

        local_path = os.path.expanduser(self.path)
        try:
            repos = super()._get_bare_repo_names_from_path(local_path)
            for repo in repos:
                super().add_repo_name_and_location(repo, os.path.join(local_path, repo))
            return super().repo_names
        except PermissionError:
            raise
        except FileNotFoundError:
            raise
