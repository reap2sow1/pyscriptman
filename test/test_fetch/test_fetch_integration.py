# Standard Library Imports
import subprocess, os, filecmp, sys, shutil

# Third Party Imports
import pytest

# Local Application Imports
from util.diff import Diff
from pyrepoman.hosts.webhosts.github import GitHub
from test.conftest import (
    localhost_clone_repo,
    remotehost_clone_repo,
    github_clone_repo,
    localhost_setup,
    remotehost_setup,
    github_setup,
)
from test.test_fetch.conftest import (
    configholder,
    ACTION_IDENTIFIER,
    FETCH_TARGET,
    MODEL_TARGET,
)
from test.test_variables import PYREPOMAN_MAIN_PATH


class TestFetchIntegration:
    @pytest.mark.parametrize(
        "localhost_setup",
        [(localhost_clone_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_fetch_localhost(self, localhost_setup):
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "localhost",
                configholder.get_config_value("LOCAL_BARE_REPOS_DIR_PATH"),
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "remotehost_setup",
        [(remotehost_clone_repo, configholder, MODEL_TARGET)],
        indirect=True,
    )
    def test_fetch_remotehost(self, remotehost_setup):
        target = f"{configholder.get_config_value('REMOTE_USER')}@{configholder.get_config_value('REMOTE_ADDR')}"
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "remotehost",
                target,
                "--target-path",
                configholder.get_config_value("REMOTE_BARE_REPOS_DIR_PATH"),
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "github_setup",
        [
            (
                GitHub.OWN_CMD_ARG_NAME,
                "all",
                github_clone_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OWN_CMD_ARG_NAME,
                "public",
                github_clone_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OWN_CMD_ARG_NAME,
                "private",
                github_clone_repo,
                configholder,
                MODEL_TARGET,
            ),
        ],
        indirect=True,
    )
    def test_fetch_github_own(self, github_setup):
        data = github_setup
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "github",
                repo_owner_type,
                "--repo-type",
                repo_type,
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False

    @pytest.mark.parametrize(
        "github_setup",
        [
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "all",
                github_clone_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "owner",
                github_clone_repo,
                configholder,
                MODEL_TARGET,
            ),
            (
                GitHub.OTHER_CMD_ARG_NAME,
                "member",
                github_clone_repo,
                configholder,
                MODEL_TARGET,
            ),
        ],
        indirect=True,
    )
    def test_fetch_github_other(self, github_setup):
        data = github_setup
        username = configholder.get_config_value("GITHUB_NAME")
        repo_owner_type, repo_type = data[0], data[1]
        os.chdir(FETCH_TARGET)
        subprocess.run(
            [
                sys.executable,
                PYREPOMAN_MAIN_PATH,
                ACTION_IDENTIFIER,
                "github",
                repo_owner_type,
                username,
                "--repo-type",
                repo_type,
            ]
        )
        os.chdir("..")
        dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
        diff = Diff(dcmp)
        assert diff.run() == False
