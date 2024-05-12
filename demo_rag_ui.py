import streamlit as st
from config import params
import os,json
from typing import List,Union
from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModel

supported_service = params.supported_services
# Load config
state_path = os.path.join(params.cache_folder,"streamlit_status.json")

@st.cache_resource
def load_chat_model(chat_model_provider:str,chat_model:str,temperature:float):
    # Define service
    return ServiceChatModel(service_name=chat_model_provider.upper(),model_name=chat_model,temperature=temperature)


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


def main_layout():
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


    st.title("RAG Baseline")
    with st.sidebar:
        # with st.form(key="Parameter Layout Turning"):
        st.header("Configure")

        # Provide chat model provider
        chat_provider_index = find_index(current_state["chat_model_provider"],chat_providers) if os.path.exists(state_path) else 0
        selected_chat_provider = st.selectbox("Choose chat model provider:",chat_providers,index=chat_provider_index)

        # Provide chat model
        list_chat_models = supported_service[selected_chat_provider.upper()]["CHAT_MODELS"]
        chat_model_index = find_index(current_state["chat_model"],list_chat_models) if os.path.exists(state_path) else 0
        selected_chat_model = st.selectbox("Chat model name",list_chat_models,index=chat_model_index)

        # Space
        st.markdown('##')
        # Provide embedding provider
        embedding_provider_index = find_index(current_state["embedding_provider"],embedding_providers) if os.path.exists(state_path) else 0
        selected_embedding_provider = st.selectbox("Choose embedding provider:",embedding_providers,index=embedding_provider_index)

        # Provide embedding model
        embedding_models = supported_service[selected_embedding_provider.upper()]["EMBBEDDING_MODELS"]
        embedding_model_index = find_index(current_state["embedding_provider"],embedding_models) if os.path.exists(state_path) else 0
        selected_embedding_model = st.selectbox("Choose embedding model",embedding_models,index=embedding_model_index)

        # Space
        st.markdown('##')
        temperature_value = 0.7 if not os.path.exists(state_path) else current_state["temperature"]
        # Provide temperature
        temperature = st.slider("Temperature",value=temperature_value,step=0.05)

        # Provide max token
        list_max_tokens = [128,256,512,1024]
        max_tokens_index = find_index(current_state["max_tokens"], list_max_tokens)
        max_tokens = st.select_slider("Max tokens", options=list_max_tokens,value=list_max_tokens[max_tokens_index])

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

    # Chat flow
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})
        print(st.session_state["messages"])

if __name__ == "__main__":
    main_layout()