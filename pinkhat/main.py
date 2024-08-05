from argparse import ArgumentParser
from pinkhat.iacparsers.core_scanning import CoreScanning


PINKHAT_VERSION = "1.0.0"


def initialize_command_line() -> ArgumentParser:
    parser = ArgumentParser(
        prog="pinkhat",
        usage="%(prog)s [OPTION] [DIRECTORY]...",
        description=f"""
        pinkhat {PINKHAT_VERSION}

        Application executes defined policy checks on the given directory path
        """,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog} {PINKHAT_VERSION}",
    )
    parser.add_argument(
        "files", nargs="*", help="file directory/directories or file/files", type=str
    )
    return parser


def start_processing_data(paths: str | list[str]):
    core = CoreScanning()
    if str == type(paths):
        paths = [paths]
    for path in paths:
        core.start_scanning(path=path)
    print(core.get_vulnerabilities_dict())


def main() -> None:
    parser = initialize_command_line()
    args = parser.parse_args()
    if args.files:
        start_processing_data(paths=args.files)


if __name__ == "__main__":
    main()
