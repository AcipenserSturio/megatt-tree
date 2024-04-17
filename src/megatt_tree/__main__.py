import argparse

from .convert import convert


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="megatt-tree",
        description="Converts trees from timetree-of-life/MEGA-TT to nicer formats.",
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--convert",
        help="Converts .nwk tree to csv",
        action="store_true",
    )
    action.add_argument(
        "--leaves",
        help="Provides a list of branches for given leaves",
        action="store_true",
    )

    args = parser.parse_args()

    if args.convert:
        convert()
    else:
        print(args)
