FROM python:3.9
# Set working directory
WORKDIR /app
# Copy all files to working directory
COPY . /app
# Install requirement packages
RUN pip install -r requirements.txt
RUN pip install llama-index-embeddings-fastembed
CMD python /app/test_vector.py
EXPOSE 6333