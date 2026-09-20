from orchestrator.workflow import get_workflow
from config.logging_config import setup_logger

logger = setup_logger('main')

def main():
    workflow = get_workflow()
    while True:
        query = str(input('User Query: '))

        if query.strip() == '' or query.strip().lower() in {'exit', 'quit'}:
            return

        try:
            result = workflow.invoke({
                'user_query' : query
            })

            # Research result only
            if result.get('research_result'):
                logger.info(f"\n{result['research_result']}")

            # Coding result only
            if result.get('coding_result'):
                logger.info(f"\n{result['coding_result']}")

        except Exception as exc:
            logger.error(f"Application error: {str(exc)}")


if __name__ == '__main__':
    main()