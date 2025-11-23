from typing import Union
from mypy_boto3_s3 import S3Client
from pathlib import Path


def list_files(client: S3Client, SPACE_NAME: str):
    response = client.list_objects_v2(Bucket=SPACE_NAME)
    # print(type(response))
    # print(type(response.get('Contents')))
    list_file_name = []
    for obj in response.get("Contents", []):
        # print(obj.get('Key',''))
        res_temp = obj.get("Key", "")
        if res_temp != "":
            # list_file_name.append(res_temp)
            list_file_name.append(obj)

        # print(obj.keys())
        # print(obj)

    return list_file_name


def key_only(arr: list) -> list[str]:
    return [obj["Key"] for obj in arr if obj.get("Key")]


def download_files(
    client: S3Client,
    SPACE_NAME: str,
    download_list: list[Union[str, tuple[str, str]]],
    download_dir: str = "Downloads",
):
    remote_name = local_name = None

    Path(download_dir).mkdir(parents=True, exist_ok=True)

    results = {"success": [], "failed": []}

    for item in download_list:
        try:
            # in case if we want to differentiate the local and remote name
            if isinstance(item, tuple):
                remote_name, local_name = item
            else:
                remote_name = local_name = item

            local_dir = Path(download_dir) / local_name

            client.download_file(
                Bucket=SPACE_NAME, Key=remote_name, Filename=str(local_dir)
            )

            if not local_dir.exists() or local_dir.stat().st_size == 0:
                raise ValueError(f"Downloaded file is invalid: {local_dir}")

            results["success"].append({"remote": remote_name, "local_name": local_name})

        except Exception as e:
            results["failed"].append(
                {
                    "remote": remote_name,
                    "error": str(e),
                }
            )

    return results


def upload_files(
    client: S3Client,
    SPACE_NAME: str,
    upload_list: list[Union[str, tuple[str, str]]] = None,
    local_base_dir: str = "Downloads",
):
    results = {"success": [], "failed": []}
    upload_path = Path(local_base_dir)

    if upload_list is None:
        if not upload_path:
            results["failed"].append(f"There is no {local_base_dir} or {upload_path}")
            return results

        upload_list = [
            str(f.relative_to(upload_path))
            for f in upload_path.rglob("*")
            if f.is_file()
        ]

    if len(upload_list) == 0:
        results["failed"].append(
            f"There is no file under {local_base_dir} or {upload_path}"
        )
        return results

    for item in upload_list:
        remote_name = local_name = None
        try:
            if isinstance(item, tuple):
                remote_name, local_name = item
            else:
                remote_name = local_name = item

            local_path = upload_path / local_name

            if not local_path.exists():
                raise FileNotFoundError(f"File not found : {local_path}")

            client.upload_file(
                Filename=str(local_path), Bucket=SPACE_NAME, Key=remote_name
            )

            results["success"].append(
                {
                    "local": local_name,
                    "remote": remote_name,
                }
            )
        except Exception as e:
            results["failed"].append(
                {"local": local_name or str(item), "error": str(e)}
            )

    return results
