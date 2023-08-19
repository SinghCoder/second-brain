from organize import agent_executor

if __name__ == '__main__':
    print("We will show you the prioritized list of things to do today.")
    agent_executor.run(
        "Show me the prioritized list of things to do today."
    )
