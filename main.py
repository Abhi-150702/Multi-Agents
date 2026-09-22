import argparse
import asyncio

from orchestrator.workflow import get_workflow
from orchestrator.nodes import initialize_agents, get_agents_status

from mcp_client.manager import MCPManager

from config.logging_config import setup_logger
from config.settings import Settings


logger = setup_logger("main")


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


async def main():

    args = parse_arguments()

    config_settings = Settings()
    # Set runtime configuration from command-line arguments
    config_settings.use_ollama = args.use_ollama

    logger.info("Starting Multi-Agent Application...")
    logger.info(f"Use Ollama: {config_settings.use_ollama}")

    mcp_manager = MCPManager()

    try:
        logger.info("=" * 60)
        logger.info("Initializing MCP Servers...")
        logger.info("=" * 60)

        await mcp_manager.register_server(
            server_name="research",
            server_path="mcp_servers/research_server.py"
        )

        logger.info("Research MCP Server initialized successfully!")

        await mcp_manager.register_server(
            server_name="coding",
            server_path="mcp_servers/coding_server.py"
        )

        logger.info("Coding MCP Server initialized successfully!")
        

        await initialize_agents(
            config_settings=config_settings,
            mcp_manager=mcp_manager
        )

        status = get_agents_status()

        if not status["all_initialized"]:
            logger.warning(
                "Some agents were not initialized at startup. "
                "They will be initialized when required."
            )

        else:
            logger.info("All agents initialized successfully!")

        workflow = get_workflow_and_representation(config_settings)

        logger.info("Application ready to accept queries!\n")

        while True:
            query = input("\n\nUser Query: ").strip()

            if not query:
                continue

            if query.lower() in {"exit", "quit"}:
                logger.info("Shutting down application.")
                break

            try:
                result = await workflow.ainvoke(
                    {
                        "user_query": query
                    }
                )

                if result.get("general_result"):
                    logger.info(
                        f"\nAI Response: "
                        f"{result['general_result']}"
                    )

                elif result.get("research_result"):
                    logger.info(
                        f"\nAI Response: "
                        f"{result['research_result']}"
                    )

                elif result.get("coding_result"):
                    logger.info(
                        f"\nAI Response: "
                        f"{result['coding_result']}"
                    )

            except Exception as exc:
                logger.exception(f"Application error: {exc}")

    except Exception as exc:
        logger.exception(f"Failed to initialize application: {exc}")

    finally:
        logger.info("Shutting down MCP connections...")
        try:
            await mcp_manager.disconnect()
            logger.info("MCP connections closed successfully.")

        except Exception as exc:
            logger.exception(f"Error while shutting down MCP: {exc}")

if __name__ == "__main__":
    asyncio.run(main())