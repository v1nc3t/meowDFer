import tempfile
import os

from utils.extract import extract_zips
from utils.convert import convert_all_to_pdf
from utils.merge import merge_to_volumes

def run(args, name):
    src = args.src
    dest = args.dest
    vols = args.vols

    with tempfile.TemporaryDirectory() as tmp_extracted:
        extract_zips(src, tmp_extracted)

        with tempfile.TemporaryDirectory() as temp_converted:
            convert_all_to_pdf(tmp_extracted, temp_converted, name)

            merge_to_volumes(temp_converted, dest, vols, name)


def register_command(parser):
    parser.add_argument(
        "--src",
        type=str,
        help="Source folder where zip files are located"
    )
    parser.add_argument(
        "--dest",
        type=str,
        help="Name of folder where final volume are located"
    )
    parser.add_argument(
        "--vols",
        type=str,
        help="Name of .txt where intervals for volums are located (include and chapter number separated by commas)"
    )