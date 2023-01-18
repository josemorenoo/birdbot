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

    @staticmethod
    def fetch_report(report_date: datetime) -> str:
        report_date_str: str = report_date.strftime("%Y-%m-%d")
        report_path = f"reports/{report_date_str}/{report_date_str}.json"
        local_report_path = f"/tmp/{report_date_str}.json"

        s3_client = boto3.resource("s3")
        s3_client.Bucket(Bucket).download_file(report_path, local_report_path)
        return local_report_path

    @staticmethod
    def fetch_repo_manifest() -> str:
        s3_client = boto3.resource("s3")
        s3_client.Bucket(Bucket).download_file(
            "assets/repo_manifest.json", REPO_MANIFEST_LOCATION
        )
        return REPO_MANIFEST_LOCATION

    @staticmethod
    def fetch_contributors_asset() -> str:
        s3_client = boto3.resource("s3")
        s3_client.Bucket(Bucket).download_file(
            "assets/contributors.json", CONTRIBUTORS_LOCATION
        )
        return CONTRIBUTORS_LOCATION

    @staticmethod
    def open_repo_manifest():
        with open(REPO_MANIFEST_LOCATION, "r") as f:
            return json.load(f)

    @staticmethod
    def open_contributors_asset() -> Dict[str, List[Dict[str, Union[str, int]]]]:
        with open(CONTRIBUTORS_LOCATION, "r") as f:
            return json.load(f)
