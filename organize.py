from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor

from tools.calendar import create_calendar_event
from tools.time import Datetime

system_description = \
"""
You are a personal assistant of the human.
Your role is to capture and organize things such as tasks, calendar events, and notes. 
On the basis of some conversation or context, you need to take a decision and perform an action to capture and organize things.
Evaluate actions on the basis of current time, context and conversation.
"""

llm = ChatOpenAI(temperature=0)
system_message = SystemMessage(content=system_description)
prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
tools = [create_calendar_event, Datetime]
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.run(
    "I have a meeting with my friend (harpinderjot36@gmail.com) tomorrow at 10:00 am."
)
