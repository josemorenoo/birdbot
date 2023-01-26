import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot")))

from typing import Dict, Optional
import tweepy

from config.bird_config import BirdConfig
import report_parser.report_util as report_util

from definitions.graph_names import GRAPH_NAMES

DAILY_REPORTS_PATH = "reports/daily"


class PostMaker:
    def __init__(self, sts_secrets: Optional[Dict[str, str]] = None):
        self.config = BirdConfig(sts_secrets)

        self.auth = tweepy.OAuthHandler(
            self.config.consumer_key, self.config.consumer_secret
        )
        self.auth.set_access_token(self.config.access_key, self.config.access_secret)
        self.tweepy_api = tweepy.API(self.auth)

    def generate_tweet_text(self, report_date, metric, timeframe="DAILY"):
        summary_report_dict = report_util.get_summary_report()
        token_hashtags = " ".join(
            [f"#{each['token']}" for each in summary_report_dict[metric]]
        )

        if timeframe == "DAILY":
            when = "today"
        if timeframe == "WEEKLY":
            when = "this week"

        if metric == "top_by_num_commits":
            status = f"Most active #crypto projects by #github commits {when} 👨‍💻\n\n"
        if metric == "top_by_num_distinct_authors":
            status = f"#crypto projects with most active developers {when} 👩‍💻\n\n"
        if metric == "top_by_new_lines":
            status = f"Most active #crypto project by new lines of code {when} 📈\n\n"
        return status + token_hashtags

    def _post_chart_tweet(self, img_path, tweet_text):
        """this ones actually posts the tweet"""
        print(f"posting img: {img_path}")
        print(tweet_text)

        self.tweepy_api.update_status_with_media(status=tweet_text, filename=img_path)

    def post_loc_chart(self, report_date, timeframe="DAILY"):

        top_loc_img_path = f'/tmp/{GRAPH_NAMES["LOC_AND_EXT"]}'
        loc_tweet_text = self.generate_tweet_text(
            report_date, "top_by_new_lines", timeframe=timeframe
        )

        self._post_chart_tweet(top_loc_img_path, loc_tweet_text)

    def post_authors_chart(self, report_date, timeframe="DAILY"):

        top_distinct_authors_img_path = f'/tmp/{GRAPH_NAMES["AUTHORS_AND_EXT"]}'
        authors_tweet_text = self.generate_tweet_text(
            report_date, "top_by_num_distinct_authors", timeframe=timeframe
        )

        self._post_chart_tweet(top_distinct_authors_img_path, authors_tweet_text)

    def post_top_commits_chart(self, report_date, timeframe="DAILY"):

        top_commits_img_path = f'/tmp/{GRAPH_NAMES["COMMITS_AND_EXT"]}'
        commits_tweet_text = self.generate_tweet_text(
            report_date, "top_by_num_commits", timeframe=timeframe
        )

        self._post_chart_tweet(top_commits_img_path, commits_tweet_text)


if __name__ == "__main__":
    pass
