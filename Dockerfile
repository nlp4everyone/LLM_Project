FROM python:3.9
# Set working directory
WORKDIR /app
# Copy all files to working directory
COPY requirements.txt requirements.txt
# Install requirement packages
RUN pip install -r requirements.txt
RUN pip install llama-index-embeddings-fastembed
RUN pip install llama-index-vector-stores-elasticsearch
COPY . .
CMD python /app/test_vector.py
