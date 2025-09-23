import argparse

from ._docker import docker_get_client, docker_list_containers
from ._util import log


def configure(parser: argparse.ArgumentParser):
    pass


def execute(args: argparse.Namespace):
    client = docker_get_client()
    containers = docker_list_containers(client)

    if not containers:
        log('no bazel containers found')
        return

    print(f'{"NAME":<30} {"ID":<15} {"STATUS":<15} {"SSH PORT"}')
    print('-' * 70)

    for container in containers:
        ports = container.attrs['HostConfig']['PortBindings']
        ssh_port = 'n/a'
        if ports and '22/tcp' in ports and ports['22/tcp']:
            ssh_port = ports['22/tcp'][0]['HostPort']

        name = container.name
        short_id = container.short_id
        status = container.status

        print(f'{name:<30} {short_id:<15} {status:<15} {ssh_port}')
