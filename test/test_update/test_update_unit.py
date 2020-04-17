# Standard Library Imports
import subprocess, sys, os, platform, stat

# Third Party Imports
import pytest

# Local Application Imports
from pyrepoman.actions.update import (
    Update
)
from test.test_update.conftest import (
    pytest_runtest_setup,
    pytest_runtest_teardown,
    UPDATE_TARGET
)
from test.test_variables import (
    PYREPOMAN_MAIN_PATH,
)
from test.helpers import(
    change_target_filemode_recursive
)

NO_PERMISSIONS = 0

class TestUpdate:
    def test_permission_error(self):

        filemode_binary = os.stat(UPDATE_TARGET).st_mode
        if(platform.system().lower() != 'linux'):
            change_target_filemode_recursive(UPDATE_TARGET, stat.S_IREAD)
        else:
            change_target_filemode_recursive(UPDATE_TARGET, NO_PERMISSIONS)

        with pytest.raises(PermissionError):
            update = Update()
            update.run()

        change_target_filemode_recursive(UPDATE_TARGET, filemode_binary)
