import streamlit as st
from config import params

supported_service = params.supported_services
def main_layout():
    # Default params
    provider_keys = list(supported_service.keys())
    chat_providers = [provider.title() for provider in provider_keys if len(supported_service[provider]["CHAT_MODELS"])>0]
    embedding_providers = [provider.title() for provider in provider_keys if len(supported_service[provider]["EMBBEDDING_MODELS"])>0]

    st.title("RAG Baseline")
    with st.sidebar:
        # with st.form(key="Parameter Layout Turning"):
        st.header("Configure")

        # Provide chat model provider
        selected_chat_provider = st.selectbox("Choose chat model provider:",chat_providers,index=len(chat_providers)-1)
        if not isinstance(selected_chat_provider,str) or len(selected_chat_provider) ==0:
            raise Exception("Selected Provider is not string")

        # Provide chat model
        chat_modelname = supported_service[selected_chat_provider.upper()]["CHAT_MODELS"]
        selected_chat_model = st.selectbox("Chat model name",chat_modelname)

        # Space
        st.markdown('##')
        # Provide embedding provider
        selected_embedding_provider = st.selectbox("Choose embedding provider:",embedding_providers)
        embedding_models = supported_service[selected_embedding_provider.upper()]["EMBBEDDING_MODELS"]
        # Provide embedding model
        selected_embedding_models = st.selectbox("Choose embedding model",embedding_models)

        # Space
        st.markdown('##')
        # Provide temperature
        temperature = st.slider("Temperature",value=0.7,step=0.05)
        # Provide max token
        max_tokens = st.select_slider("Max tokens", [128,256,512,1024])

        pressed_button = st.button("Apply")
        if pressed_button:
            print(max_tokens)
        # Choose chat model
        # chatmodel_name = supported_service[selected_provider.]
            # st.form_submit_button("Apply")


if __name__ == "__main__":
    main_layout()