from pathlib import Path
from fastapi import UploadFile


def main(mode: int, file: UploadFile = None, save_dir: Path = None):
    if mode == 1:
        return load(save_dir)
    if mode == 2:
        return 0
    return 1


def load(folder_path: Path) -> list:
    folder_path = Path(folder_path)
    media_arr = []
    if folder_path.exists():
        for file in sorted(folder_path.iterdir()):
            if file.is_file():
                media_arr.append(file.name)
    return media_arr


async def save(file: UploadFile, target_dir: Path) -> int:
    try:
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / file.filename
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        return 1
    except Exception:
        return 0  