import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Carregar variáveis de ambiente
load_dotenv()

def carregar_texto(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def criar_chatbot():
    # 1. Carregar texto
    texto = carregar_texto("inputs/sentencas.txt")

    # 2. Dividir em chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    docs = splitter.create_documents([texto])

    # 3. Criar embeddings e índice vetorial
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 4. Criar retriever e chain
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(temperature=0.2)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain

def iniciar_chat():
    print("\nChat IA iniciado! Digite 'sair' para encerrar.\n")

    chatbot = criar_chatbot()

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("\nEncerrando chat. Até mais!")
            break

        resposta = chatbot({"query": pergunta})
        print("\nBot:", resposta["result"], "\n")

if __name__ == "__main__":
    iniciar_chat()
