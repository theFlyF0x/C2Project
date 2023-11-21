# Command and Control (C2) Framework

## Overview

This project is a simple Command and Control (C2) framework implemented in Python. It allows an operator to interact with remote systems through commands sent over a network connection.

## Features

- **Shell Access:** Open a reverse shell on the target system.
- **File Upload:** Upload files from the local system to the target system.
- **File Download:** Download files from the target system to the local system.
- **Session Management:** View and switch between active sessions.

## Getting Started

### Prerequisites

- Python minimum 3.10

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/theFlyF0x/C2Project.git
    cd C2Project
    ```

### Usage

1. Start the C2 server:

    ```bash
    python c2_server.py
    ```

2. Connect to the C2 server from the target system:

    ```bash
    python c2_client.py
    ```

3. Use the provided commands to interact with the target system.

## Commands

- `help`: Display help information.
- `sessions`: List all active sessions.
- `session <number>`: Switch to the specified session.
- `shell`: Open a reverse shell on the target system.
- `upload <local_file> <destination_path>`: Upload a file to the target system.
- `download <remote_file>`: Download a file from the target system.
- `quit`: Exit the C2 framework.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.
