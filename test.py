
from llama_index.readers.file.pymu_pdf import PyMuPDFReader

from llama_index.core.node_parser import SemanticSplitterNodeParser

docs = PyMuPDFReader().load_data("data/whales.pdf")
# all_text = [doc.text for doc in docs]
# all_text = "\n".join(all_text)
# print(all_text)
from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModel
chat_service = ServiceChatModel()
llm = chat_service.get_chat_model()

from llama_index.core.extractors import QuestionsAnsweredExtractor

extractor = QuestionsAnsweredExtractor(llm=llm,questions=15)
questions = extractor.extract(docs)

all_questions = ""
for question in questions:
    all_questions += question["questions_this_excerpt_can_answer"] + '\n'

with open("question.txt",'w') as f:
    f.write(all_questions)