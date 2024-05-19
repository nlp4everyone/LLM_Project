from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Annotated

from api.support_param import *

app = FastAPI(debug=True)


@app.post("/login/")
def login_system(user_name: str, password: str):
    user = user_name
    password = password

    # Verify account:
    ## todo ##
    return "Login successfully"


@app.post("/UploadPrimary/")
async def create_files(
    file: Annotated[List[UploadFile], File(description="Multiple reference documents")]
):

    if len(file) > 1:
        raise Exception("Only one primary document can be uploaded")

    pdf_reader = CustomPDFReader()
    file = file[0]
    bin_content = await file.read()
    save_pdf(bin_content, file.filename)
    content = await pdf_reader.aload_data(f"{save_path}/{file.filename}")
    print(content)
    return "Upload primary document successfully"


@app.post("/UploadReference/")
async def create_upload_files(
    files: Annotated[
        List[UploadFile], File(description="Multiple reference documents")
    ],
    collection_name: str = Form(description="Name of the new collection"),
):

    if len(files) > 1:
        raise Exception("Only one primary document can be uploaded")

    pdf_reader = CustomPDFReader()
    for file in files:
        bin_content = await file.read()
        print(type(bin_content))
        save_pdf(bin_content, file.filename)
        content = await pdf_reader.aload_data(f"{save_path}/{file.filename}")
        create_collection(content, collection_name)
    return f"Create collection {collection_name} successfully"

@app.post("/Chat/")
async def create_files(
    file: Annotated[List[UploadFile], File(description="Multiple reference documents")]
):

    if len(file) > 1:
        raise Exception("Only one primary document can be uploaded")

    pdf_reader = CustomPDFReader()
    file = file[0]
    bin_content = await file.read()
    save_pdf(bin_content, file.filename)
    content = await pdf_reader.aload_data(f"{save_path}/{file.filename}")
    print(content)
    return "Upload primary document successfully"

@app.get("/")
async def main():
    content = """
<body>
    <h1>Upload Files</h1>
    <form action="/UploadReference/" method="post" enctype="multipart/form-data">
        <label for="collection_name">Collection name:</label>
        <input type="text" id="collection_name" name="collection_name" required><br><br>
        <label for="files">Select files:</label>
        <input type="file" id="files" name="files" multiple required><br><br>
        <button type="submit">Upload</button>
    </form>
</body>
    """
    return HTMLResponse(content=content)
