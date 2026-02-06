
from ..utils.merge import merge_to_volumes

def run(args):
    src = args.src
    dest = args.dest
    vols = args.vols
    name = args.dest

    merge_to_volumes(src, dest, vols, name)

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
        "--vols",
        type=str,
        help="Name of .txt where intervals for volums are located (include and chapter number separated by commas)"
    )