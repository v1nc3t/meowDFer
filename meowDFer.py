import os
import sys
import re
import argparse


logo = r"""
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  meowDFer
"""


def extract_zips(src, dest):
    return

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
    subparsers = parser.add_subparsers(dest="commands", required=True) 

    name = input("Enter name: ")

    print(name)


if __name__ == "__main__":
    main()