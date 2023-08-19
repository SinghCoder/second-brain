from datetime import datetime
from langchain.tools import tool
import json

@tool
def add_todo_item(request: str) -> str:
    '''
    Example:
        { "what":"buy milk", "when":"tomorrow" }

    Args:
        request (str): a string representing the item to add to the todo list.

    Returns:
        a JSON data structure, in the format:

        '{{"what":"<what>","when":"<when>"}}'
    '''

    what = data['what']
    data = json.loads(request)
    when = datetime.now().isoformat()
    data = {
        'what': what,
        'when': when
    }

    response_as_json = json.dumps(data)
    return response_as_json

