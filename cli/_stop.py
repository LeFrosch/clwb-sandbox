import argparse

from ._docker import docker_get_client, docker_get_container, docker_stop_container
from ._util import log, log_error


def configure(parser: argparse.ArgumentParser):
    parser.add_argument('name', help='name or ID of the container to stop')


def execute(args: argparse.Namespace):
    client = docker_get_client()
    container = docker_get_container(client, args.name)

    if not container:
        log_error(f"container '{args.name}' not found")
        return

    if container.status != 'running':
        log(f"container '{container.name}' is not running")
        return

    docker_stop_container(container)
    log(f"container '{container.name}' stopped successfully")
