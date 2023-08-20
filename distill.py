import os
from datetime import datetime
import dateutil.parser as parser
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from tools.calendar import create_calendar_event, get_calendar_events,fetch_calendar_events
from tools.time import Datetime
from tools.todo import add_todo_item
from tools.notes import add_notes
from tools.contact import get_contact
from tools.slack import notify_user


from dotenv import load_dotenv
load_dotenv()

USER = os.environ.get("USER")

distill_agent_description = \
f"""
You are a personal assistant of the user {USER}.
You have access to the user's notes, calendar meetings and todo items.
You should be able to prioritize things for the day for the user on the basis of time and context.
When there are conflicts in the schedule, suggest some other free time of the day for the conflicting event.
Also, make sure, you do not overload the user with too many things to do in a day.
If you need to ask/confirm something from the user, create a todo item for the user.
Also, keep track of actions already taken. 
"""

def distill_agent_executor():
    llm = ChatOpenAI(temperature=0, model='gpt-4')
    system_message = SystemMessage(content=distill_agent_description)
    prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
    tools = [Datetime, notify_user, get_conflicting_meetings]
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

def get_conflicting_meetings():
    events = fetch_calendar_events()
    if not events:
        return "No events found for today"
    event_summary = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = parser.isoparse(start)
        end = event['end'].get('dateTime', event['end'].get('date'))
        end = parser.isoparse(end)
        event_summary = event_summary + [{
            'title': event['summary'],
            'start': start,
            'end': end,
        }]

    conflicts = []
    event_summary.sort(key=lambda x: x['start'])
    for i in range(len(event_summary) - 1):
        if event_summary[i]['end'] > event_summary[i + 1]['start']:
            conflicts = conflicts + [(event_summary[i], event_summary[i + 1])]
    
    if not conflicts:
        return "No conflicts found for today"
    else:
        result = "Conflicts found for today: \n"
        for e1, e2 in conflicts:
            edesc = lambda e : f"{e['title']} at {e['start'].strftime('%H:%M')}"
            result += f"{edesc(e1)} conflicts with {edesc(e2)}. \n"
        return result

