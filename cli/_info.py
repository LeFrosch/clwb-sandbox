import argparse

from ._docker import docker_get_client, docker_get_container
from ._util import log, log_error, container_derive_port


def container_print_info(client, name):
    container = docker_get_container(client, name)

    if not container:
        log_error(f"container '{name}' not found")
        return

    port = container_derive_port(name)

    log(f"Details for container '{container.name}':")
    print(f'  ID:         {container.short_id}')
    print(f'  Status:     {container.status}')
    print(f'  Image:      {container.image.tags[0] if container.image.tags else "n/a"}')
    print(f'  Created:    {container.attrs["Created"]}')
    print('')
    log('Ports:')
    print(f'  SSH:        ssh abc@localhost -p {port}')
    print(f'  RDP:        rdp://abc@localhost:{port + 1}')
    print(f'  IntelliJ:   {port + 2}')
    print(f'  Agentlib:   {port + 3}')
    print('')

    mounts = container.attrs['Mounts']
    if mounts:
        log('Mounts:')
        for mount in mounts:
            print(f'  - {mount["Source"]} -> {mount["Destination"]}')


def configure(parser: argparse.ArgumentParser):
    parser.add_argument('name', help='name or ID of the container')


def execute(args: argparse.Namespace):
    client = docker_get_client()
    container_print_info(client, args.name)
