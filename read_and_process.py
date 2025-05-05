import json
from pathlib import Path
from zipfile import ZipFile
from loguru import logger
from typing import Generator
from config import LOGS_DIR, STAGING_DIR, BATCH_SIZE
from db import Database


def verify_if_log_folder_exist(path: Path, staging_folder: Path) -> None:
    """
    Verify if log folder exists and create staging folder if needed

    Args:
        path (Path): Path to logs folder
        staging_folder (Path): Path to staging folder

    Raises:
        FileNotFoundError: If logs folder not found
    """
    if not path.exists():
        raise FileNotFoundError("Logs folder not found.")

    if not staging_folder.exists():
        staging_folder.mkdir()
        logger.info("Staging folder created")
    else:
        logger.info("Staging folder found")


def extract_zip_file(zip_file_path: Path, staging_folder: Path) -> Path:
    """
    Extract zip file to staging folder

    Args:
        zip_file_path (Path): Path to zip file
        staging_folder (Path): Path to staging folder

    Returns:
        Path: Path to extracted file

    Raises:
        AssertionError: If zip file is empty
    """
    with ZipFile(zip_file_path) as zip_file:
        infolist = zip_file.infolist()
        assert infolist, f"No files in zip file {zip_file_path}"

        filename = infolist[0].filename
        zip_file.extractall(staging_folder)
        return staging_folder / filename


def read_json_log_file(log_file_path: Path) -> Generator[dict, None, None]:
    """
    Read and parse JSON log file line by line

    Args:
        log_file_path (Path): Path to the log file

    Yields:
        dict: Parsed JSON log entry

    Raises:
        ValueError: If file cannot be read
        json.JSONDecodeError: If JSON parsing fails
    """
    try:
        with open(log_file_path, "r", encoding="utf-8") as log_file:
            for line in log_file:
                try:
                    log_entry = json.loads(line)
                    yield log_entry
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in line: {line[:100]}... Error: {e}")
                    continue
    except Exception as e:
        logger.error(f"Failed to read log file {log_file_path}: {e}")
        raise


def process_logs(log_file_path: Path, db: Database) -> None:
    """
    Process JSON log entries in batches with transaction management

    Args:
        log_file_path (Path): Path to the log file
        db (Database): Database connection instance
    """
    try:
        with db.transaction():
            batch = []
            for log_entry in read_json_log_file(log_file_path):
                if "text" in log_entry and "record" in log_entry:
                    batch.append(
                        (
                            log_entry["record"]["level"]["name"],
                            log_entry["record"]["message"],
                            log_entry["record"]["time"]["timestamp"],
                        )
                    )

                    if len(batch) >= BATCH_SIZE:
                        db.insert_logs(batch)
                        batch = []

            # Insert remaining logs
            if batch:
                db.insert_logs(batch)

    except Exception as e:
        logger.error(f"Failed to process logs: {e}")
        raise


def main() -> None:
    """Main entry point with improved error handling and progress tracking"""
    try:
        # Initialize database
        with Database() as db:
            db.create_table()

            # Verify folders
            verify_if_log_folder_exist(LOGS_DIR, STAGING_DIR)

            # Process files
            zip_files = list(LOGS_DIR.glob("*.zip"))
            if not zip_files:
                logger.warning("No zip files found")
                return

            total_files = len(zip_files)
            for i, zip_file in enumerate(zip_files, 1):
                try:
                    logger.info(f"Processing file {i}/{total_files}: {zip_file.name}")
                    extracted_file = extract_zip_file(zip_file, STAGING_DIR)
                    process_logs(extracted_file, db)
                    extracted_file.unlink()
                except Exception as e:
                    logger.error(f"Error processing {zip_file.name}: {e}")
                    continue

    except KeyboardInterrupt:
        logger.warning("Processing interrupted by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        raise


if __name__ == "__main__":
    main()
