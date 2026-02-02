import sys
import argparse

from commands import convert_command, extract_command, merge_command, all_command

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
    extract_command.register_command(extract_parser)

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

    args = parser.parse_args()

    if args.command == "extract":
        if not args.src or not args.dest:
            extract_parser.error("The --src and --dest flags are required when using extract")
        print("Running extract...\n")
        extract_command.run(args)

    elif args.command == "convert":
        if not args.src or not args.dest:
            convert_parser.error("The --src and --dest flags are required when using convert")
        
        name = input("Give name: ")
        print("Running convert...\n")
        convert_command.run(args, name)
    
    elif args.command == "merge":
        if not args.src or not args.dest:
            merge_parser.error("The --src, --dest, and --vols flags are required when using merge")
        
        name = input("Give name: ")
        print("Running merge...\n")
        merge_command.run(args, name)

    elif args.command == "all":
        if not args.src or not args.dest:
            merge_parser.error("The --src, --dest, and --vols flags are required when using all")

        name = input("Give name: ")
        print("Running all...")
        all_command.run(args, name)


    else:
        parser.print_help()


if __name__ == "__main__":
    main()