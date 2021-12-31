import argparse
import os

parser = argparse.ArgumentParser(description='Debug flag')
parser.add_argument('-d', '--my_debug', type=int, choices=[0, 1], help="0 : Debug off, 1 : Debug on", required=False)

# Parse and print the results
args = parser.parse_args()

if args.my_debug == 1 or os.path.isfile('test_bit'):
    os.environ["MY_DEBUG"] = "1"
else:
    os.environ["MY_DEBUG"] = "0"

DEBUG = int(os.getenv("MY_DEBUG"))

import app

app.start()

# todo: make gpio mapping dynamic by storing them in separate file
# todo: add hardware circuit instructions to README
