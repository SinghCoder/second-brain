from datetime import datetime
import parsedatetime as pdt
from langchain.tools import tool
import json


@tool
def add_todo_item(what: str, when: str) -> str:
    '''
    Adds a todo item to the todo list.
    '''

    try:
        cal = pdt.Calendar()
        datetime_obj, _ = cal.parseDT(when, datetime.now())
        parsed_when = datetime_obj.isoformat()

        ## Add to todo list
        with open('todo.md', 'a') as f:
            f.write(f"- [ ] {what} by {when} ({parsed_when})\n")

        return json.dumps({'what': what,'when': f"{when} ({parsed_when})"})

    except Exception as e:
        return json.dumps({'error': str(e)})

