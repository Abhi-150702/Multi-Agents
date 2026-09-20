import argparse

from orchestrator.workflow import get_workflow
from orchestrator.nodes import initialize_agents, get_agents_status
from config.logging_config import setup_logger
from config.settings import Settings


logger = setup_logger('main')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Multi-Agent AI Application"
    )

    parser.add_argument(
        "--use-ollama",
        action="store_true",
        help="Use Ollama as the LLM provider.",
    )

    return parser.parse_args()


def get_workflow_and_representation(config_settings):
    workflow = get_workflow(config_settings)

    png_bytes = workflow.get_graph().draw_mermaid_png()

    with open("workflow.png", "wb") as f:
        f.write(png_bytes)

    logger.info("Workflow saved to workflow.png")

    return workflow


def main():
    args = parse_arguments()

    config_settings = Settings()
    # Set runtime configuration from command-line arguments
    config_settings.use_ollama = args.use_ollama

    logger.info("Starting Multi-Agent Application...")
    logger.info(f"Use Ollama: {config_settings.use_ollama}")

    try:
        initialize_agents(config_settings)

        status = get_agents_status()

        if not status["all_initialized"]:
            logger.warning(
                "Some agents were not initialized at startup. "
                "They will be initialized when required."
            )

        logger.info("Application ready to accept queries!\n")

    except Exception as exc:
        logger.exception(
            f"Failed to initialize application: {exc}"
        )
        return
    workflow = get_workflow_and_representation(config_settings)

    while True:
        query = input("User Query: ").strip()

        if not query:
            continue

        if query.lower() in {"exit", "quit"}:
            logger.info("Shutting down application.")
            return

        try:
            result = workflow.invoke({"user_query": query})

            if result.get("general_result"):
                logger.info(f"\nAI Response: {result['general_result']}")

            elif result.get("research_result"):
                logger.info(f"\nAI Response: {result['research_result']}")

            elif result.get("coding_result"):
                logger.info(f"\nAI Response: {result['coding_result']}")

        except Exception as exc:
            logger.exception(
                f"Application error: {exc}"
            )


if __name__ == "__main__":
    main()
