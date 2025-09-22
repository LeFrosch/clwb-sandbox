import argparse
import os

from ._docker import docker_get_client, docker_create_container, docker_get_container
from ._util import get_workspace_dir, container_derive_port, log, log_error


def create_container(client, name, workspace_dir, clwb_dir):
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
    environment = {  # todo, in practice this should be retrived from `id $(whoami)`
        'PUID': '1000',
        'PGID': '1000',
        'TZ': 'Etc/UTC',
    }

    docker_create_container(client, name, ports, volumes, environment)


def print_container_info(client, name):
    container = docker_get_container(client, name)

    if container:
        port = container_derive_port(name)
        log(f'Docker container running: {container.short_id}')
        log(f'-> connect with ssh: ssh abc@localhost -p {port}')
        log(f'-> connect with rdp: rdp://abc@localhost:{port + 1}')
        log(f'-> intellij backend port: {port + 2}')
        log(f'-> agentlib debug port: {port + 3}')
    else:
        log(f"container '{name}' does not appear to be running")


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
    parser.add_argument(
        '--recreate',
        action='store_true',
        help='remove and recreate the container if it already exists',
    )


def execute(args: argparse.Namespace):
    client = docker_get_client()
    workspace_dir = get_workspace_dir(args.workspace)

    if not os.path.isdir(args.clwb):
        log_error(f"CLwB directory '{args.clwb}' not found")

    clwb_dir = os.path.abspath(args.clwb)
    container_name = os.path.basename(workspace_dir)

    container = docker_get_container(client, container_name)
    if container:
        log_error(f"container '{container_name}' already exists")

    create_container(client, container_name, workspace_dir, clwb_dir)
    print_container_info(client, container_name)
