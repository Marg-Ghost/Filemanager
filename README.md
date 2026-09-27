# MARG File Manager

A small personal file manager built with FastAPI and a static HTML/CSS/JavaScript interface. It currently supports uploading and downloading files, editing a plain-text notes file, and exporting notes and media together as a ZIP archive.

## Features

- Browse, upload, and download files in the media directory.
- Edit and download a plain-text notes file.
- Download notes and media together as a ZIP archive.
- Protect data endpoints with HTTP Basic authentication.
- Run locally with Python or in a single Docker container.

## Requirements

- Python 3.11 or newer
- Dependencies listed in `requirements.txt`
- Docker, if using the container setup

## Run locally

Set credentials before starting the app. Replace these example values with your own:

```powershell
$env:APP_USER = "your-user"
$env:PASSWORD = "replace-with-a-long-unique-password"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload --port 4300
```

Open <http://localhost:4300>. The interactive API documentation is at <http://localhost:4300/docs>.

On Linux or macOS, activate the environment and set credentials like this:

```sh
export APP_USER="your-user"
export PASSWORD="replace-with-a-long-unique-password"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload --port 4300
```

## Run with Docker

Build and run the image from the repository root, passing credentials through environment variables:

```sh
docker build -t marg-file-manager .
docker run --rm -p 4300:4300 -e APP_USER=your-user -e PASSWORD=replace-with-a-long-unique-password marg-file-manager
```

Open <http://localhost:4300>. The current Docker setup does not persist changes to notes and uploaded media when the container is removed.

## Pages and API

| Page | Endpoint | Status |
| --- | --- | --- |
| Home | `/` | Available |
| Media | `/media` | Upload and download files |
| Notes | `/notes` | Read, edit, and download notes |
| Database | `/database` | Placeholder; database module and UI are not implemented yet |

Data endpoints use HTTP Basic authentication:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/media_load` | List stored media filenames |
| `POST` | `/media_add` | Upload a file |
| `GET` | `/media_download/{filename}` | Download one media file |
| `GET` | `/notes_load` | Read notes |
| `POST` | `/notes_save` | Save notes; JSON body: `{"content": "..."}` |
| `GET` | `/notes_download` | Download the notes file |
| `GET` | `/download_data` | Download notes and media as a ZIP archive |

## Data locations

- Notes: `data/notes.txt`
- Uploaded media: `data/medien/`

## Limitations and security

This is a prototype, not a production-ready file service. The code currently falls back to an empty username and the known password `standard_passwort` when `APP_USER` or `PASSWORD` is not set. Always set both values, and do not expose the service to an untrusted network. Uploaded files and notes are stored without a database. The database page is unfinished, and the supplied check scripts are manual smoke checks rather than an automated test suite.

The Docker image has no persistent volume configured, so its data is lost when the container is removed. Add a data volume before relying on it for anything important.

## Project structure

```text
server.py              FastAPI app, routes, and authentication
media.py               Media listing and upload helpers
notes.py               Plain-text notes storage
database.py            Database feature (currently empty)
requirements.txt       Runtime and check-script dependencies
Dockerfile             Single-container setup
data/                  Notes and uploaded media
web/                   Static pages, styles, scripts, and images
```
