from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
DATA_DIR = BASE_DIR / "data"
MEDIA_DIR = DATA_DIR / "medien"
NOTES_FILE = DATA_DIR / "notes.txt"

app = FastAPI()
app.mount("/web", StaticFiles(directory=str(WEB_DIR)), name="web")


@app.get("/")
async def init_file_manager():
    file_path = WEB_DIR / "index.html"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="index.html")
    return FileResponse(str(file_path))


###################
## Modes
###################
@app.get("/media")
async def media_page():
    file_path = WEB_DIR / "media.html"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="media.html")
    return FileResponse(str(file_path))


@app.get("/database")
async def database_page():
    file_path = WEB_DIR / "database.html"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="database.html")
    return FileResponse(str(file_path))


@app.get("/notes")
async def notes_page():
    file_path = WEB_DIR / "notes.html"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="notes.html")
    return FileResponse(str(file_path))


###################
## Load
###################
@app.get("/media_load")
async def media_load() -> dict:
    import media

    media_list = media.main(1, save_dir=MEDIA_DIR)
    if media_list == 2:
        return {"data": []}
    return {"data": media_list}


@app.get("/database_load/{db}/{table}")
async def database_load(db: str, table: str) -> dict:
    import database

    table_collums, table_contend = database.main(db, table)
    return {"framework": table_collums, "data": table_contend}


@app.get("/notes_load")
async def notes_load() -> dict:
    import notes

    zettel = notes.main(0)
    return {"data": zettel}


@app.get("/download_data")
async def download_data():
    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, "w") as archive:
        if NOTES_FILE.exists():
            archive.write(NOTES_FILE, arcname="notes/notes.txt")
        if MEDIA_DIR.exists():
            for file in sorted(MEDIA_DIR.iterdir()):
                if file.is_file():
                    archive.write(file, arcname=f"media/{file.name}")

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer.read(),
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="filemanager_data.zip"'},
    )


@app.get("/notes_download")
async def notes_download():
    if not NOTES_FILE.exists():
        raise HTTPException(status_code=404, detail="No notes file found")

    return FileResponse(
        str(NOTES_FILE),
        media_type="text/plain",
        filename="notes.txt",
    )


@app.get("/media_download/{filename}")
async def media_download(filename: str):
    root = MEDIA_DIR.resolve()
    file_path = (root / filename).resolve()

    if root not in file_path.parents and file_path != root:
        raise HTTPException(status_code=404, detail="File not found")
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(str(file_path), media_type="application/octet-stream", filename=filename)


###################
## add
###################
class Notes(BaseModel):
    content: str


@app.post("/media_add")
async def media_add(file: UploadFile = File(...)) -> int:
    import media

    status = await media.save(file, MEDIA_DIR)
    return status


@app.post("/notes_save")
async def notes_save(data_input: Notes) -> dict:
    import notes

    try:
        notes.main(1, data_input.content)
        return {"status": 0}
    except Exception:
        return {"status": 1}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4300)