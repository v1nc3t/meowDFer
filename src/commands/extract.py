
from utils.utils_zips import extract_zips

def run(args):
    src = args.src
    dest = args.dest
    extract_zips(src, dest)

def register_command(parser):
    # use a flag to extract 
    parser.add_argument(
        "-e", "--extract",
        action="store_true",
        help="Extract zip files from folder into destination folder"
    )
    parser.add_argument(
        "--src",
        type=str,
        help="Source folder where zips are located"
    )
    parser.add_argument(
        "--dest",
        type=str,
        help="Name of folder where zips to be extracted in"
    )