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
TEMP_ZIP = os.path.join(TOOL_PATH, 'temp.zip')

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
    # Download the assets.zip file
    urlretrieve(ASSETS_ZIP, TEMP_ZIP)

    # Get the data for current and downloaded zip
    with open(TEMP_JSON) as f:
        new_data = json.load(f)
    with open(LOCAL_JSON) as f:
        old_data = json.load(f)

    # Check that we have a new build
    if old_data['build'] != new_data['build']:
        # Check we downloaded OK by using SHA256 checksum
        with open(TEMP_ZIP, 'rb') as f:
            data = f.read()  # read entire file as bytes
            new_hash = hashlib.sha256(data).hexdigest()

        # Replace json and zip file if hash is OK
        if new_hash == new_data['sha256']:
            print(f'Successfully downloaded build {new_data["build"]}')
            if os.path.exists(LOCAL_JSON):
                os.remove(LOCAL_JSON)
            os.rename(TEMP_JSON, LOCAL_JSON)
            if os.path.exists(LOCAL_ZIP):
                os.remove(LOCAL_ZIP)
            os.rename(TEMP_ZIP, LOCAL_ZIP)
        else:
            print(f'Download of build {new_data["build"]} failed checksoums do not match:')
            print(f'Expected: {new_data["sha256"]}')
            print(f'Actual:   {new_hash}')
            os.remove(TEMP_JSON)
            os.remove(TEMP_ZIP)

    return


if __name__ == '__main__':
    main()
