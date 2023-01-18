import os
from typing import Dict, Optional
import sys

import yaml

# yikes
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "birdbot", "config")))
from config.paths import PATHS


class BirdConfig:
    def __init__(self, sts_secrets: Optional[Dict[str, str]] = None):
        if os.path.exists(PATHS["BIRD_CONFIG_FILE"]):
            print("BirdConfig loading secrets from local")
            self.exists = True
            self.bird_config = yaml.safe_load(open(PATHS["BIRD_CONFIG_FILE"]))
            self.consumer_key = self.bird_config["CONSUMER_KEY"]
            self.consumer_secret = self.bird_config["CONSUMER_SECRET"]
            self.access_key = self.bird_config["ACCESS_KEY"]
            self.access_secret = self.bird_config["ACCESS_SECRET"]
        elif sts_secrets is not None:
            print("BirdConfig loading secrets from SecretsManager")
            self.bird_config = None
            self.consumer_key = sts_secrets["CONSUMER_KEY"]
            self.consumer_secret = sts_secrets["CONSUMER_SECRET"]
            self.access_key = sts_secrets["ACCESS_KEY"]
            self.access_secret = sts_secrets["ACCESS_SECRET"]
            self.exists = True
        else:
            self.bird_config = None
            self.consumer_key = None
            self.consumer_secret = None
            self.access_key = None
            self.access_secret = None
            self.exists = False
            print(
                f"BirdConfig: no local environment config and no AWS SecretManager secrets found, something is off"
            )
