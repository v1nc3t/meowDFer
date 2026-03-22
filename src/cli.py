import argparse

from .commands import (
    convert_command,
    merge_command, 
    all_command, 
    cm_command
)

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

    # convert
    convert_parser = subparsers.add_parser(
        "convert", help="Convert one or more folders with images into PDFs. (help: convert -h)"
    )
    convert_command.register_command(convert_parser)

    # merge
    merge_parser = subparsers.add_parser(
        "merge", help="Merge PDFs into volumes based on input. (help: merge -h)"
    )
    merge_command.register_command(merge_parser)

    # all in one command
    all_parser = subparsers.add_parser(
        "all", help="Extract, convert and merge all at once. (help: all -h)"
    )
    all_command.register_command(all_parser)

    # covert and merge command
    all_parser = subparsers.add_parser(
        "cm", help="Convert and merge at once. (help: cm -h)"   
    )
    cm_command.register_command(all_parser)
    

    args = parser.parse_args()
    
    # extract zips
    # convert folders to PDFs
    if args.command == "convert":
        if not args.src or not args.dest:
            convert_parser.error("The --src and --dest flags are required when using convert")
        
        convert_command.run(args)

    # merge PDFs into volumes
    elif args.command == "merge":
        if not args.src or not args.dest:
            merge_parser.error("The --src, --dest, and --vols flags are required when using merge")
        
        merge_command.run(args)

    # run all three: extract, convert, and merge one after another 
    elif args.command == "all":
        if not args.src or not args.dest:
            merge_parser.error("The --src, --dest, and --vols flags are required when using all")

        all_command.run(args)

    # run convert and merge one after another
    elif args.command == "cm":
        if not args.src or not args.dest:
            merge_parser.error("The --src, --dest, and --vols flags are required when using cm")

        cm_command.run(args)
    
    else:
        parser.print_help()