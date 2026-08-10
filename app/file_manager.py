from pathlib import Path
from datetime import datetime


BASE_DOWNLOAD_FOLDER = Path("downloads")

ALLOWED_EXTENSIONS = {
    ".xlsx",
    ".xls",
    ".csv"
}


def get_today_folder():
    today = datetime.now().strftime("%Y-%m-%d")

    folder = BASE_DOWNLOAD_FOLDER / today

    folder.mkdir(parents=True, exist_ok=True)

    return folder


def is_allowed_file(filename: str):
    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


def generate_safe_filename(filename: str):
    original_path = Path(filename)

    original_name = original_path.stem
    extension = original_path.suffix.lower()

    timestamp = datetime.now().strftime("%H%M%S_%f")

    return f"{original_name}_{timestamp}{extension}"