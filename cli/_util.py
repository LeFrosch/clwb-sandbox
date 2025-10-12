import sys
import os
import subprocess
import hashlib

from simple_term_menu import TerminalMenu


def log(message: str):
    print('>> ' + message)


def log_error(message: str):
    print('!! ' + message)
    sys.exit(1)


def exit(message: str):
    log(message)
    sys.exit(1)


def ask(question: str) -> bool:
    while True:
        answer = input('?? %s [y/n]' % question)

        if answer in ['y', 'Y']:
            return True
        if answer in ['n', 'N']:
            return False


def choose(title: str, options: list[str]) -> str:
    menu = TerminalMenu(options, title='?? ' + title)
    index = menu.show()

    return options[index][1]


def wait(message: str):
    input(':: %s' % message)


def filter_none(generator):
    return (x for x in generator if x is not None)


def first(generator):
    return next(iter(generator), None)


def get_workspace_dir(workspace_source):
    """
    Determines the workspace directory. If the source is a Git URL,
    it clones the repository. If it's a local path, it validates it.
    Returns the absolute path to the workspace directory.
    """
    if workspace_source.startswith(('https://', 'http://', 'git@')):
        project_name = os.path.basename(workspace_source)
        if project_name.endswith('.git'):
            project_name = project_name[:-4]

        workspace_dir = os.path.expanduser(f'~/.cache/clwb-workspaces/{project_name}')

        if os.path.isdir(os.path.join(workspace_dir, '.git')):
            log(f"workspace '{project_name}' already cloned in '{workspace_dir}', using existing directory")
        elif os.path.exists(workspace_dir):
            log_error(f"path '{workspace_dir}' exists but is not a git repository")
        else:
            log(f"cloning workspace from '{workspace_source}' into '{workspace_dir}'")
            try:
                subprocess.run(['git', 'clone', workspace_source, workspace_dir], check=True)
            except FileNotFoundError:
                log_error("command 'git' not found, is it installed and in your PATH?")
            except subprocess.CalledProcessError as e:
                log_error(f'error cloning repository: {e.stderr.strip()}')
        return workspace_dir
    else:
        # It's a local path
        if not os.path.isdir(workspace_source):
            log_error(f"workspace directory '{workspace_source}' not found")
        return os.path.abspath(workspace_source)


def container_derive_port(name):
    """Derives a stable port from the container name."""
    hash_object = hashlib.sha256(name.encode())
    hex_dig = hash_object.hexdigest()
    hash_int = int(hex_dig[:8], 16)
    port_range_start = 20000
    port_range_end = 60000
    port_range_size = port_range_end - port_range_start
    return port_range_start + (hash_int % port_range_size)
