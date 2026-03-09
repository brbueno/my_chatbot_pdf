import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()

# 1. Carregar texto
with open("inputs/sentencas.txt", "r", encoding="utf-8") as f:
    texto = f.read()

# 2. Quebrar em chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
docs = splitter.create_documents([texto])

# 3. Criar embeddings e índice vetorial
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# 4. Criar chain de QA com retrieval
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatOpenAI(temperature=0.2)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# 5. Loop de chat
print("Chat iniciado. Digite 'sair' para encerrar.\n")
while True:
    pergunta = input("Você: ")
    if pergunta.lower() in ["sair", "exit", "quit"]:
        break

    resposta = qa_chain({"query": pergunta})
    print("\nBot:", resposta["result"], "\n")
