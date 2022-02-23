import json


class TestlinkConfig:
    def __init__(self):
        with open("config.json") as config:
            data = json.load(config)
        # 1 + 2) Read URL's from config file
        self.tl_api_url = data["TL_API_URL"]
        self.tl_base_url = data["TL_BASE_URL"]

        # 3) The Repository should have a "devkey"-file that contains the API token for Testlink as text
        #    needed for authentication, obviously
        with open("devkey") as devkey_file:
            data = devkey_file.read()

        # 4) API-Key
        self.dev_key = data

        # 5) Get rid of reference to file
        del data
