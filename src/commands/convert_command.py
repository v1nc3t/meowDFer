
from utils.convert import convert_all_to_pdf

def run(args):
    src = args.src
    dest = args.dest
    name = args.name
    convert_all_to_pdf(src, dest, name)

def register_command(parser):
    parser.add_argument(
        "--src",
        type=str,
        help="Source folder where folders with images are located"
    )
    parser.add_argument(
        "--dest",
        type=str,
        help="Name of folder where pdf to be created"
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Name of the book"
    )