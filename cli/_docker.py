import docker
from ._util import log_error

IMAGE_NAME = 'clwb-sandbox'
CONTAINER_PREFIX = 'clwb-'


def docker_get_client():
    """Returns a Docker client, or exits if Docker is not running."""
    try:
        return docker.from_env()
    except docker.errors.DockerException:
        log_error('Docker is not running, please start Docker and try again')


def docker_create_container(client, name, ports, volumes, environment=None):
    """Creates and runs a new sandbox container."""
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
    """Finds a sandbox container by name or ID."""
    # try ID or full name first
    try:
        return client.containers.get(name)
    except docker.errors.NotFound:
        pass  # Not found, continue

    # if not found, and it's not a full name, try with prefix
    if not name.startswith(CONTAINER_PREFIX):
        try:
            return client.containers.get(CONTAINER_PREFIX + name)
        except docker.errors.NotFound:
            pass  # Not found with prefix either

    # if we are here, container is not found
    return None


def docker_list_containers(client, all=True, filters=None):
    """Returns a list of all sandbox containers."""
    return client.containers.list(all=all, filters={'ancestor': IMAGE_NAME})


def docker_remove_container(container, force=False):
    """Removes the given container."""
    try:
        container.remove(force=force)
    except docker.errors.APIError as e:
        log_error(f"failed to remove container '{container.name}': {e}")


def docker_stop_container(container):
    """Stops the given container."""
    try:
        container.stop()
    except docker.errors.APIError as e:
        log_error(f"failed to stop container '{container.name}': {e}")


def docker_start_container(container):
    """Starts the given container."""
    try:
        container.start()
    except docker.errors.APIError as e:
        log_error(f"failed to start container '{container.name}': {e}")