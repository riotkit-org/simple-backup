import os
import json
import re
import time
import subprocess
from logging import info
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import List
import boto3
import botocore.client


from .config import from_dict_or_env


@dataclass
class File:
    name: str
    last_modified: datetime


class Filesystem(ABC):
    def list_files(self) -> List[File]:
        return []

    def upload(self, local_path: str, remote_name: str = ''):
        pass

    def delete(self, remote_name: str):
        pass


class Dummy(Filesystem):
    local_list: List[File]

    def __init__(self):
        self.local_list = []

    def list_files(self) -> List[File]:
        return self.local_list

    def upload(self, local_path: str, remote_name: str = ''):
        self.local_list.append(File(remote_name, datetime.now()))

    def delete(self, remote_name: str):
        self.local_list = list(
            filter(lambda x: x.name != remote_name, self.local_list)
        )


class Local(Filesystem):
    """
    Local filesystem as a "remote" destination
    """

    base_dir: str

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    def list_files(self) -> List[File]:
        results = []

        for f in os.scandir(self.base_dir):
            if f.is_file():
                results.append(
                    File(f.name, datetime.fromtimestamp(
                        os.path.getmtime(self.base_dir + "/" + f.name)))
                )

        return results

    def upload(self, local_path: str, remote_name: str = ''):
        subprocess.check_call(['cp', local_path, self.base_dir + "/" + remote_name])

    def delete(self, remote_name: str):
        os.unlink(self.base_dir + "/" + remote_name)


class S3(Filesystem):
    """
    S3 using AWS SDK/Boto3
    """

    client: botocore.client.BaseClient
    resource: None
    base_dir: str
    bucket_name: str

    def __init__(self, endpoint_url: str, access_key_id: str, secret_access_key: str, 
                 bucket_name: str, base_dir: str, retries: int = 30):

        self.base_dir = base_dir.strip(" /")
        session = boto3.session.Session(aws_access_key_id=access_key_id,
                                aws_secret_access_key=secret_access_key)
        config = boto3.session.Config(
            s3={'addressing_style': 'path'}, 
            retries={'max_attempts': retries, 'mode': 'standard'}
        )
        self.client = session.client('s3', endpoint_url=endpoint_url, config=config)
        self.resource = boto3.resource('s3', 
            endpoint_url=endpoint_url, config=config, 
            aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
        )
        self.bucket_name = bucket_name

    def list_files(self) -> List[File]:
        results = []

        for obj in self.client.list_objects(Bucket=self.bucket_name)["Contents"]:
            name = obj["Key"]

            if self.base_dir:
                if not obj["Key"].startswith(self.base_dir):
                    continue

                name = name[len(self.base_dir) + 1:]

            results.append(File(name, obj['LastModified']))

        return results

    def upload(self, local_path: str, remote_name: str = ''):
        self.client.upload_file(local_path, self.bucket_name, self.base_dir + "/" + remote_name)

    def delete(self, remote_name: str):
        self.client.delete_object(Bucket=self.bucket_name, Key=self.base_dir + "/" + remote_name)


def create_fs(fs_type: str, remote_string: str) -> Filesystem:
    """
    Factory method
    """

    if fs_type == "local":
        info("Creating local filesystem")
        data = json.loads(remote_string)
        return Local(from_dict_or_env(data, "path", "RBACKUP_PATH", None))

    if fs_type == "s3":
        info("Creating S3 type filesystem")
        data = json.loads(remote_string)
        return S3(
            endpoint_url=from_dict_or_env(data, "endpoint", "RBACKUP_ENDPOINT", None),
            access_key_id=from_dict_or_env(data, "access_key_id", "RBACKUP_ACCESS_KEY_ID", None),
            secret_access_key=from_dict_or_env(data, "secret_key_id", "RBACKUP_SECRET_KEY_ID", 
            None),
            bucket_name=from_dict_or_env(data, "bucket_name", "RBACKUP_BUCKET_NAME", None),
            base_dir=from_dict_or_env(data, "base_dir", "RBACKUP_BASE_DIR", None),
            retries=int(from_dict_or_env(data, "retries", "RBACKUP_RETRIES", 20))
        )

    raise Exception(f'Unknown filesystem type "{fs_type}"')


def order_files_by_last_modified(input_files: List[File]) -> List[File]:
    return sorted(input_files, key=lambda x: x.last_modified.timestamp(), reverse=True)

def filter_by_pattern(input_files: List[File], pattern: str) -> List[File]:
    pattern = pattern.strip()

    if pattern in ["", "*", ".*", "(.*)"]:
        return input_files

    def filter_func(f: File) -> bool:
        return re.match(pattern, f.name)

    return list(filter(filter_func, input_files))
