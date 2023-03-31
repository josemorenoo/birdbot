import boto3
from datetime import datetime
import json
import os
from typing import Dict, List, Union
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "assets")))


class AssetUtils:
    BUCKET = "coincommit"
    REPO_MANIFEST_LOCATION = "/tmp/repo_manifest.json"
    CONTRIBUTORS_LOCATION = "/tmp/contributors.json"

    @classmethod
    def fetch_report(cls, report_date: datetime) -> str:
        report_date_str: str = report_date.strftime("%Y-%m-%d")
        report_path = f"reports/{report_date_str}/{report_date_str}.json"
        local_report_path = f"/tmp/{report_date_str}.json"

        s3_client = boto3.resource("s3")
        print(cls.BUCKET, report_path, local_report_path)
        s3_client.Bucket(cls.BUCKET).download_file(report_path, local_report_path)
        return local_report_path

    @classmethod
    def fetch_repo_manifest(cls) -> str:
        s3_client = boto3.resource("s3")
        s3_client.Bucket(cls.BUCKET).download_file(
            "assets/repo_manifest.json", cls.REPO_MANIFEST_LOCATION
        )
        return cls.REPO_MANIFEST_LOCATION

    @classmethod
    def fetch_contributors_asset(cls) -> str:
        s3_client = boto3.resource("s3")
        s3_client.Bucket(cls.BUCKET).download_file(
            "assets/contributors.json", cls.CONTRIBUTORS_LOCATION
        )
        return cls.CONTRIBUTORS_LOCATION

    @classmethod
    def open_repo_manifest(cls):
        with open(cls.REPO_MANIFEST_LOCATION, "r") as f:
            return json.load(f)

    @classmethod
    def open_contributors_asset(cls) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        with open(cls.CONTRIBUTORS_LOCATION, "r") as f:
            return json.load(f)
