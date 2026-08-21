
from pathlib import Path


def main(mode: int, input_data: str = None) -> str:
    base_dir = Path(__file__).resolve().parent
    filepath = base_dir / "data" / "notes.txt"
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if mode == 0:
        if not filepath.exists():
            return ""
        return filepath.read_text(encoding="utf-8")

    if mode == 1:
        if input_data is None:
            return "Keine Daten zum Schreiben übergeben"
        filepath.write_text(input_data, encoding="utf-8")
        return "Gespeichert"

    return "Ungültiger Typ"
            

