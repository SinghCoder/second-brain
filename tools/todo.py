import json
import sqlite3

from datetime import datetime
import parsedatetime as pdt
from langchain.tools import tool

todoconn = sqlite3.connect('secondbrain.db')
todoconn.cursor().execute('''CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    what TEXT,
    due TEXT,
    parsed_when TIMESTAMP,
    completed BOOLEAN
)''')
todoconn.commit()

def add_todo_item(what: str, when: str) -> str:
    '''
    Adds a todo item to the todo list.
    '''
    try:
        cal = pdt.Calendar()
        datetime_obj, _ = cal.parseDT(when, datetime.now())
        parsed_when = datetime_obj.isoformat(timespec='minutes')

        ## Add to database
        cur = todoconn.cursor()
        values = (what, when, datetime_obj, False)
        cur.execute('INSERT INTO todos (what, due, parsed_when, completed) VALUES (?, ?, ?, ?)', values).close()
        todoconn.commit()

        cur = todoconn.cursor()
        cur.execute('SELECT * FROM todos order by parsed_when asc')
        todos = cur.fetchall()
        with open('store/todo.md', 'w') as f:
            for row in todos:
                what = row[1]
                due = row[2]
                parsed_when = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
                completed = ' ' if row[4] == False else 'x'
                f.write(f"- [{completed}] {what} by {due} ({parsed_when})\n")

        return json.dumps({'what': what,'when': f"{when} ({parsed_when})"})

    except Exception as e:
        return json.dumps({'error': str(e)})
