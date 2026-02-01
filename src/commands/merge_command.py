
from utils.merge import merge_to_volumes

def run(args):
    src = args.src
    dest = args.dest
    name = args.name
    merge_to_volumes(src, dest, name)

def register_command(parser):
    parser.add_argument(
        "--src",
        type=str,
        help="Source folder where PDFs are located"
    )
    parser.add_argument(
        "--dest",
        type=str,
        help="Name of destination folder where volumes are to be created"
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Name of the book"
    )