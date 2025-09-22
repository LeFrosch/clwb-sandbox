import docker
from ._util import log_error

IMAGE_NAME = 'clwb-sandbox'
CONTAINER_PREFIX = 'clwb-'


def docker_get_client():
    try:
        return docker.from_env()
    except docker.errors.DockerException:
        log_error('Docker is not running, please start Docker and try again')


def docker_create_container(client, name, ports, volumes, environment=None):
    try:
        return client.containers.run(
            IMAGE_NAME,
            detach=True,
            name=CONTAINER_PREFIX + name,
            ports=ports,
            volumes=volumes,
            environment=environment,
            security_opt=['seccomp=unconfined'],
        )
    except docker.errors.APIError as e:
        log_error(f"failed to create container '{name}': {e}")


def docker_get_container(client, name):
    if not name.startswith(CONTAINER_PREFIX):
        name = CONTAINER_PREFIX + name

    try:
        return client.containers.get(name)
    except docker.errors.NotFound:
        return None


def docker_list_containers(client, all=True, filters=None):
    return client.containers.list(all=all, filters={'ancestor': IMAGE_NAME})


def docker_remove_container(container, force=False):
    try:
        container.remove(force=force)
    except docker.errors.APIError as e:
        log_error(f"failed to remove container '{container.name}': {e}")


def docker_stop_container(container):
    try:
        container.stop()
    except docker.errors.APIError as e:
        log_error(f"failed to stop container '{container.name}': {e}")


def docker_start_container(container):
    try:
        container.start()
    except docker.errors.APIError as e:
        log_error(f"failed to start container '{container.name}': {e}")
