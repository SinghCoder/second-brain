from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.cleaners.core import clean, clean_extra_whitespace, remove_punctuation
from urlextract import URLExtract

extractor = URLExtract()

def generate_document(url):
    "Given an URL, return a langchain Document to futher processing"
    loader = UnstructuredURLLoader(urls=[url],
    mode="elements",
    post_processors=[clean,remove_punctuation,clean_extra_whitespace])
    elements = loader.load()
    selected_elements = [e for e in elements if e.metadata['category']=="NarrativeText"]
    full_clean = " ".join([e.page_content for e in selected_elements])
    return Document(page_content=full_clean, metadata={"source":url})


def url_summary(url: str) -> str:
    "Given an URL return the summary from OpenAI model"
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="stuff")
    tmp_doc = generate_document(url)
    summary = chain.run([tmp_doc])
    print("Summary: ", summary)
    return clean_extra_whitespace(summary)

def summarize_just_urls(s: str) -> str:
    urls = extractor.find_urls(s)
    print(urls)
    for i in range(len(urls)):
        s = s.replace(urls[i], f"{urls[i]} - {url_summary(urls[i])}")
    return s

def summarize(s: str) -> str:
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([s])
    llm = ChatOpenAI(temperature=0, model_name='gpt-4')
    summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce')
    output:str = ""
    # print(f"Docs: {docs}")
    output = summary_chain.run(docs)
    return output