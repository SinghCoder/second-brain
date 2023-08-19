import datetime
import json
from langchain.agents import Tool


def time():
    # Get the current time
    current_time = datetime.datetime.now()
    # Format the time as a string in a local format

    local_time = current_time.strftime("%I:%M %p")
    return local_time


def date():
    # Get the current time
    current_time = datetime.datetime.now()

    # Format the time as a string in a local format
    local_time = current_time.strftime("%A, %B %d, %Y")
    return local_time


def fulldate():
    # Get the current time
    current_time = datetime.datetime.now()

    # Format the time as a string in a local format
    local_time = current_time.strftime("%A, %B %d, %Y %I:%M %p %Z")
    return local_time


def datetime_tool(request: str = 'now') -> str:
    '''
    Example:
        { "when":"today", "where":"Genova, Italy" }

    Args:
        request (str): optional/not used.

    Returns:
        date and time as a JSON data structure, in the format:

        '{{"fulldate":"<fulldate>","date":"<date>","time":"<time>"}}'
    '''

    data = {
        'fulldate': fulldate(),
        'date': date(),
        'time': time()
    }

    response_as_json = json.dumps(data)
    return response_as_json


#
# instantiate the langchain tool.
# The tool description instructs the LLM to pass data using a JSON.
# Note the "{{" and "}}": this double quotation is needed to avoid a runt-time error triggered by the agent instatiation.
#
name = "datetime"
response_format = '{{"fulldate":"<fulldate>","date":"<date>","time":"<time>"}}'
description = f'helps to retrieve date and time. Output is a JSON in the following format: {response_format}'

# create an instance of the custom langchain tool
Datetime = Tool(name=name, func=datetime_tool, description=description)
