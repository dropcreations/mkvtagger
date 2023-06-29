import os
import argparse

from core import MKVTagger
    
def main():
    parser = argparse.ArgumentParser(
        description="Tag MKV/WebM files with OFFICIAL or UNOFFICIAL tags with multiple tag value support."
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='mkvtagger v1.0.0'
    )
    parser.add_argument(
        "-m",
        "--multi",
        dest="multi",
        action="store_true",
        help="Use multiple tag values"
    )
    parser.add_argument(
        "-t",
        "--tags",
        dest="tags",
        default=None,
        type=str,
        help="Add tags from a text file"
    )
    parser.add_argument(
        "--no-encoded-date",
        dest="enc_date",
        action="store_true",
        help="Remove encoded date"
    )
    parser.add_argument(
        "--no-writing-application",
        dest="wrt_app",
        action="store_true",
        help="Remove writing application"
    )
    parser.add_argument(
        "--no-writing-library",
        dest="wrt_lib",
        action="store_true",
        help="Remove writing library"
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=str,
        help="Add input files or folders"
    )
    args = parser.parse_args()
    
    tagger = MKVTagger(args.inputs)
    tagger.process(
        args.tags,
        args.multi,
        args.enc_date,
        args.wrt_app,
        args.wrt_lib
    )

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()