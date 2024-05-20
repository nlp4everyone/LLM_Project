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
EXPOSE 8501
CMD ["streamlit","run","demo_rag.py"]

#ENTRYPOINT ["streamlit", "run", "demo_rag.py", "--server.port=8501", "--server.address=192.168.65.9"]
# CMD python /app/test.py
#CMD streamlit run demo_rag.py
