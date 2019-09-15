'''
Main entry point for the program, used to centralise the spec file and the
settings for the loggers.

Usage python main.py file_fw file_ad
file_fw: file to save fixed width sample in.
file_ad: file to save ASCII delimited translation of above file in.
'''
from src.spec import spec
from src.app import app
import logging
import sys

logging.basicConfig(level=logging.WARNING)

if __name__ == '__main__':
    file_fw = sys.argv[1]
    file_ad = sys.argv[2]
    random = sys.argv[3]
    # TODO Fix the cl arguments using argparse.
    app(spec, file_fw, file_ad, random)
