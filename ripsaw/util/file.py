import os
import shutil
from uuid import uuid4


def clone_directory_uuid(source):
    uuid_name = str(uuid4())
    path_top, path_tail = os.path.split(source)
    uuid_destination = os.path.join(path_top, uuid_name)

    shutil.copytree(source, uuid_destination)

    return uuid_destination


def wipe_directory(target):
    shutil.rmtree(target)
