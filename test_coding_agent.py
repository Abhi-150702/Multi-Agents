from agents.coding.agent import create_coding_agent

coding_agent = create_coding_agent()


result = coding_agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": """
            Inspect this project and explain its structure.
            """
        }
    ]
})


for message in result["messages"]:
    print("\n" + "=" * 80)
    print(message)