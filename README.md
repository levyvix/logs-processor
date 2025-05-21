# Logs Processor

A Python project for processing and analyzing log files using modern Python tools and best practices.

## Project Overview

This project is designed to process and analyze log files with the following features:
- Efficient log file processing with batch operations
- Robust error handling and logging
- Database integration for data storage
- Concurrent processing capabilities
- Modern Python packaging with UV

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Installation

1. Install UV package manager if you haven't already:
   ```bash
   pip install uv
   ```

2. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd wind-cascade
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

### Running the Program

To run the main program:
```bash
uv run main.py
```

To run the log processing script:
```bash
uv run read_and_process.py
```

### Project Structure

```
logs-processor/
├── config.py           # Configuration settings
├── db/                 # Database related files
├── logs/               # Application logs
├── logs_staging/       # Staging area for log processing
├── main.py            # Main application entry point
├── read_and_process.py # Log processing script
├── pyproject.toml      # Project configuration
└── uv.lock            # UV lock file
```

## Features

- Robust logging with Loguru
- JSON log file processing
- Database integration
- Automated log rotation and compression
- Error handling and recovery

## Dependencies

- loguru >= 0.7.3

## Development

The project uses modern Python development practices:
- Type hints for better code maintainability
- Robust error handling
- Logging for debugging and monitoring

## License

MIT License
