from loguru import logger
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import timedelta

logger.remove()

logger.add(sys.stderr, level="INFO", diagnose=True)

log_folder = Path("logs")
log_folder.mkdir(exist_ok=True)

logger.add(
    log_folder / "app.log",
    level="INFO",
    rotation=timedelta(minutes=1),
    compression="zip",
    serialize=True,
    enqueue=True,
    backtrace=True,
    diagnose=True,
)

logger.info("Start of program")


@logger.catch
def print_value(value, index):
    logger.info(f"Value: {value} Index: {index}")
    print(value, index)


values = [n for n in range(10)]
with ThreadPoolExecutor(max_workers=5) as executor:
    for i, value in enumerate(values):
        executor.submit(print_value, value=value, index=i)
    executor.shutdown()

logger.info("End of program")
