from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter


def summarize(s: str) -> str:
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([s])
    llm = ChatOpenAI(temperature=0, model_name='gpt-4')
    summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce')
    output = summary_chain.run(docs)
    return output