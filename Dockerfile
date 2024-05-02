FROM python:3.9
# Set working directory
WORKDIR /app
# Copy all files to working directory
COPY requirements.txt requirements.txt
# Install requirement packages
RUN pip install -r requirements.txt
RUN pip install llama-index-embeddings-fastembed
COPY . .
CMD python /app/insert_db.py
