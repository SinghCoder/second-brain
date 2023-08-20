from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from tools.calendar import create_calendar_event, get_calendar_events
from tools.time import Datetime
from tools.todo import add_todo_item

system_description = \
"""
You are a personal assistant of the human.
Your role is to capture and organize things such as tasks, calendar events, and notes. 
On the basis of some conversation or context, you need to take a decision and perform an action to capture and organize things.
Evaluate actions on the basis of current time, context and conversation.
When creating a calendar event, add entire conversation with user name and email in the description of the event.
You should be able to prioritize things for the day for the user on the basis of time and context.
When there are conflicts in the schedule, suggest some other free time of the day for the conflicting event.
Also, make sure, you do not overload the user with too many things to do in a day.
"""

llm = ChatOpenAI(temperature=0, model='gpt-4')
system_message = SystemMessage(content=system_description)
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
tools = [create_calendar_event, Datetime, add_todo_item, get_calendar_events]
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
