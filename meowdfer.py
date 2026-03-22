import os
import sys
import argparse

from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.traceback import install
# from src.commands import convert_command, extract_command, merge_command
from src.commands.extract import extract_zips
from src.commands.convert import convert_pdf
from src.commands.merge import merge_pdf
from src.commands.all import extract_convert_merge

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

install(show_locals=True)

def initiate():
    custom_usage = "meowdfer [-h] [-e SRC DEST] [-c SRC DEST [NAME]] [-m SRC DEST [NAME]] [-a SRC DEST [NAME]] [-cm SRC DEST [NAME]]"

    parser = argparse.ArgumentParser(
        prog="meowdfer",
        usage=custom_usage,
        description="A tool to convert image folders to PDFs."
    )

    parser.add_argument(
        "-e",
        "--extract",
        nargs=2,
        metavar=("SRC", "DEST"),
        help="Extracts zip files. Requires [src] and [dest]." 
    )

    parser.add_argument(
        "-c",
        "--convert",
        nargs="+",
        metavar=("SRC DEST", "NAME"),
        help="Converts folders with images int pdfs. Requires [src] and [dest]. Optional [NAME]."
    )

    parser.add_argument(
        "-m",
        "--merge",
        nargs="+",
        metavar=("SRC DEST VOLS", "NAME"),
        help="Merge PDFs based on vols.txt . Requires [src], [dest], [vols]. Optional [NAME]."
    )

    parser.add_argument(
        "-a",
        "--all",
        nargs="+",
        metavar=("SRC DEST VOLS", "NAME"),
        help="Extract, convert and merge one after another. Requires [src] and [dest]. Optional [NAME]."
    )

    parser.add_argument(
        "-cm",
        "--convert-merge",
        nargs="+",
        metavar=("SRC DEST VOLS", "NAME"),
        help="Convert and merge one after another. Requires [src] and [dest]. Optional [NAME]."
    )

    return parser.parse_args()

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

if __name__ == "__main__":
    args = initiate()

    console = Console()
    console.print(banner)
    
    if args.extract:
        if len(args.extract) == 2:
            extract_zips.run(args.extract[0], args.extract[1])
        else:
            console.print("[red]error: --extract requires at least a source and destination path.[/red]")

    elif args.convert:
        if len(args.convert) == 2:
            convert_pdf.run(args.convert[0], args.convert[1], name=args.convert[1])
        else: 
            console.print("[red]error: --convert requires at least a source and destination path.[/red]")

    elif args.merge:
        if len(args.merge) == 3:
            merge_pdf.run(args.merge[0], args.merge[1], args.merge[2], name=args.merge[1])
        else:
            console.print("[red]error: --merge requires at least a source, destination, and volume-intervals path.[/red]")

    elif args.all:
        if len(args.all) == 3:
            extract_convert_merge.run(args.merge[0], args.merge[1], args.merge[2], name=args.merge[1])
        else:
            console.print("[red]error: --all requires at least a source, destination, and volume-intervals path.[/red]")