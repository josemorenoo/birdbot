from datetime import datetime
import os
import random
import sys
import time
from typing import Dict, Optional

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot")))

from assets.asset_utils import AssetUtils

from report_parser.report_util import generate_summary_report

from twitter.post_maker import PostMaker
import twitter.twitter_graphs as graphs


class BirdBot:
    def __init__(self, sts_secrets: Optional[Dict[str, str]] = None) -> None:
        self.sts_secrets = sts_secrets

    def post_loc_chart(self, post_to_twitter=True, mode="DAILY", day=datetime.today()):
        """
        creates and posts graph
        """
        graphs.create_top_by_loc_graph(day, mode=mode)
        if post_to_twitter:
            post = PostMaker(self.sts_secrets)
            post.post_loc_chart(day, timeframe=mode)

    def post_authors_chart(
        self, post_to_twitter=True, mode="DAILY", day=datetime.today()
    ):
        graphs.create_top_by_num_authors_graph(day, mode=mode)
        if post_to_twitter:
            post = PostMaker(self.sts_secrets)
            post.post_authors_chart(day, timeframe=mode)

    def post_commits_chart(
        self, post_to_twitter=True, mode="DAILY", day=datetime.today()
    ):
        graphs.create_top_commits_daily_graph(day, mode=mode)
        if post_to_twitter:
            post = PostMaker(self.sts_secrets)
            post.post_top_commits_chart(day, timeframe=mode)

    def randomize_and_post(
        self,
        funcs,
        delay_secs,
        post_to_twitter=True,
        mode="DAILY",
        day=datetime.today(),
    ):
        random_order_funcs = random.sample(funcs, len(funcs))
        for f in random_order_funcs:
            f(post_to_twitter, mode=mode, day=day)
            time.sleep(delay_secs)

    def make_report_and_post_all_charts(
        self,
        post_to_twitter=True,
        mode="DAILY",
        delay_secs=30,
        day=datetime.today(),
    ):
        # daily_report_local_path: str = fetch_report()

        self.randomize_and_post(
            funcs=[
                self.post_loc_chart,
                self.post_authors_chart,
                self.post_commits_chart,
            ],
            delay_secs=delay_secs,
            post_to_twitter=post_to_twitter,
            mode=mode,
            day=day,
        )

    def tweet(self):
        try:
            report_date = datetime.today()
            AssetUtils.fetch_report(report_date)

            generate_summary_report(report_date)

            self.make_report_and_post_all_charts()
            return True
        except Exception:
            return False


if __name__ == "__main__":
    report_date = datetime.today()
    AssetUtils.fetch_report(report_date)

    generate_summary_report(report_date)
    # post_authors_chart()

    bb = BirdBot()
    # bb.make_report_and_post_all_charts()
    bb.post_authors_chart(post_to_twitter=False)
