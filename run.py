from datetime import datetime
import random
import time

from assets.asset_utils import AssetUtils

from report_parser.report_util import generate_summary_report

from twitter.post_maker import PostMaker
import twitter.twitter_graphs as graphs

# YESTERDAY = datetime.today() - timedelta(hours=24)


def post_loc_chart(post_to_twitter=True, mode="DAILY", day=datetime.today()):
    """
    creates and posts graph
    """
    graphs.create_top_by_loc_graph(day, mode=mode)
    if post_to_twitter:
        post = PostMaker()
        post.post_loc_chart(day, timeframe=mode)


def post_authors_chart(post_to_twitter=True, mode="DAILY", day=datetime.today()):
    graphs.create_top_by_num_authors_graph(day, mode=mode)
    if post_to_twitter:
        post = PostMaker()
        post.post_authors_chart(day, timeframe=mode)


def post_commits_chart(post_to_twitter=True, mode="DAILY", day=datetime.today()):
    graphs.create_top_commits_daily_graph(day, mode=mode)
    if post_to_twitter:
        post = PostMaker()
        post.post_top_commits_chart(day, timeframe=mode)


def randomize_and_post(
    funcs, delay_secs, post_to_twitter=True, mode="DAILY", day=datetime.today()
):
    random_order_funcs = random.sample(funcs, len(funcs))
    for f in random_order_funcs:
        f(post_to_twitter, mode=mode, day=day)
        time.sleep(delay_secs)


def make_report_and_post_all_charts(
    post_to_twitter=True,
    mode="DAILY",
    delay_secs=30,
    day=datetime.today(),
):
    # daily_report_local_path: str = fetch_report()

    randomize_and_post(
        funcs=[post_loc_chart, post_authors_chart, post_commits_chart],
        delay_secs=delay_secs,
        post_to_twitter=post_to_twitter,
        mode=mode,
        day=day,
    )


if __name__ == "__main__":
    report_date = datetime.today()
    # AssetUtils.fetch_report(report_date)

    # generate_summary_report(report_date)

    post_loc_chart(
        post_to_twitter=True,
    )
