from pathlib import Path
from bagels.locations import data_directory, database_file
from bagels.managers.remotedb import (
    create_client,
    download_files,
    upload_files,
    override_file,
)
from typing import Union


def push_local_database():
    client = create_client()

    if client is None:
        return

    upload_list: list[Union[str, tuple[str, str]]] = ["db.db"]
    local_base_dir = data_directory()

    res_upload = upload_files(
        client=client.client,
        SPACE_NAME=client.SPACE_NAME,
        upload_list=upload_list,
        local_base_dir=local_base_dir,
    )
    return res_upload


def pull_remote_database():
    client = create_client()

    if client is None:
        return

    download_list: list[Union[str, tuple[str, str]]] = ["db.db"]
    download_dir = Path("remote/Downloads")
    down_res = download_files(
        client=client.client,
        SPACE_NAME=client.SPACE_NAME,
        download_list=download_list,
        download_dir=download_dir,
    )

    override_file(source=download_dir / "db.db", dest=database_file())

    return down_res
