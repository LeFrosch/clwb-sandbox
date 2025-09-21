import argparse

from . import (
    _create as create,
    _stop as stop,
    _start as start,
    _list as list,
    _remove as remove,
)

from .__about__ import __version__, __description__


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
    )

    commands = parser.add_subparsers(
        required=True,
        help='available subcommands',
    )

    create_parser = commands.add_parser(
        'create',
        help='create a new container',
    )
    create_parser.set_defaults(execute=create.execute)
    create.configure(create_parser)

    stop_parser = commands.add_parser(
        'stop',
        help='stop a running container',
    )
    stop_parser.set_defaults(execute=stop.execute)
    stop.configure(stop_parser)

    start_parser = commands.add_parser(
        'start',
        help='start a stopped container',
    )
    start_parser.set_defaults(execute=start.execute)
    start.configure(start_parser)

    list_parser = commands.add_parser(
        'list',
        help='list all containers',
    )
    list_parser.set_defaults(execute=list.execute)
    list.configure(list_parser)

    remove_parser = commands.add_parser(
        'remove',
        help='remove a stopped container',
    )
    remove_parser.set_defaults(execute=remove.execute)
    remove.configure(remove_parser)

    return parser.parse_args()


def main():
    args = parse_arguments()
    args.execute(args)
