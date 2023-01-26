from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from typing import List

import report_parser.report_util as report_util

from definitions.colors import COLORS
from definitions.graph_names import GRAPH_NAMES

FONT_ASSET = "assets/arial.ttf"


def add_price_deltas(
    existing_img_name: str, new_graph_name: str, report_date: datetime, mode: str
):
    report_date_str = report_date.strftime("%Y-%m-%d")

    # open and crop existing bar graph image
    existing_img = open_existing_img(existing_img_name, report_date_str, mode)
    existing_img_cropped = crop_original_photo(existing_img)

    # get price deltas for each token in graph, create price img supplement
    _, height = existing_img_cropped.size
    price_deltas = get_price_deltas_from_summary_report(
        existing_img_name, report_date, mode
    )

    price_img = create_price_supplemental_image(price_deltas, height)

    # combine images and save
    combined_img = combine_graph_and_price_img(existing_img_cropped, price_img)
    combined_img.save(f"/tmp/{new_graph_name}")
    return combined_img


def open_existing_img(chart_name: str, report_date_str: str, mode: str):
    # load graphs with top commits, top lines of code and top authors
    return Image.open(f"/tmp/{chart_name}")


def crop_original_photo(original_img):
    # crop original graph images to avoid having a lot of space on the right where the price will be inserted.
    return original_img.crop((0, 0, 630, original_img.height))


def get_price_deltas_from_summary_report(
    existing_img_name: str, report_date: datetime, mode: str = "DAILY"
):
    summary_report = report_util.get_summary_report()
    if existing_img_name == GRAPH_NAMES["COMMITS"]:
        summary_report_key = "top_by_num_commits"
    elif existing_img_name == GRAPH_NAMES["AUTHORS"]:
        summary_report_key = "top_by_num_distinct_authors"
    elif existing_img_name == GRAPH_NAMES["LOC"]:
        summary_report_key = "top_by_new_lines"
    else:
        raise ValueError(
            f"{existing_img_name} is not in {[GRAPH_NAMES['COMMITS'], GRAPH_NAMES['AUTHORS'], GRAPH_NAMES['LOC']]}"
        )

    # reverse so that tokens show up in correct order
    tokens_represented_on_chart = [
        token_info["token"] for token_info in summary_report[summary_report_key]
    ][::-1]
    get_price_percentage_delta = lambda token: summary_report["tokens_represented"][
        token
    ]["delta_percentage"]
    price_deltas = [
        get_price_percentage_delta(token) for token in tokens_represented_on_chart
    ]

    print(f"tokens represented in {existing_img_name}:")
    print(tokens_represented_on_chart)
    print(f"\nprice deltas for {existing_img_name}:")
    print(price_deltas)
    return price_deltas


def create_price_supplemental_image(
    price_deltas: List[float], height: int = 500, width: int = 150
):
    """
    Creates the supplemental price delta img that goes on the right side of each bar graph
    posted on Twitter. Bar graph is generated first, then this image, and finally both are combined
    """

    # create the image
    price_image = Image.new(
        "RGB", (width, height), color=COLORS["darkest_blue"]
    )  # same height as original graph
    price_drawing = ImageDraw.Draw(price_image)

    # formatting

    my_font = ImageFont.truetype(FONT_ASSET, size=17)
    spacing = 33  # space between each price
    y_offset = 105  # offset from top of image
    x_offset = 5  # offset from left of (new) image -- nice to use to center the DELTA PRICE text with the actual numbers

    # Insert "Price Change" Text on top of numbers
    price_drawing.text(
        (0, y_offset - 30), "\u0394 Price", fill=(255, 255, 255), font=my_font
    )

    # insert the price deltas
    for i in range(0, len(price_deltas)):  # num tokens
        price_change = price_deltas[-i - 1]
        if price_change:
            # make font red for negative changes, green for positive changes
            color = (
                COLORS["text_green"]
                if price_change >= 0
                else COLORS["great_depression_red"]
            )
            price_drawing.text(
                (x_offset, y_offset + spacing * i),
                f"{price_change} %",
                fill=color,
                font=my_font,
            )
        else:
            # price change unavailable, probable coin not supported by coinbase
            color = COLORS["walter_white"]
            price_drawing.text(
                (x_offset, y_offset + spacing * i), "N/A", fill=color, font=my_font
            )

    return price_image


def combine_graph_and_price_img(bar_graph_img, price_img):
    """
    Combine a bar graph and the price delta supplement generated.
    """
    combined_img = Image.new(
        "RGB", (bar_graph_img.width + price_img.width, bar_graph_img.height)
    )
    combined_img.paste(bar_graph_img, (0, 0))
    combined_img.paste(price_img, (bar_graph_img.width, 0))
    return combined_img
