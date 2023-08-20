import os
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from tools.calendar import create_calendar_event, get_calendar_events
from tools.time import Datetime
from tools.todo import add_todo_item
from tools.notes import add_notes
from tools.contact import get_contact

USER = os.environ.get("USER")

distill_agent_description = \
f"""
You are a personal assistant of the user {USER}.
You have access to the user's notes, calendar meetings and todo items.
You should be able to prioritize things for the day for the user on the basis of time and context.
When there are conflicts in the schedule, suggest some other free time of the day for the conflicting event.
Also, make sure, you do not overload the user with too many things to do in a day.
If you need to ask/confirm something from the user, create a todo item for the user.
"""

def distill_agent_executor():
    llm = ChatOpenAI(temperature=0, model='gpt-4')
    system_message = SystemMessage(content=distill_agent_description)
    prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
    tools = [Datetime, add_todo_item, get_calendar_events, get_contact]
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor


