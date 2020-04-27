#!/usr/bin/env python3
# Standard Library Imports
from subprocess import CalledProcessError
import sys

# Third Party Imports
from toml import TomlDecodeError

# Local Application Imports
from pyrepoman.generator import Generator
from pyrepoman.cmd import Cmd


def main():

    try:
        configholder = Cmd.retrieve_args()
        action = Generator.generate_action(configholder)
        action.run()
    except (CalledProcessError, FileNotFoundError, PermissionError, SystemExit, TomlDecodeError):
        pass
    # except SystemExit: # TODO TO BE DELETED
    #     pass
    # except FileNotFoundError as e:
    #     print(f"Error: a particular file can not be found, '{e.filename}'")
    # except PermissionError as e:
    #     print(f"Error: a particular file/path was unaccessable, '{e.filename}'")
    # except CalledProcessError as e:
    #     pass
    except Exception as e:
        print("Error: an unknown error occured, please report the following below:")
        print(e)


if __name__ == "__main__":
    main()
