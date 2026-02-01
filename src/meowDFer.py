import os
import sys
import re
import argparse

from commands import extract, convert, merge

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
        description="Extract zips, converts image folders into PDFs, and combines PDFs into volume."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # extract
    extract_parser = subparsers.add_parser(
        "extract", help="Extract one or more zip files from a folder. (help: extract -h)"
    )
    extract.register_command(extract_parser)

    # convert
    convert_parser = subparsers.add_parser(
        "convert", help="Convert one or more folders with images into PDFs. (help: convert -h)"
    )
    convert.register_command(convert_parser)

    # merge
    merge_parser = subparsers.add_parser(
        "merge", help="Merge PDFs into volumes based on input. (help: merge -h)"
    )
    merge.register_command(merge_parser)

    args = parser.parse_args()

    if args.command == "extract":
        if not args.src or not args.dest:
            extract_parser.error("The --src and --dest flags are required when using -e/--extract")
        print("Running extract...")
        extract.run(args)

    elif args.command == "convert":
        if not args.src or not args.dest:
            convert_parser.error("The --src, --dest, and --name flags are required when using -c/--convert")
        print("Running convert...")
        convert.run(args)
    
    elif args.command == "merge":
        if not args.src or not args.dest:
            merge_parser.error("The --src, and--dest flags are required when using -m/--merge")
        print("Running merge...")
        merge.run(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()