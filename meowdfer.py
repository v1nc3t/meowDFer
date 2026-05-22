#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os
import sys
import argparse

_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_ROOT, "src"))

from rich.console import Console
from rich.traceback import install
from src.commands.extract import extract_zips
from src.commands.convert import convert_pdf
from src.commands.merge import merge_pdf
from src.commands.convert_merge import convert_merge
from src.commands.all import extract_convert_merge
from src.commands.scrape import scrape_volumes

install(show_locals=True)

def initiate():
    parser = argparse.ArgumentParser(
        prog="meowDFer",
        description="A tool to convert image folders to PDFs."
    )

    # action flags (required: must pick one)
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("-e", "--extract", nargs=2, metavar=("SRC", "DEST"), help="extract zip files.")
    action_group.add_argument("-c", "--convert", nargs=2, metavar=("SRC", "DEST"), help="convert image folders to PDFs.")
    action_group.add_argument("-m", "--merge", nargs=2, metavar=("SRC", "DEST"), help="merge PDFs based on a file with volume intervals (requires -f/--file).")
    action_group.add_argument("-a", "--all", nargs=2, metavar=("SRC", "DEST"), help="full pipeline: extract -> convert -> merge.")
    action_group.add_argument("-cm", "--convert-merge", nargs=2, metavar=("SRC", "DEST"), help="half pipeline: convert -> merge.")
    action_group.add_argument("-sc", "--scrape", nargs=2, metavar=("URL", "DEST"), help="scrape site of given url, finding the chapters intervals of a manga.")

    # data flags  
    parser.add_argument("-t", "--type", choices=["chapter", "volume"], help="processing mode: specify whether to convert by chapter or volume. (Required for convert, convert-merge, all)")
    parser.add_argument("-f", "--file", metavar="FILE", help="name of file with intervals for volumes (Required for merge, all, convert-merge).")
    parser.add_argument("-n", "--name", metavar="NAME", help="optional name output (files named differently than dest name).")
    parser.add_argument("-s", "--skip", action="store_true", help="on error during processing, log continue to the next item instead of aborting.")
    parser.add_argument("-d","--decimal", action="store_true", help="allows processing of decimal chapters.")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose/detailed output.")

    args = parser.parse_args()

    convert_actions = [args.convert, args.convert_merge, args.all]
    if any(convert_actions) and not args.type:
        parser.error("the --type argument (chapter or volume) is required when running convert, convert-merge, or all.")

    merge_actions = [args.merge or args.all or args.convert_merge]
    if any(merge_actions) and not args.file:
        parser.error("the --file/-f argument is required when running merge, convert-merge, or all.")

    if args.file and not os.path.isfile(args.file):
        parser.error(f"The file '{args.file}' does not exist.")

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

def main():
    args = initiate()    

    console = Console()
    console.print(banner)

    def _finish(ok: bool, ok_msg: str, fail_msg: str) -> None:
        if ok:
            console.print(f"[bold green]{ok_msg}[/bold green]")
        else:
            console.print(f"[bold red]{fail_msg}[/bold red]")
            sys.exit(1)

    if args.extract:
        src, dest = args.extract
        to_skip = args.skip

        console.print("[bold green]Extract: started[/bold green]")

        with console.status("[bold green]Extracting...", spinner="dots"):
            ok = extract_zips.run(src, dest, to_skip=to_skip, console=console)
        
        _finish(ok, "Extract completed!", "Extract failed: destination was not updated.")

    elif args.convert:
        src, dest = args.convert
        to_skip = args.skip
        folder_type = args.type
        allow_decimal = args.decimal

        console.print("[bold green]Convert: started[/bold green]")

        with console.status("[bold green]Converting...", spinner="dots"):
            final_name = args.name if args.name else os.path.basename(dest.rstrip(os.sep))
            ok = convert_pdf.run(src, dest, final_name, folder_type, allow_decimal=allow_decimal, to_skip=to_skip ,console=console)
        
        _finish(ok, "Convert completed!", "Convert failed: destination was not updated.")

    elif args.merge:
        src, dest = args.merge
        to_skip = args.skip
        allow_decimal = args.decimal

        console.print("[bold green]Merge: started[/bold green]")

        with console.status("[bold green]Merging...", spinner="dots"):
            final_name = args.name if args.name else os.path.basename(dest.rstrip(os.sep))
            ok = merge_pdf.run(src, dest, args.file, final_name, allow_decimal=allow_decimal, to_skip=to_skip,console=console)
        
        _finish(ok, "Merge completed!", "Merge failed: destination was not updated.")

    elif args.convert_merge:
        src, dest = args.convert_merge
        to_skip = args.skip
        folder_type = args.type
        allow_decimal = args.decimal

        console.print("[bold green]CM pipeline (Convert -> Merge): started[/bold green]")

        with console.status("[bold green]Pipeline...", spinner="dots"):
            final_name = args.name if args.name else os.path.basename(dest.rstrip(os.sep))
            ok = convert_merge.run(src, dest, args.file, final_name, folder_type, allow_decimal=allow_decimal, to_skip=to_skip, console=console)
            
        _finish(
            ok,
            "CM pipeline (Convert -> Merge): completed!",
            "CM pipeline (Convert -> Merge) failed: destination was not updated.",
        )

    elif args.all:
        src, dest = args.all
        to_skip = args.skip
        folder_type = args.type
        allow_decimal = args.decimal

        console.print("[bold green]All pipeline (Extract -> Convert -> Merge): started[/bold green]")

        with console.status("[bold green]Pipeline...", spinner="dots"):
            final_name = args.name if args.name else os.path.basename(dest.rstrip(os.sep))
            ok = extract_convert_merge.run(src, dest, args.file, final_name, folder_type, allow_decimal=allow_decimal, to_skip=to_skip, console=console)

        _finish(
            ok,
            "All pipeline (Extract -> Convert -> Merge): completed!",
            "All pipeline (Extract -> Convert -> Merge) failed: destination was not updated.",
        )
    
    elif args.scrape: 
        url, dest = args.scrape

        console.print(f"[bold green]Scraping: started[/bold green]")

        if args.verbose:
            ok = scrape_volumes.run(url, dest, verbose=True, console=console)
        else:
            ok = scrape_volumes.run(url, dest, verbose=False, console=console)
        
        _finish(
            ok,
            "Scraping: completed!",
            "Scraping failed: destination was not updated.",
        )


if __name__ == "__main__":
    main()