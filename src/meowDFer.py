import os
import sys
import re
import argparse

from commands import extract, convert


logo = r"""
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  meowDFer
"""

def main():
    print(logo)

    parser = argparse.ArgumentParser(
        prog="meowDFer",
        description="Extract zips, converts image folders into PDFs, and combines PDFs into volume"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser(
        "extract", help="Extract one or more zip files from a folder"
    )
    extract.register_command(extract_parser)

    convert_parser = subparsers.add_parser(
        "convert", help="Converts one or more folders with images into PDFs"
    )
    convert.register_command(convert_parser)

    args = parser.parse_args()

    if args.command == "extract":
        if not args.src or not args.dest:
            parser.error("The --src and --dest flags are required when using -e/--extract")
        extract.run(args)

    elif args.command == "convert":
        if not args.src or not args.dest:
            parser.error("The --src and --dest flags are required when using -c/--convert")
        convert.run(args)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()