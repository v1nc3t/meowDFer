# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os
import sys
import argparse

from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.traceback import install
from src.commands.extract import extract_zips
from src.commands.convert import convert_pdf
from src.commands.merge import merge_pdf

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

install(show_locals=True)

def initiate():
    parser = argparse.ArgumentParser(
        prog="meowDFer",
        description="A tool to convert image folders to PDFs."
    )

    # action flags (required: must pick one)
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("-e", "--extract", action="store_true", help="extract zip files.")
    action_group.add_argument("-c", "--convert", action="store_true", help="convert image folders to PDFs.")
    action_group.add_argument("-m", "--merge", action="store_true", help="merge PDFs based on vols.txt.")
    action_group.add_argument("-a", "--all", action="store_true", help="full pipeline: extract -> convert -> merge.")
    action_group.add_argument("-cm", "--convert-merge", action="store_true", help="half pipeline: convert -> merge.")

    # data flags 
    parser.add_argument("-s", "--src", required=True, help="source path (directory)")
    parser.add_argument("-d", "--dest", required=True, help="destination directory (if not exists will be created).")  
    parser.add_argument("-v", "--vols", help="path to vols.txt (Required for merge, all, convert-merge).")
    parser.add_argument("-n", "--name", help="optinal name output (files named differently than dest name).")

    args = parser.parse_args()

    if (args.merge or args.all or args.convert_merge) and not args.vols:
        parser.error("the --vols/-v argument is required when running merge, all, or convert-merge.")

    return args

banner = r"""[purple]
                                                 /$$$$$$$  /$$$$$$$$                 
                                                | $$__  $$| $$_____/                 
 /$$$$$$/$$$$   /$$$$$$   /$$$$$$  /$$  /$$  /$$| $$  \ $$| $$     /$$$$$$   /$$$$$$ 
| $$_  $$_  $$ /$$__  $$ /$$__  $$| $$ | $$ | $$| $$  | $$| $$$$$ /$$__  $$ /$$__  $$
| $$ \ $$ \ $$| $$$$$$$$| $$  \ $$| $$ | $$ | $$| $$  | $$| $$__/| $$$$$$$$| $$  \__/
| $$ | $$ | $$| $$_____/| $$  | $$| $$ | $$ | $$| $$  | $$| $$   | $$_____/| $$      
| $$ | $$ | $$|  $$$$$$$|  $$$$$$/|  $$$$$/$$$$/| $$$$$$$/| $$   |  $$$$$$$| $$      
|__/ |__/ |__/ \_______/ \______/  \_____/\___/ |_______/ |__/    \_______/|__/      


                                                                by v1c3nt                                                                                                                             
[/purple]"""


def handle_extract(src, dest):
    extract_zips.run(src, dest)

def handle_convert(src, dest, name):
    final_name = name if name else os.path.basename(dest)
    convert_pdf.run(src, dest, final_name)

def handle_merge(src, dest, vols, name):
    final_name = name if name else os.path.basename(dest)
    merge_pdf.run(src, dest, vols, final_name)

def main():
    args = initiate()    

    console = Console()
    console.print(banner)

    if args.extract:
        with console.status("[bold green]Processing...", spinner="dots"):
            handle_extract(args.src, args.dest)
    
    elif args.convert:
        with console.status("[bold green]Processing...", spinner="dots"):
            handle_convert(args.src, args.dest, args.name)

    elif args.merge:
        with console.status("[bold green]Processing...", spinner="dots"):
            handle_merge(args.src, args.dest, args.vols, args.name)
    
    elif args.convert_merge:
        with console.status("[bold green]Processing...", spinner="dots"):
            handle_extract(args.src, args.dest)
            handle_convert(args.src, args.dest, args.name)

    elif args.all:
        with console.status("[bold green]Processing...", spinner="dots"):
            handle_extract(args.src, args.dest)
            handle_convert(args.src, args.dest, args.name)
            handle_merge(args.src, args.dest, args.vols, args.name)


if __name__ == "__main__":
    main()