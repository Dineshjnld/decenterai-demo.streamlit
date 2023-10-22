import os
import shutil

import pytest

# assume your zip_folder function is in a module named "your_module"
from .archive import archive_directory


@pytest.fixture()
def create_test_directory():
    test_directory = 'test_dir'
    if not os.path.exists(test_directory):
        os.makedirs(test_directory)

    with open('test_dir/test_file.txt', 'w') as file:
        file.write('Hello, World!')

    yield test_directory

    # Teardown after test
    shutil.rmtree(test_directory)
    os.remove('archive.zip')


def test_zip_folder(create_test_directory):
    archive_name = 'archive'
    archive_directory(archive_name, create_test_directory)

    # Verify that the archive file is created
    assert os.path.isfile(f'{archive_name}.zip')
