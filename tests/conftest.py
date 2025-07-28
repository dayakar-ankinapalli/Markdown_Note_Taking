import pytest
import os
import shutil
from project import create_app

@pytest.fixture(scope='module')
def test_client():
    """Create and configure a new app instance for each test module."""
    app = create_app('project.config.TestingConfig')
    testing_client = app.test_client()

    # Establish an application context
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens

    ctx.pop()

@pytest.fixture(scope='module')
def init_test_notes_dir():
    """Create and clean up the test notes directory for the test module."""
    from project.config import TestingConfig
    test_dir = TestingConfig.NOTES_DIR

    os.makedirs(test_dir, exist_ok=True)

    yield test_dir  # provide the path to the tests

    shutil.rmtree(test_dir)