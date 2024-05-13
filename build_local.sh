# Rebuild
#docker build -t llamaindex-project .
# Run Qdrant DB
docker run -d --name qdrant_db -p 6333:6333 qdrant/qdrant
# Run streamlit
streamlit run demo_rag.py
# Access web
xdg-open http://localhost:8501/