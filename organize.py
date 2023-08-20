from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from tools.calendar import create_calendar_event, get_calendar_events
from tools.time import Datetime
from tools.todo import add_todo_item
from tools.notes import add_notes
from tools.contact import get_contact

organize_agent_description = \
"""
You are a personal assistant of the human.
Your role is to capture and organize things such as tasks, calendar events, and notes. 
On the basis of some conversation or context, you need to take a decision and perform an action to capture and organize things.
Evaluate actions on the basis of current time, context and conversation.
When creating a calendar event, add entire conversation with user name and email in the description of the event.
If there is actionable item other than the meeting, create a todo item for the user.
To engage with the correct people, use the contact tool.
"""

def organize_agent_executor():
    llm = ChatOpenAI(temperature=0, model='gpt-4')
    system_message = SystemMessage(content=organize_agent_description)
    prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
    tools = [create_calendar_event, Datetime, add_todo_item, get_calendar_events, add_notes, get_contact]
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor
