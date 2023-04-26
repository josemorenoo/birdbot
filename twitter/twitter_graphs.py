from datetime import datetime
import os
import plotly.graph_objs as go
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "twitter")))

from definitions.colors import COLORS
from definitions.graph_names import GRAPH_NAMES
import twitter.price_delta_supplement as price_delta
import twitter.file_extension_supplement as extensions

import report_parser.report_util as report_util


def create_img(image_path, fig):
    fig.write_image(image_path)
    print(f"image saved: {image_path}")


def create_top_by_loc_graph(report_date, mode="DAILY"):
    report_date_str = report_date.strftime("%Y-%m-%d")
    if mode == "DAILY":
        title = "Today's Top 10 Tokens by New Lines of Code"
        REPORT_DIR = f"/tmp"

    # get data
    by_locs = report_util.get_most_active_by_loc(report_date_str, mode=mode)

    # flip so that they show up in descending order on HORIZONTAL bar graph
    by_locs = by_locs[::-1]

    token_list = [loc[0] for loc in by_locs]
    locs_list = [loc[1] for loc in by_locs]

    data = [
        go.Bar(y=[f"{token} " for token in token_list], x=locs_list, orientation="h")
    ]

    layout = go.Layout(
        template="plotly_dark",
        margin=dict(l=130),
        plot_bgcolor=COLORS["background_blue"],  # plot dark background
        title=dict(text=title, x=0.5, font_size=18),  # center title
        font=dict(family="courier"),
        xaxis=dict(
            title=dict(text="New Lines of Code", font=dict(size=20)),
            tickfont=dict(size=18),
        ),
        yaxis=dict(
            title=dict(
                text="Token",
                font=dict(size=20),
                standoff=10,  # give the axis title some spacing from the tickers, left spacing is fig margin, see above
            ),
            tickfont=dict(size=18),
        ),
    )

    fig = go.Figure(data=data, layout=layout)

    fig.update_traces(
        marker_color=COLORS["loc_pink"],
        textposition="inside",
        text=[f"+{loc_count}" for loc_count in locs_list],  # bar graph annotations
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
    token_list = [metadata[0] for metadata in by_authors]
    distinct_dev_counts = [metadata[1] for metadata in by_authors]
    active_team_ratio = [metadata[2] for metadata in by_authors]
    labels = [metadata[3] for metadata in by_authors]

    data = [
        go.Bar(
            y=[f"{token} " for token in token_list],
            x=[round(100 * r, 2) for r in active_team_ratio],
            orientation="h",
        )
    ]

    layout = go.Layout(
        template="plotly_dark",
        margin=dict(l=130),
        plot_bgcolor=COLORS["background_blue"],  # plot dark background
        title=dict(text=title, x=0.5, font_size=18),  # center title
        font=dict(family="courier"),
        xaxis=dict(
            title=dict(text="Active Team Percentage (%)", font=dict(size=20)),
            tickfont=dict(size=18),
        ),
        yaxis=dict(
            title=dict(
                text="Token",
                font=dict(size=20),
                standoff=10,  # give the axis title some spacing from the tickers, left spacing is fig margin, see above
            ),
            tickfont=dict(size=18),
        ),
    )

    fig = go.Figure(data=data, layout=layout)

    fig.update_traces(
        marker_color=COLORS["dev_purple"],
        textposition="inside",
        text=[l for l in labels],  # bar graph annotations
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
        tokens_represented_in_graph=token_list,
        bar_percentages=bar_percentages,
    )

    with_extension_logos.save(f"{REPORT_DIR}/{GRAPH_NAMES['AUTHORS_AND_EXT']}")

    # remove graph without price delta
    # os.remove(image_path)


def create_top_commits_daily_graph(report_date, mode="DAILY"):
    report_date_str = report_date.strftime("%Y-%m-%d")
    if mode == "DAILY":
        title = "Today's Top 10 Tokens by Most Commits"
        REPORT_DIR = f"/tmp"

    # get data
    by_commits = report_util.get_most_active_by_commits(report_date_str, mode=mode)

    # flip so that they show up in descending order on HORIZONTAL bar graph
    by_commits = by_commits[::-1]

    token_list = [x[0] for x in by_commits]
    commits_list = [x[1] for x in by_commits]

    data = [
        go.Bar(y=[f"{token} " for token in token_list], x=commits_list, orientation="h")
    ]

    layout = go.Layout(
        template="plotly_dark",
        margin=dict(l=130),
        plot_bgcolor=COLORS["background_blue"],  # plot dark background
        title=dict(text=title, x=0.5, font_size=18),  # center title
        font=dict(family="courier"),
        xaxis=dict(
            title=dict(text="Number of Commits", font=dict(size=20)),
            tickfont=dict(size=18),
        ),
        yaxis=dict(
            title=dict(
                text="Token",
                font=dict(size=20),
                standoff=10,  # give the axis title some spacing from the tickers, left spacing is fig margin, see above
            ),
            tickfont=dict(size=18),
        ),
    )

    fig = go.Figure(data=data, layout=layout)

    fig.update_traces(
        marker_color=COLORS["text_green"],
        textposition="inside",
        text=[f"+{loc_count}" for loc_count in commits_list],  # bar graph annotations
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
    create_top_by_num_authors_graph(datetime(2022, 2, 14), mode="DAILY")
    create_top_commits_daily_graph(datetime(2022, 2, 14), mode="DAILY")
    create_top_by_loc_graph(datetime(2022, 2, 14), mode="DAILY")
