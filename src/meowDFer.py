import os
import sys
import re
import argparse

from commands import extract


logo = r"""
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  meowDFer
"""


def extract_chapter_number(file_name):
    return

def file_to_pdf(file_name):
    return

def convert_all_pdf(src, dest, name):
    return

def combine_volume(src, dest, name):
    return


def main():
    print(logo)

    parser = argparse.ArgumentParser(
        prog="meowDFer",
        description="Extract zips, converts image folders into PDFs, and combines PDFs into volume"
    )

    extract.register_command(parser)

    args = parser.parse_args()

    if args.extract:
        if not args.src or not args.dest:
            parser.error("The --src and --dest flags are required when using -e/--extract")
        extract.run(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()