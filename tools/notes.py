from datetime import datetime
import parsedatetime as pdt
from langchain.tools import tool
import json


@tool
def add_notes(title: str, source: str, note: str) -> str:
    '''
    Adds a note to the notebook with a title and source.
    Source could be slack conversation, email, etc.
    A note is added only when the information is required to be stored.
    '''
    try:
        header = f"- {datetime.now().isoformat(timespec='hours')}"
        ## Add to todo list
        with open('store/notes.md', 'a') as f:
            f.write(f"# {title}\n")
            f.write(f"{header}\n")
            f.write(f"- {source}\n")
            f.write(note)
        return "Note added."
    except Exception as e:
        return json.dumps({'error': str(e)})


