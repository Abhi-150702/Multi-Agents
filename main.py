from orchestrator.workflow import get_workflow
from orchestrator.nodes import initialize_agents, get_agents_status
from config.logging_config import setup_logger

logger = setup_logger('main')

def get_workflow_and_representation():
    # Get workflow after agents are initialized
    workflow = get_workflow()

    # Saving the representation of the worflow in workflow.png file
    png_bytes = workflow.get_graph().draw_mermaid_png()
    with open("workflow.png", "wb") as f:
        f.write(png_bytes)
    logger.info("Workflow saved to workflow.png")

    return workflow

def main():
    # Initialize all agents at application startup
    logger.info("Starting Multi-Agent Application...")
    try:
        initialize_agents()

        # Verify all agents are initialized
        status = get_agents_status()
        if not status['all_initialized']:
            logger.error("Failed to initialize all agents. Status: %s", status)
            return

        logger.info("Application ready to accept queries!\n")
    except Exception as exc:
        logger.error(f"Failed to initialize agents: {str(exc)}")
        return

    workflow = get_workflow_and_representation()
    
    while True:
        query = str(input('User Query: '))

        if query.strip() == '' or query.strip().lower() in {'exit', 'quit'}:
            return

        try:
            result = workflow.invoke({
                'user_query' : query
            })

            # General result only
            if result.get('general_result'):
                logger.info(f"\nAI Response: {result['general_result']}")

            # Research result only
            if result.get('research_result'):
                logger.info(f"\nAI Response: {result['research_result']}")

            # Coding result only
            if result.get('coding_result'):
                logger.info(f"\n{result['coding_result']}")

        except Exception as exc:
            logger.error(f"Application error: {str(exc)}")


if __name__ == '__main__':
    main()