# CLwB Sandbox

This project provides a CLI tool to manage isolated sandbox environments for developing and testing untrusted Bazel projects.

## Purpose

The sandbox provides a Docker container pre-configured with Bazel, IntelliJ IDEA, CLion, and other essential development tools. It allows for remote development via SSH or a graphical desktop session using RDP, providing a secure and reproducible environment for working with Bazel projects, especially for CLwB (C++ Language support within Bazel).

When a container starts, it automatically launches a JetBrains remote development backend, allowing you to connect from a local IDE for a seamless development experience.

## Setup

The tool can be installed into a local virtual environment using the Makefile:

```bash
make install
```

The Docker image for the sandbox can be built using the provided Makefile:

```bash
make image
```

This command builds the image and tags it as `clwb-sandbox`.


After the tool is installed, it can be executed from inside the virtual environment. To activate the virtual environment, run the following command:

```bash
source .venv/bin/activate
```

## CLI Usage

The CLI tool helps manage the lifecycle of the development sandboxes.

- **`create`**: Creates a new sandbox container. You must provide a path to your project's workspace and to a local checkout of the `clwb` repository. The container name is derived from your workspace's directory name.
  ```bash
  cli create --workspace /path/to/your/project --clwb /path/to/clwb
  ```

- **`info <name>`**: Shows detailed information about a specific container, including connection details (SSH, RDP), exposed ports, and mounted volumes.
  ```bash
  cli info <container_name>
  ```

- **`start <name>`**: Starts a stopped container.
  ```bash
  cli start <container_name>
  ```

- **`stop <name>`**: Stops a running container.
  ```bash
  cli stop <container_name>
  ```

- **`remove <name>`**: Stops and permanently removes a container.
  ```bash
  cli remove <container_name>
  ```

## Connecting to the Sandbox

You can connect to the running sandbox in two ways. Use the `sandbox info <name>` command to get the correct ports.

- **SSH**: For a terminal session, use the SSH command provided by the `info` command.
  ```bash
  ssh abc@localhost -p <ssh_port>
  ```

- **RDP**: For a full graphical desktop experience, use an RDP client to connect to the address provided by the `info` command.

## Remote Development with IntelliJ

The sandbox is designed for remote development with JetBrains IDEs. When a container is started, it automatically launches an IntelliJ remote development backend for the project located in the mounted `/config/clwb` directory. You can connect to this backend from a local JetBrains IDE (like IntelliJ or CLion with the Bazel plugin) to develop and debug your code directly inside the container.
