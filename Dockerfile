FROM python:3.9-slim
# Set working directory
WORKDIR /app
# Copy all files to working directory
COPY requirements.txt requirements.txt
# Install requirement packages
RUN pip install -r requirements.txt
#RUN pip install llama-index-embeddings-fastembed==0.1.3
#RUN pip install transformers -U
COPY . .

# Run RAG
CMD python /app/sample_rag.py
# CMD python /app/data_ingestion.py
