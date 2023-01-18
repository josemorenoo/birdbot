import os

if os.getcwd().endswith("birdbot"):
    prefix = ""
else:
    prefix = "birdbot/"

cwd = os.getcwd()

PATHS = dict(
    BIRD_CONFIG_FILE=os.path.abspath(
        os.path.join(cwd, f"{prefix}config/local_bird_config.yaml")
    ),
)
