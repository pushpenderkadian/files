from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
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

