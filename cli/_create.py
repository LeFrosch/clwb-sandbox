import argparse
import os
import sys

from ._docker import docker_get_client, docker_create_container, docker_get_container
from ._util import get_workspace_dir, container_derive_port, log, log_error
from ._info import container_print_info


def container_create(client, name, workspace_dir, clwb_dir):
    """Creates and starts a new container on stable ports derived from its name."""

    log(f"starting new container '{name}'")

    port = container_derive_port(name)

    ports = {
        '22/tcp': port,
        '3389/tcp': port + 1,
        '5991/tcp': port + 2,
        '5006/tcp': port + 3,
    }
    volumes = {
        workspace_dir: {'bind': '/config/workspace', 'mode': 'rw'},
        clwb_dir: {'bind': '/config/clwb', 'mode': 'rw'},
    }
    environment = {
        'PUID': '911' if sys.platform == 'darwin' else str(os.getuid()),
        'PGID': '911' if sys.platform == 'darwin' else str(os.getgid()),
        'TZ': 'Etc/UTC',
    }

    docker_create_container(client, name, ports, volumes, environment)


def configure(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--workspace',
        required=True,
        help='local directory or GitHub URL for the workspace',
    )
    parser.add_argument(
        '--clwb',
        required=True,
        help='local directory to the CLwB repository',
    )


def execute(args: argparse.Namespace):
    client = docker_get_client()
    workspace_dir = get_workspace_dir(args.workspace)

    if not os.path.isdir(args.clwb):
        log_error(f"CLwB directory '{args.clwb}' not found")

    clwb_dir = os.path.abspath(args.clwb)
    name = os.path.basename(workspace_dir)

    container = docker_get_container(client, name)
    if container:
        log_error(f"container '{name}' already exists")

    container_create(client, name, workspace_dir, clwb_dir)
    container_print_info(client, name)
