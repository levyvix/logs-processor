from pathlib import Path
from typing import Final

# Directories
LOGS_DIR: Final = Path("logs")
STAGING_DIR: Final = Path("logs_staging")
DB_PATH: Final = Path("db.db")

# Database configuration
BATCH_SIZE: Final = 1000
MAX_RETRIES: Final = 3

# Logging configuration
LOG_LEVEL: Final = "INFO"
