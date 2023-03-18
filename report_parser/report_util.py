from datetime import timedelta
from collections import Counter
import json
from typing import Any, List, Dict, Union
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "report_parser")))

from assets.file_extension_imgs.file_extensions import FILE_EXTENSIONS
from report_parser.prices import Prices
from assets.asset_utils import AssetUtils


def generate_summary_report(report_date, report_path=None, mode="DAILY") -> str:
    """Displays the top 10 projects across multiple categories
    - most commits
    - most new lines of code
    - most distinct authors

    Assumes the daily report already exists at reports/daily/<YYY-MM-DD>/<YYY-MM-DD>.json

    Args:
        report_date_str (str): "YYYY-MM-DD"
    """
    report_date_str = report_date.strftime("%Y-%m-%d")

    # display the top 10 from the daily report
    by_commits = get_most_active_by_commits(
        report_date_str, report_path, n=10, mode=mode
    )
    by_LOC = get_most_active_by_loc(report_date_str, report_path, n=10, mode=mode)
    by_distinct_authors = get_most_active_by_author(
        report_date_str, report_path, n=10, mode=mode
    )

    summary_report = {"tokens_represented": {}}

    # now get the open/close price for each token in report
    tokens_represented = set(
        [x[0] for x in by_commits]
        + [x[0] for x in by_LOC]
        + [x[0] for x in by_distinct_authors]
    )
    prices = Prices()
    price_data = prices.get_prices(list(tokens_represented))

    # price_data = {"24hr": {sym: None for sym in tokens_represented}}
    if "DAILY" in mode:
        time_key = "24hr"
    if "WEEKLY" in mode:
        time_key = "7d"

    for token_symbol, price_change in price_data[time_key].items():
        summary_report["tokens_represented"][token_symbol] = {
            "delta_percentage": price_change,
        }

    summary_report["top_by_num_commits"] = [
        {"token": token, "count": count} for token, count in by_commits
    ]
    summary_report["top_by_new_lines"] = [
        {"token": token, "count": count} for token, count in by_LOC
    ]
    summary_report["top_by_num_distinct_authors"] = [
        {"token": token, "count": count, "active_ratio": active_ratio, "label": label}
        for token, count, active_ratio, label in by_distinct_authors
    ]

    output_path = ""
    if mode == "DAILY":
        output_path = f"/tmp/{report_date_str}_summary.json"
    if mode == "WEEKLY":
        output_path = "/tmp/weekly_summary.json"
    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=2)
    return output_path


### ### ### ### ### vvv METRICS vvv ### ### ### ### ###


def get_most_active_by_commits(
    report_date_str: str, report_path=None, n=10, mode="DAILY"
):
    """Sorts tokens by most active to least active

    Args:
        report_date_str ([type]): [YYYY-MM-DD]
        n ([type]): [the top n to add to the list]

    Returns:
        [List[tuple(token_name, commit_count)]
    """
    if mode == "DAILY":
        report_json_path = f"/tmp/{report_date_str}.json"

    if report_path:
        report_json_path = report_path

    with open(report_json_path, "r") as f:
        report = json.load(f)

    # sort in descending order, [(token_name, commit_count or lines_of_code), ...]
    sort_by_metric = lambda report_list: sorted(
        report_list, key=lambda x: x[1], reverse=True
    )
    report_by_most_commits_as_list = [
        (token_name, int(token_data["commit_count"]))
        for token_name, token_data in report.items()
    ]
    by_commits = sort_by_metric(report_by_most_commits_as_list)[:n]
    print("\nTop projects by # of commits", *by_commits, sep="\n")
    return by_commits


def get_most_active_by_author(
    report_date_str: str, report_path=None, n=10, mode="DAILY"
):
    """Sorts tokens by most active to least active

    Args:
        report_date_str ([type]): [YYYY-MM-DD]
        n ([type]): [the top n to add to the list]

    Returns:
        [List[tuple(token_name, commit_count)]
    """
    AssetUtils.fetch_contributors_asset()
    historical_contributors: Dict[
        str, List[Dict[str, Union[str, int]]]
    ] = AssetUtils.open_contributors_asset()

    report_json_path = f"/tmp/{report_date_str}.json"
    if report_path:
        report_json_path = report_path

    with open(report_json_path, "r") as f:
        report = json.load(f)

    def get_active_ratio(token_name: str, active_contributors: int) -> float:
        all_project_contributors = historical_contributors[token_name]
        return float(active_contributors) / len(all_project_contributors)

    authors_by_project = [
        # token, count, active_ratio
        (
            token_name,
            len(set(data["distinct_authors"])),
            get_active_ratio(token_name, len(set(data["distinct_authors"]))),
            f'{len(set(data["distinct_authors"]))}/{len(historical_contributors[token_name])} devs',
        )
        for token_name, data in report.items()
    ]

    top_n_projects_by_authors = sorted(
        authors_by_project, key=lambda x: x[2], reverse=True
    )[:n]

    return top_n_projects_by_authors


def get_most_active_by_loc(report_date_str: str, report_path=None, n=10, mode="DAILY"):
    """Sorts tokens by most active to least active

    Args:
        report_date_str ([type]): [YYYY-MM-DD]
        n ([type]): [the top n to add to the list]

    Returns:
        [List[tuple(token_name, commit_count)]
    """
    if mode == "DAILY":
        report_json_path = f"/tmp/{report_date_str}.json"
    if report_path:
        report_json_path = report_path

    with open(report_json_path, "r") as f:
        report = json.load(f)

    # sort in descending order, [(token_name, commit_count or lines_of_code), ...]
    sort_by_metric = lambda report_list: sorted(
        report_list, key=lambda x: x[1], reverse=True
    )
    report_by_most_LOC_list = [
        (token_name, int(token_data["lines_of_code"]))
        for token_name, token_data in report.items()
    ]
    by_LOC = sort_by_metric(report_by_most_LOC_list)[:n]
    print("\nTop projects by new lines of code", *by_LOC, sep="\n")
    return by_LOC


def get_file_extensions_and_lines_of_code_modified(project_commits):
    """
    USED TO POPULATE THE DAILY/WEEKLY REPORT

    For a single token,

    returns a count of how many times each file type shows up,
    and a count of how many files were affected by each respective file extension

    ABC: {
        json: {extension_count: 4, loc_modified: 233},
        py: {extension_count: 3, loc_modified: -4}
    }
    """

    project_ext_count_and_loc_affected = {}
    for commit in project_commits:

        # count how many times each file extension was modified for this token
        for ext, commit_ext_count in Counter(commit.file_extensions).items():
            if ext not in project_ext_count_and_loc_affected:
                project_ext_count_and_loc_affected[ext] = {
                    "extension_count": commit_ext_count
                }
            else:
                project_ext_count_and_loc_affected[ext][
                    "extension_count"
                ] += commit_ext_count

            # log out if extension is new so we can add a picture of it
            if ext not in FILE_EXTENSIONS:
                print(f"NEW EXTENSIONS ALERT: {ext}")

        # count the number of lines of code affected for each respective file extension
        for (
            ext,
            loc_modified_for_extension,
        ) in commit.loc_changed_by_file_extension.items():
            project_ext_count_and_loc_affected[ext][
                "loc_modified"
            ] = loc_modified_for_extension

    return project_ext_count_and_loc_affected


def get_file_extension_breakdown_from_summary_report(
    token, report_date, mode="DAILY", verbose=False
):
    """
    PULLS FROM DAILY/WEEKLY REPORT

    for a single token,

    return a dict of file extensions that were modified, and their count, as well as the number of files affected

    # sort by number of file extensions updated
    """
    raw_report = get_raw_report(
        report_date=report_date, mode=mode
    )  # raw means daily/weekly

    def combine_dicts(d1, d2):
        return dict(list(d1.items()) + list(d2.items()))

    token_specific_extension_data = [
        {"extension": file_extension, "extension_count": extension_count}
        for file_extension, extension_count in raw_report[token][
            "file_extensions"
        ].items()
    ]

    sorted_by_extension_count = sorted(
        token_specific_extension_data, key=lambda x: x["extension_count"], reverse=True
    )
    if verbose:
        print(f"Most popular file extensions for {token}")
        print(*sorted_by_extension_count, sep="\n")
    return sorted_by_extension_count


def get_changed_methods(project_commits) -> List[str]:
    """
    Used to populate the DAILY/WEEKLY reports, gets a list of
    method names that were changed.

    Note: Removes duplicates from list, sometimes same method is touched in more than one commit
    """
    project_changed_methods = []
    for commit in project_commits:
        for file in commit.modified_files:
            method_names = [m.name for m in file.changed_methods]
            project_changed_methods.extend(method_names)
    print(*project_changed_methods, sep="\n")
    return list(set(project_changed_methods))


### ### ### ### ### ### vvv PRICE vvv ### ### ### ### ### ###


def get_daily_price_deltas(sorted_tokens: List[Any], report_date, mode="DAILY"):
    summary_report = get_summary_report()
    return [
        summary_report["tokens_represented"][token]["delta_percentage"]
        for token in sorted_tokens
    ]


### ### ### ### ### ### vvv REPORTS vvv
#
#  ### ### ### ### ### ###
def get_summary_report():
    with open(f"/tmp/summary.json", "r") as f:
        summary_report = json.load(f)
    return summary_report


def get_raw_report(report_date, mode="DAILY"):
    report_date_str = report_date.strftime("%Y-%m-%d")
    if mode == "DAILY":
        with open(
            f"/tmp/{report_date_str}.json",
            "r",
        ) as f:
            raw_report = json.load(f)
    return raw_report
