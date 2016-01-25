#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from homehubdb.model.photo import *
import datetime
import argparse
import re

FORMAT='jpeg'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filename', help='file to write to'
                    , required = False)

    # Connect to databases and crawler on GCE instance
    args = ap.parse_args()
    filename = "test." + FORMAT
    if args.filename:
        filename = args.filename

    c = Camera()
    c.capture(filename)



if __name__ == "__main__":
    __main__()

