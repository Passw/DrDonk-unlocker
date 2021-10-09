#!/usr/bin/env python3

import hashlib
import json
import os
import sys
from urllib.request import urlretrieve


# Build some constants
ROOT = os.path.dirname(os.path.abspath(__file__))
TOOL_PATH = os.path.join(ROOT, 'tools')
LOCAL_ZIP = os.path.join(TOOL_PATH, 'assets.zip')
LOCAL_JSON = os.path.join(TOOL_PATH, 'assets.json')
TEMP_JSON = os.path.join(TOOL_PATH, 'temp.json')
ASSETS_JSON  = 'https://raw.githubusercontent.com/DrDonk/patchersupportpkg/main/assets/assets.json'
ASSETS_ZIP  = 'https://raw.githubusercontent.com/DrDonk/patchersupportpkg/main/assets/assets.zip'


def main():
    # Check minimal Python version is 3.8
    if sys.version_info < (3, 8):
        sys.stderr.write('You need Python 3.8 or later\n')
        sys.exit(1)

    # Make a tools folder if not present
    if not os.path.exists(TOOL_PATH):
        os.makedirs(TOOL_PATH)

    # Get the assets.json file
    urlretrieve(ASSETS_JSON, TEMP_JSON)
    with open(TEMP_JSON) as f:
        new_data = json.load(f)
    with open(LOCAL_JSON) as f:
        old_data = json.load(f)

    if old_data['build'] != new_data['build']:
        # Download the assets.zip file
        urlretrieve(ASSETS_ZIP, LOCAL_ZIP)
        with open(LOCAL_ZIP, 'rb') as f:
            data = f.read()  # read entire file as bytes
            readable_hash = hashlib.sha256(data).hexdigest();
            print(readable_hash)
        os.remove(LOCAL_JSON)
        os.rename(TEMP_JSON, LOCAL_JSON)

    return


if __name__ == '__main__':
    main()
