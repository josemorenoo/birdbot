import os

if os.getcwd().endswith("birdbot"):
    prefix = ""
else:
    prefix = "birdbot/"

cwd = os.getcwd()

PATHS = dict(
    BIRD_CONFIG_FILE=os.path.abspath(
        os.path.join(cwd, f"{prefix}config/local_bird_config.json")
    ),
)

if os.getcwd().endswith("scraper-infra"):
    PATHS = dict(BIRD_CONFIG_FILE="birdbot/config/local_bird_config.json")
    print(
        f"invoked from scraper-infra, setting local config file to {PATHS['BIRD_CONFIG_FILE']}"
    )
