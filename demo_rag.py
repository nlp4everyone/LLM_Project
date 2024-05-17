import streamlit as st
from config import params
import os,json
from typing import List,Union
from ai_modules.chatmodel_modules import ServiceChatModel
from ai_modules.embedding_modules import ServiceEmbedding
from ingestion_modules.custom_vectorstore import QdrantService

supported_service = params.supported_services
# Load config
state_path = os.path.join(params.cache_folder,"streamlit_status.json")



@st.cache_resource
def load_chat_model(chat_model_provider:str,chat_model:str,temperature:float):
    # Define service
    chat_service = ServiceChatModel(service_name=chat_model_provider.upper(),model_name=chat_model,temperature=temperature)
    return chat_service.get_chat_model()

@st.cache_resource
def load_embedding_model(embedding_provider:str,model_name:str,batch_size = 1):
    # Define service
    embedding_service = ServiceEmbedding(model_name=model_name,service_name=embedding_provider.upper(),batch_size=batch_size)
    return embedding_service.get_embedding_model()

@st.cache_resource
def load_vector_service():
    # Define service
    return QdrantService()

def chat_response(question: str,vector_service,embedding_model,chat_model):
    # Define index
    index = vector_service.load_index(embedding_model=embedding_model)

    chat_engine = index.as_chat_engine(llm=chat_model,chat_mode="simple",verbose=True)
    answer = chat_engine.chat(question)
    return answer

def save_state(data:dict,path = state_path):
    os.makedirs(params.cache_folder,exist_ok=True)
    assert data, "Data cant be None"

    # Save file
    with open(path,'w') as f:
        json.dump(data,f)

def load_current_state(path = state_path):
    if not os.path.exists(path):
        return {
            "chat_model_provider":"",
            "chat_model":"",
            "embedding_provider":"",
            "embedding_model":"",
            "temperature":"",
            "max_tokens":""
        }
    # Save file
    with open(path, 'r') as f:
        return json.load(f)

def set_params_state(current_state):
    st.session_state["chat_model_provider"] = current_state["chat_model_provider"]
    st.session_state["chat_model"] = current_state["chat_model"]
    st.session_state["embedding_provider"] = current_state["embedding_provider"]
    st.session_state["embedding_model"] = current_state["embedding_model"]
    st.session_state["temperature"] = current_state["temperature"]
    st.session_state["max_tokens"] = current_state["max_tokens"]


def find_index(query:str,refs :Union[List[str],List[int]]):
    index = 0

    if isinstance(refs[0],str):
        # Preprocess
        refs = [ref.lower() for ref in refs]
        query = query.lower()

    # Check index
    return index if query not in refs else refs.index(query)

def notify_save():
    st.warning("You must click the Apply button for accepting change!")


def main_layout():
    # Define title
    st.title("RAG Baseline")

    # Default params
    provider_keys = list(supported_service.keys())
    chat_providers = [provider.title() for provider in provider_keys if len(supported_service[provider]["CHAT_MODELS"])>0]
    embedding_providers = [provider.title() for provider in provider_keys if len(supported_service[provider]["EMBBEDDING_MODELS"])>0]

    # Load state
    current_state = load_current_state()
    # Set state
    set_params_state(current_state)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display chat messages from history on app rerun
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.sidebar:
        # with st.form(key="Parameter Layout Turning"):
        st.header("Configure")

        # Provide chat model provider
        chat_provider_index = find_index(current_state["chat_model_provider"],chat_providers) if os.path.exists(state_path) else 0
        selected_chat_provider = st.selectbox("Choose chat model provider:",chat_providers,index=chat_provider_index,on_change=notify_save)

        # Provide chat model
        list_chat_models = supported_service[selected_chat_provider.upper()]["CHAT_MODELS"]
        chat_model_index = find_index(current_state["chat_model"],list_chat_models) if os.path.exists(state_path) else 0
        selected_chat_model = st.selectbox("Chat model name",list_chat_models,index=chat_model_index,on_change=notify_save)

        # Space
        st.markdown('##')
        # Provide embedding provider
        # embedding_provider_index = find_index(current_state["embedding_provider"],embedding_providers) if os.path.exists(state_path) else 0
        # Fix embedding provider
        embedding_provider_index = find_index(params.embedding_service,embedding_providers) if os.path.exists(state_path) else 0
        selected_embedding_provider = st.selectbox("Choose embedding provider:",embedding_providers,index=embedding_provider_index,disabled=True)

        # Provide embedding model
        embedding_models = supported_service[selected_embedding_provider.upper()]["EMBBEDDING_MODELS"]
        # embedding_model_index = find_index(current_state["embedding_provider"],embedding_models) if os.path.exists(state_path) else 0
        # Fix embedding model name
        embedding_model_index = find_index(params.embedding_model_name, embedding_models) if os.path.exists(state_path) else 0
        selected_embedding_model = st.selectbox("Choose embedding model",embedding_models,index=embedding_model_index,disabled=True)

        # Space
        st.markdown('##')
        temperature_value = 0.7 if not os.path.exists(state_path) else current_state["temperature"]
        # Provide temperature
        temperature = st.slider("Temperature",value=temperature_value,step=0.05,on_change=notify_save)

        # Provide max token
        list_max_tokens = [128,256,512,1024]
        max_tokens_index = find_index(current_state["max_tokens"], list_max_tokens)
        max_tokens = st.select_slider("Max tokens", options=list_max_tokens,value=list_max_tokens[max_tokens_index],on_change=notify_save)

        pressed_button = st.button("Apply")
        if pressed_button:
            st.success("Saved params")
            current_state["chat_model_provider"] = selected_chat_provider
            current_state["chat_model"] = selected_chat_model
            current_state["embedding_provider"] = selected_embedding_provider
            current_state["embedding_model"] = selected_embedding_model
            current_state["temperature"] = temperature
            current_state["max_tokens"] = max_tokens
            # Set state
            set_params_state(current_state)
            # Save state
            save_state(data=st.session_state.to_dict())
            # Reset message
            st.session_state["messages"] = []

    # Define variable
    embedding_model = load_embedding_model(embedding_provider=current_state["embedding_provider"].upper(),model_name=current_state["embedding_model"])
    chat_model = load_chat_model(chat_model_provider=current_state["chat_model_provider"].upper(),chat_model=current_state["chat_model"],temperature=float(current_state["temperature"]))
    qdrant_service = load_vector_service()

    # Chat flow
    # print(disabled_chat)
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        # print(st.session_state["messages"])

        # Generate response
        # try:
        response = chat_response(question=prompt,vector_service=qdrant_service,chat_model=chat_model,embedding_model=embedding_model)
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add user message to chat history
        st.session_state["messages"].append({"role": "assistant", "content": response})
        # except Exception as e:
        #     st.error(e)

if __name__ == "__main__":
    # Python Program to Get IP Address
    main_layout()