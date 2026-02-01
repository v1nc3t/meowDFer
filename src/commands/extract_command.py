
from utils.extract import extract_zips

def run(args):
    src = args.src
    dest = args.dest
    extract_zips(src, dest)

def register_command(parser):
    parser.add_argument(
        "--src",
        type=str,
        help="Source folder where zips are located"
    )
    parser.add_argument(
        "--dest",
        type=str,
        help="Name of folder where zips to be extracted"
    )