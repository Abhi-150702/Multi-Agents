from agents.research.agent import create_research_agent
from config.logging_config import setup_logger

logger = setup_logger('main')

def main(query: str) -> None:
    if not query:
        return
    agent = create_research_agent()

    response = agent.invoke(
        {
            "messages" : [
                {
                    "role" : "user",
                    "content" : query
                }
            ]
        }
    )

    logger.info(f"-------FINAL RESPONSE-------\n{response['messages'][-1].content}")
    logger.info('\n\n------COMPLETE RESPONSE------\n',response)


if __name__ == '__main__' : 
    main(str(input('Query: ')))