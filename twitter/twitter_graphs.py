from datetime import datetime
import dataframe_image as df_image
import os
import pandas as pd
from PIL import Image
import plotly.express as px
import sys
from tkinter import Y


from definitions.colors import COLORS
from definitions.graph_names import GRAPH_NAMES
import twitter.price_delta_supplement as price_delta
import twitter.file_extension_supplement as extensions

import report_parser.report_util as report_util

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "twitter")))


def create_img(image_path, fig):
    fig.write_image(image_path)
    print(f"image saved: {image_path}")


def create_file_extension_base_img(
    tokens_represented, report_date, mode="DAILY", limit=6
):
    """creates an image representing the top 6 files modified for each project by converting a dataframe into an image"""
    report_date_str = report_date.strftime("%Y-%m-%d")

    for token in tokens_represented:
        # get_data, sorted list of: [{extension: 'abc', extension_count: 4, loc_modified: 34}, {...}, ...]
        extension_counts_and_loc_by_token = (
            report_util.get_file_extension_breakdown_from_summary_report(
                token, report_date, mode=mode
            )
        )

        # convert to list of lists (each sub list is a df row): [[.ext_name, extension count, loc modified]]
        create_df_row = lambda row_list: [f".{row_list[0]}", row_list[1], row_list[2]]
        extension_data = [
            create_df_row(list(v.values())) for v in extension_counts_and_loc_by_token
        ]

        # save most common file extensions to dataframe
        token_specific_df = pd.DataFrame(
            extension_data[:limit],
            columns=["file extension", "extension count", "lines of code added"],
        )

        # styling
        styled_df = token_specific_df.style.background_gradient()

        TOKEN_SPECIFIC_DIR = f"tmp/token_specific/"
        IMG_PATH = TOKEN_SPECIFIC_DIR + f"{token}_file_extensions_base_img.png"
        IMG_PATH_TMP = IMG_PATH + ".tmp"

        # make directory if it doesn't exist
        if not os.path.exists(TOKEN_SPECIFIC_DIR):
            os.mkdir(TOKEN_SPECIFIC_DIR)

        # save to tmp image so we can crop after
        df_image.export(styled_df, IMG_PATH_TMP)

        # now crop the image to remove the index on the left side of the image
        # crop: left, top, right, bottom
        tmp_img = Image.open(IMG_PATH_TMP)
        cropped_img = tmp_img.crop((50, 0, tmp_img.width, tmp_img.height))
        cropped_img.save(IMG_PATH)
        os.remove(IMG_PATH_TMP)


def create_top_by_loc_graph(report_date, mode="DAILY"):
    report_date_str = report_date.strftime("%Y-%m-%d")
    if mode == "DAILY":
        title = "Today's Top 10 Tokens by New Lines of Code"
        REPORT_DIR = f"/tmp"

    # get data
    by_locs = report_util.get_most_active_by_loc(report_date_str, mode=mode)

    # flip so that they show up in descending order on HORIZONTAL bar graph
    by_locs = by_locs[::-1]

    by_locs_df = pd.DataFrame(by_locs, columns=["Token", "New Lines of Code"])

    fig = px.bar(
        by_locs_df,
        title=title,
        x="New Lines of Code",
        y=[
            f"{token} " for token in by_locs_df["Token"]
        ],  # Give the damn token label some breathing room
        orientation="h",
        template="plotly_dark",  # fig dark background
    )
    fig.update_layout(
        margin=dict(l=130),
        plot_bgcolor=COLORS["background_blue"],  # plot dark background
        title=dict(x=0.5, font_size=18),  # center title
        font=dict(family="courier"),
        xaxis=dict(title=dict(font=dict(size=20)), tickfont=dict(size=18)),
        yaxis=dict(
            title=dict(
                text="Token",
                font=dict(size=20),
                standoff=10,  # give the axis title some spacing from the tickers, left spacing is fig margin, see above
            ),
            tickfont=dict(size=18),
        ),
    )
    fig.update_traces(
        marker_color=COLORS["loc_pink"],
        textposition="inside",
        text=[
            f"+{loc_count}" for loc_count in by_locs_df["New Lines of Code"]
        ],  # bar graph annotations
        textfont=dict(color=COLORS["background_blue"], size=20),
    )

    # save to image
    image_path = f"{REPORT_DIR}/{GRAPH_NAMES['LOC']}"
    create_img(image_path, fig)

    # add price supplement image
    combined_img = price_delta.add_price_deltas(
        existing_img_name=GRAPH_NAMES["LOC"],
        new_graph_name=GRAPH_NAMES["LOC_AND_PRICE"],
        report_date=report_date,
        mode=mode,
    )

    # get each bar in the graph as a percentage of the largest bar in the graph.
    # used to figure out where to put the file extension images on the graph
    bar_percentages = [x[1] / by_locs[-1][1] for x in by_locs[::-1]]

    tokens_represented = [metadata[0] for metadata in by_locs]
    with_extension_logos = extensions.add_ext_imgs_to_graph(
        bar_graph_img=combined_img,
        report_date=report_date,
        tokens_represented_in_graph=tokens_represented,
        bar_percentages=bar_percentages,
    )

    with_extension_logos.save(f"{REPORT_DIR}/{GRAPH_NAMES['LOC_AND_EXT']}")

    # remove graph without price delta
    os.remove(image_path)


def create_top_by_num_authors_graph(report_date, mode="DAILY"):
    report_date_str = report_date.strftime("%Y-%m-%d")
    if mode == "DAILY":
        title = "Today's Top 10 Tokens by Dev Team Activity"
        REPORT_DIR = f"/tmp"

    # get data
    by_authors = report_util.get_most_active_by_author(report_date_str, mode=mode)

    # flip so that they show up in descending order on HORIZONTAL bar graph
    by_authors = by_authors[::-1]
    tokens_represented = [metadata[0] for metadata in by_authors]

    by_authors_df = pd.DataFrame(
        by_authors,
        columns=[
            "Token",
            "Number of Distinct Developers",
            "Active Team Ratio",
            "Label",
        ],
    )
    fig = px.bar(
        by_authors_df,
        title=title,
        x="Active Team Ratio",
        y=[
            f"{token} " for token in by_authors_df["Token"]
        ],  # Give the damn token label some breathing room
        orientation="h",
        template="plotly_dark",  # fig dark background
    )
    fig.update_layout(
        margin=dict(l=130),
        plot_bgcolor=COLORS["background_blue"],  # plot dark background
        title=dict(x=0.5, font_size=18),  # center title
        font=dict(family="courier"),
        xaxis=dict(title=dict(font=dict(size=20)), tickfont=dict(size=18)),
        yaxis=dict(
            title=dict(
                text="Token",
                font=dict(size=20),
                standoff=10,  # give the axis title some spacing from the tickers, left spacing is fig margin, see above
            ),
            tickfont=dict(size=18),
        ),
    )
    fig.update_traces(
        marker_color=COLORS["dev_purple"],
        textposition="inside",
        text=by_authors_df["Label"],
        textfont=dict(color=COLORS["background_blue"], size=20),
    )

    # save to image
    image_path = f"{REPORT_DIR}/{GRAPH_NAMES['AUTHORS']}"
    create_img(image_path, fig)

    # add price supplement image
    combined_img = price_delta.add_price_deltas(
        existing_img_name=GRAPH_NAMES["AUTHORS"],
        new_graph_name=GRAPH_NAMES["AUTHORS_AND_PRICE"],
        report_date=report_date,
        mode=mode,
    )

    # get each bar in the graph as a percentage of the largest bar in the graph.
    # used to figure out where to put the file extension images on the graph
    bar_percentages = [x[2] / by_authors[-1][2] for x in by_authors[::-1]]

    with_extension_logos = extensions.add_ext_imgs_to_graph(
        bar_graph_img=combined_img,
        report_date=report_date,
        tokens_represented_in_graph=tokens_represented,
        bar_percentages=bar_percentages,
    )

    with_extension_logos.save(f"{REPORT_DIR}/{GRAPH_NAMES['AUTHORS_AND_EXT']}")

    # remove graph without price delta
    os.remove(image_path)


def create_top_commits_daily_graph(report_date, mode="DAILY"):
    report_date_str = report_date.strftime("%Y-%m-%d")
    if mode == "DAILY":
        title = "Today's Top 10 Tokens by Most Commits"
        REPORT_DIR = f"/tmp"

    # get data
    by_commits = report_util.get_most_active_by_commits(report_date_str, mode=mode)

    # flip so that they show up in descending order on HORIZONTAL bar graph
    by_commits = by_commits[::-1]

    # create top n commits graph
    by_commits_df = pd.DataFrame(by_commits, columns=["Token", "Number of commits"])
    fig = px.bar(
        by_commits_df,
        title=title,
        x="Number of commits",
        y=[
            f"{token} " for token in by_commits_df["Token"]
        ],  # Give the damn token label some breathing room
        orientation="h",
        template="plotly_dark",  # fig dark background
    )
    fig.update_layout(
        margin=dict(l=130),
        plot_bgcolor=COLORS["background_blue"],  # plot dark background
        title=dict(x=0.5, font_size=22),  # center title
        font=dict(family="courier"),
        xaxis=dict(title=dict(font=dict(size=20)), tickfont=dict(size=18)),
        yaxis=dict(
            title=dict(
                text="Token",
                font=dict(size=20),
                standoff=10,  # give the axis title some spacing from the tickers, left spacing is fig margin, see above
            ),
            tickfont=dict(size=18),
        ),
    )
    fig.update_traces(
        marker_color=COLORS["text_green"],
        textposition="inside",
        text=by_commits_df["Number of commits"],
        textfont=dict(color=COLORS["background_blue"], size=20),
    )

    # save to image
    image_path = f"{REPORT_DIR}/{GRAPH_NAMES['COMMITS']}"
    create_img(image_path, fig)

    # add price supplement image
    combined_img = price_delta.add_price_deltas(
        existing_img_name=GRAPH_NAMES["COMMITS"],
        new_graph_name=GRAPH_NAMES["COMMITS_AND_PRICE"],
        report_date=report_date,
        mode=mode,
    )

    # get each bar in the graph as a percentage of the largest bar in the graph.
    # used to figure out where to put the file extension images on the graph
    bar_percentages = [x[1] / by_commits[-1][1] for x in by_commits[::-1]]

    tokens_represented = [metadata[0] for metadata in by_commits]
    with_extension_logos = extensions.add_ext_imgs_to_graph(
        bar_graph_img=combined_img,
        report_date=report_date,
        bar_percentages=bar_percentages,
        tokens_represented_in_graph=tokens_represented,
    )

    with_extension_logos.save(f"{REPORT_DIR}/{GRAPH_NAMES['COMMITS_AND_EXT']}")

    # remove graph without price delta
    os.remove(image_path)


if __name__ == "__main__":
    """
    create_top_commits_daily_graph()
    create_top_by_num_authors_graph()
    create_top_by_loc_graph()
    """
    # create_file_extension_base_img(['ICP', 'ETH'], datetime(2022, 2, 13), "DAILY")
    create_top_by_num_authors_graph(datetime(2022, 2, 14), mode="DAILY")
    create_top_commits_daily_graph(datetime(2022, 2, 14), mode="DAILY")
    create_top_by_loc_graph(datetime(2022, 2, 14), mode="DAILY")
