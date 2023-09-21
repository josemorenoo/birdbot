import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "twitter")))

from typing import Dict, Optional
import tweepy

from config.bird_config import BirdConfig
import report_parser.report_util as report_util

from definitions.graph_names import GRAPH_NAMES

DAILY_REPORTS_PATH = "reports/daily"


class PostMaker:
    def __init__(self, sts_secrets: Optional[Dict[str, str]] = None):
        self.config = BirdConfig(sts_secrets)

    def generate_tweet_text(self, metric, timeframe="DAILY"):
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
        print(f"posting img: {img_path}")

        auth = tweepy.OAuth1UserHandler(
            consumer_key=self.config.consumer_key,
            consumer_secret=self.config.consumer_secret,
            access_token=self.config.access_key,
            access_token_secret=self.config.access_secret,
        )

        api = tweepy.API(auth)

        # Upload the image
        media = api.media_upload(filename=img_path)
        media_id = media.media_id

        # OAuth2 authentication for creating tweet
        client = tweepy.Client(
            bearer_token=self.config.bearer_token,
            consumer_key=self.config.consumer_key,
            consumer_secret=self.config.consumer_secret,
            access_token=self.config.access_key,
            access_token_secret=self.config.access_secret,
        )

        # Create a tweet with the uploaded media
        client.create_tweet(text=tweet_text, media_ids=[media_id])
        print("Done posting image!")

    def post_loc_chart(self, report_date, timeframe="DAILY"):
        top_loc_img_path = f'/tmp/{GRAPH_NAMES["LOC_AND_EXT"]}'
        loc_tweet_text = self.generate_tweet_text(
            "top_by_new_lines", timeframe=timeframe
        )

        self._post_chart_tweet(top_loc_img_path, loc_tweet_text)

    def post_authors_chart(self, report_date, timeframe="DAILY"):
        top_distinct_authors_img_path = f'/tmp/{GRAPH_NAMES["AUTHORS_AND_EXT"]}'
        authors_tweet_text = self.generate_tweet_text(
            "top_by_num_distinct_authors", timeframe=timeframe
        )

        self._post_chart_tweet(top_distinct_authors_img_path, authors_tweet_text)

    def post_top_commits_chart(self, report_date, timeframe="DAILY"):
        top_commits_img_path = f'/tmp/{GRAPH_NAMES["COMMITS_AND_EXT"]}'
        commits_tweet_text = self.generate_tweet_text(
            "top_by_num_commits", timeframe=timeframe
        )

        self._post_chart_tweet(top_commits_img_path, commits_tweet_text)


if __name__ == "__main__":
    pass
