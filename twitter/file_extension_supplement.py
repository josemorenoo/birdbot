from PIL import Image
from typing import List

from assets.file_extension_imgs.file_extensions import FILE_EXTENSIONS

import report_parser.report_util as report_util


def add_ext_imgs_to_graph(
    bar_graph_img,
    bar_percentages: List[float],
    tokens_represented_in_graph: List[str],
    report_date,
    timeframe,
    top_n=5,
):
    """
    extensions is a list of lists containing extensions, each sublist represents one bar
    in order from top to bottom

    only add the top 5 to each bar graph
    """

    get_ext_for_token = lambda token: [
        ext["extension"]
        for ext in report_util.get_file_extension_breakdown_from_summary_report(
            token, report_date, timeframe, verbose=False
        )
    ]

    extensions: List[List[str]] = [
        get_ext_for_token(token) for token in tokens_represented_in_graph
    ][::-1]

    for bar_idx in range(len(extensions)):
        num_ext_for_this_bar = len(extensions[bar_idx])
        if num_ext_for_this_bar < top_n:
            num_ext_to_add = num_ext_for_this_bar
        else:
            num_ext_to_add = top_n

        logo_idx = 0
        skipped = 0
        while logo_idx < num_ext_to_add:
            ext_name = extensions[bar_idx][logo_idx]
            if ext_name not in FILE_EXTENSIONS:
                print(
                    f"Warning: file extension missing from images: {ext_name}, skipping"
                )
                skipped += 1
                logo_idx += 1
                continue
            else:
                ext_img_path = FILE_EXTENSIONS[ext_name]["path"]
                bar_graph_img = combine_graph_and_ext_img(
                    bar_graph_img,
                    ext_img=Image.open(ext_img_path),
                    bar_from_top=bar_idx,
                    logo_idx=logo_idx - skipped,
                    top_n=top_n,
                    bar_percentage=bar_percentages[bar_idx],
                )
                logo_idx += 1

    return bar_graph_img


def combine_graph_and_ext_img(
    bar_graph_img,
    ext_img,
    bar_from_top: int,
    logo_idx: int,
    bar_percentage: float,
):
    """
    Combine a bar graph and a SINGLE file extension img.
    This gets called in a loop multiple times.

    bar_from_top is zero indexed, is the number of the bar starting from the top
    logo_idx is zero indexed, is the number of logo for a single bar
    """
    FILE_EXT_WIDTH_PAD = 20
    BAR_VERTICAL_PAD = 32

    # initialize canvas using bar graph
    canvas = Image.new("RGB", (bar_graph_img.width, bar_graph_img.height))
    canvas.paste(bar_graph_img, (0, 0))

    # resize ext image and past
    ext_img = ext_img.resize((17, 17), resample=Image.BICUBIC)

    # these are the coordinates for the first bar, first position on the left
    if bar_percentage < 0.25:
        SCALING_FACTOR = (
            25  # how far right to move the ext images so they don't overlap with bar
        )
        left_offset = 134 + int(bar_percentage * SCALING_FACTOR * FILE_EXT_WIDTH_PAD)
    else:
        left_offset = 134
    top_offset = 108

    left_offset += logo_idx * FILE_EXT_WIDTH_PAD
    top_offset += bar_from_top * BAR_VERTICAL_PAD
    canvas.paste(ext_img, (left_offset, top_offset))
    return canvas


if __name__ == "__main__":
    pass
