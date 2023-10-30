from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import os,secrets

app = FastAPI()

UPLOAD_DIR = "uploads"

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate a random filename using the 'secrets' module
    random_filename = secrets.token_hex(16)  # You can adjust the length of the filename as needed

    file_path = os.path.join(UPLOAD_DIR, random_filename)
    with open(file_path, 'wb') as f:
        while True:
            chunk = await file.read(65536)
            if not chunk:
                break
            f.write(chunk)
    
    return {"download_link": f"/download/{file.filename}"}

@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = os.path.join(UPLOAD_DIR, file_name)
    return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={file_name}"})
