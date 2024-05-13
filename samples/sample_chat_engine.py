from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModel
import samples.data_web_ingestion as data_web_ingestion

# Define large language model
service_provider = ServiceChatModel()
llm = service_provider.get_chat_model()
# Reference service
qdrant_service = data_web_ingestion.qdrant_service
embedding_model = data_web_ingestion.embedding_model

def chat_response(question: str):
    # Define index
    index = qdrant_service.load_index(embedding_model=embedding_model)

    chat_engine = index.as_chat_engine(llm=llm,chat_mode="simple",verbose=True)
    answer = chat_engine.chat(question)
    return answer
    
answer = chat_response("Who is Neymar?")
print(answer)

