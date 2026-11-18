from pathlib import Path
from typing import Final

LOGS_DIR: Final = Path("logs")
STAGING_DIR: Final = Path("logs_staging")
DB_PATH: Final = Path("db.db")

BATCH_SIZE: Final = 1000

LOG_LEVEL: Final = "INFO"
