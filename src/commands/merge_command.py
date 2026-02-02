
from utils.merge import merge_to_volumes

def run(args, name):
    src = args.src
    dest = args.dest
    vals = args.vals
    merge_to_volumes(src, dest, vals, name)

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
        "--vals",
        type=str,
        help="Name of .txt where intervals for volums are located (include and chapter number separated by commas)"
    )