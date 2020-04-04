# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from .action import Action

class Backup(Action):

    def __init__(self, host, configholder):

        super().__init__()
        self.host = host
        self.dest = configholder.get_config_value('dest')

    @classmethod
    def add_parser(cls, subparser_container):

        subcommand = cls.__name__.lower()
        backup = subparser_container.add_parser(subcommand, help='backup all Git repos, done by mirroring repos fully', allow_abbrev=False)
        backup.add_argument('dest', help='where to store backups (destination)')
        backup.set_defaults(action=subcommand)
        return backup

    def run(self):

        repo_names_and_locations = self.host.get_user_repo_names_and_locations()
        dest = self.dest
        super()._create_dir(dest)
        not_delete = list()
        backup_content = os.listdir(dest)
        for repo_name in repo_names_and_locations:
            backup_repo_location = os.path.join(dest, repo_name)
            if(not repo_name in backup_content):
                super()._create_mirror(self.host.get_location_from_repo_name(repo_name), backup_repo_location)
            not_delete.append(repo_name)
        super()._remove_all_dir_content(dest, not_delete)
