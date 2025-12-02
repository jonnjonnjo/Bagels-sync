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
    try:
        client = create_client()

        if client is None:
            return {
                "Success": False,
                "error": "Failed to create remote client. Please check the credentials.",
            }
        db_path = database_file()

        if not db_path.exists():
            return {"Success": False, "error": "Local database file not found."}

        upload_list: list[Union[str, tuple[str, str]]] = ["db.db"]
        local_base_dir = data_directory()

        res_upload = upload_files(
            client=client.client,
            SPACE_NAME=client.SPACE_NAME,
            upload_list=upload_list,
            local_base_dir=local_base_dir,
        )

        if res_upload["failed"]:
            return {
                "success": False,
                "error": f"Upload failed: {res_upload['failed'][0].get('error', 'Unknown error')}",
            }

        return {"success": True, "message": "Database uploaded successfully"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error during push: {str(e)}"}


def pull_remote_database():
    """Pull remote database and replace local one."""
    try:
        client = create_client()

        if client is None:
            return {
                "success": False,
                "error": "Failed to create remote client. Check credentials.",
            }

        download_list: list[Union[str, tuple[str, str]]] = ["db.db"]
        download_dir = Path("remote/Downloads")

        download_dir.mkdir(parents=True, exist_ok=True)

        down_res = download_files(
            client=client.client,
            SPACE_NAME=client.SPACE_NAME,
            download_list=download_list,
            download_dir=download_dir,
        )

        if down_res["failed"]:
            return {
                "success": False,
                "error": f"Download failed: {down_res['failed'][0].get('error', 'Unknown error')}",
            }

        # Verify downloaded file exists and is valid
        downloaded_file = download_dir / "db.db"
        if not downloaded_file.exists():
            return {"success": False, "error": "Downloaded file not found"}

        if downloaded_file.stat().st_size == 0:
            return {"success": False, "error": "Downloaded file is empty"}

        backup_path = database_file().with_suffix(".db.backup")
        try:
            if database_file().exists():
                import shutil

                shutil.copy2(database_file(), backup_path)
        except Exception as e:
            return {"success": False, "error": f"Failed to create backup: {str(e)}"}

        try:
            override_file(source=downloaded_file, dest=database_file())
        except Exception as e:
            # Restore backup if override fails
            if backup_path.exists():
                import shutil

                shutil.copy2(backup_path, database_file())
            return {"success": False, "error": f"Failed to override database: {str(e)}"}

        if backup_path.exists():
            backup_path.unlink()

        return {
            "success": True,
            "message": "Database downloaded successfully",
            "backup_created": True,
        }

    except Exception as e:
        return {"success": False, "error": f"Unexpected error during pull: {str(e)}"}


# def push_local_database():
#     client = create_client()
#
#     if client is None:
#         return
#
#     upload_list: list[Union[str, tuple[str, str]]] = ["db.db"]
#     local_base_dir = data_directory()
#
#     res_upload = upload_files(
#         client=client.client,
#         SPACE_NAME=client.SPACE_NAME,
#         upload_list=upload_list,
#         local_base_dir=local_base_dir,
#     )
#     return res_upload
#


# def pull_remote_database():
#     client = create_client()
#
#     if client is None:
#         return
#
#     download_list: list[Union[str, tuple[str, str]]] = ["db.db"]
#     download_dir = Path("remote/Downloads")
#     down_res = download_files(
#         client=client.client,
#         SPACE_NAME=client.SPACE_NAME,
#         download_list=download_list,
#         download_dir=download_dir,
#     )
#
#     override_file(source=download_dir / "db.db", dest=database_file())
#
#     return down_res
