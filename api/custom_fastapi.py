import sys
import os

current_path = os.getcwd()
sys.path.append(current_path)
from ingestion_modules.custom_loader.custom_pdf_loader import CustomPDFReader
from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService
from ai_modules.embedding_modules.service_embedding import (
    ServiceEmbedding,
)  # Change to custom
from llama_index.core.ingestion import IngestionPipeline  # Change to custom
from llama_index.core.text_splitter import SentenceSplitter  # Change to custom
from ingestion_modules import utils
from config.api_param import FASTAPI_PORT

from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel
import uvicorn

app = FastAPI(debug=True)

save_path = "save_pdf"


class PdfParam(BaseModel):
    files: Annotated[List[UploadFile], File(description="Multiple files as UploadFile")]
    collection_name: str = Form(description="Name of the new collection")


# Function to save pdf after upload
def save_pdf(file, file_name):
    with open(f"{save_path}/{file_name}", "wb") as f:
        f.write(file)
    f.close()


service_embedding = ServiceEmbedding(
    service_name="COHERE", model_name="embed-english-light-v3.0"
)
embedding_model = service_embedding.get_embedding_model()
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)


# Function to create a collection in qdrant db
def create_collection(content: str, collection_name: str):
    # Init vector_store
    qdrant_service = QdrantService(collection_name=collection_name, mode="local")

    nodes = pipeline.run(documents=content)

    # Convert nodes to docs
    docs = utils.convert_nodes_to_docs(nodes)

    # Build index
    qdrant_service.build_index_from_docs(
        documents=docs, embedding_model=embedding_model
    )


# @app.post("/files/")
# async def create_files(
#     files: Annotated[List[bytes], File(description="Multiple files as bytes")],
# ):
#     for file in files:
#         print(file.decode("utf-8"))
#     return {"file_sizes": [len(file) for file in files]}


@app.post("/create/")
async def create_upload_files(
    files: Annotated[
        List[UploadFile], File(description="Multiple files as UploadFile")
    ],
    collection_name: str = Form(description="Name of the new collection"),
):

    pdf_reader = CustomPDFReader()
    for file in files:
        bin_content = await file.read()
        print(type(bin_content))
        save_pdf(bin_content, file.filename)
        content = await pdf_reader.aload_data(f"{save_path}/{file.filename}")
        create_collection(content, collection_name)
    return f"Create collection {collection_name} successfully"


@app.get("/")
async def main():
    content = """
<body>
    <h1>Upload Files</h1>
    <form action="/create/" method="post" enctype="multipart/form-data">
        <label for="collection_name">Collection name:</label>
        <input type="text" id="collection_name" name="collection_name" required><br><br>
        <label for="files">Select files:</label>
        <input type="file" id="files" name="files" multiple required><br><br>
        <button type="submit">Upload</button>
    </form>
</body>
    """
    return HTMLResponse(content=content)
