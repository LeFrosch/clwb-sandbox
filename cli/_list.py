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

    log('bazel containers:')
    for container in containers:
        ports = container.attrs['HostConfig']['PortBindings']
        ssh_port = 'n/a'
        if ports and '22/tcp' in ports and ports['22/tcp']:
            ssh_port = ports['22/tcp'][0]['HostPort']

        print(f'  name: {container.name}')
        print(f'    ID: {container.short_id}')
        print(f'    status: {container.status}')
        print(f'    SSH port: {ssh_port}')
        print('-' * 20)
