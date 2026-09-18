from agents.supervisor.agent import create_supervisor_agent

supervisor_agent = create_supervisor_agent()


test_queries = [
    "Research how HNSW works and explain it.",
    
    "Write a Python implementation of cosine similarity.",
    
    "Research the latest approaches for multimodal RAG "
    # "and implement one in Python.",
    
    # "Build a RAG application using LangGraph.",
]


for query in test_queries:

    print("\n" + "=" * 80)
    print(f"USER: {query}")
    print("=" * 80)

    result = supervisor_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": query,
            }
        ]
    })

    decision = result["structured_response"]

    print(f"ROUTE: {decision.route}")
    print(f"RATIONALE: {decision.rationale}")