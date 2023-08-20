from datetime import datetime
from langchain.tools import tool
import json

# chromadb_client = chromadb.Client()
# collection = chromadb_client.create_collection("notes")

@tool
def add_notes(title: str, source: str, note: str) -> str:
    '''
    Adds a note to the notebook with a title and source.
    Source could be slack conversation, email, etc.
    A note is added only when the information is required to be stored.
    '''
    try:
        timestamp = datetime.now().strftime('%m/%d/%Y, %H:%M')
        header = f"{source} : {timestamp}"
        ## Add to todo list
        with open('store/notes.md', 'a') as f:
            f.write(f"# {title}\n")
            f.write(f"- {header}\n")
            f.write(note)

        # collection.add(
        #     documents=[note],
        #     metadatas=[{'source': source, 'time': timestamp}],
        #     ids=[random.randint(5000, 100000)]
        # )
        return "Note added."
    except Exception as e:
        return json.dumps({'error': str(e)})

# @tool
# def search_notes(query: str) -> str:
#     '''
#     Searches for a note in the notebook.
#     '''
#     try:
#         results = collection.query(
#             query_texts=[query],
#             n_results=2,
#             fields=['documents', 'metadatas', 'ids']
#         )
#         return json.dumps(results)
#     except Exception as e:
#         return json.dumps({'error': str(e)})
