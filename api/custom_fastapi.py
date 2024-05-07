import sys
import os
current_path = os.getcwd()
print(current_path)
sys.path.append(current_path)

from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing_extensions import Annotated
import uvicorn
from ingestion_modules.loader.pdf_loader import PDFReader

app = FastAPI(debug=True)

save_path = "save_pdf"

def save_pdf(file, file_name):
    with open(f"{save_path}/{file_name}", "wb") as f:
        f.write(file)
    f.close()

@app.post("/files/")
async def create_files(
    files: Annotated[List[bytes], File(description="Multiple files as bytes")],
):
    for file in files:
        print(file.decode("utf-8"))
    return {"file_sizes": [len(file) for file in files]}



@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        List[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    pdf_reader = PDFReader()
    
    for file in files:
        content = await file.read()
        save_pdf(content, file.filename)
        print(f"Save {file.filename} successfully")
        await pdf_reader.aload_data(f"{save_path}/{file.filename}")
    #return {"filenames": [file.filename for file in files]}
    return 1


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)