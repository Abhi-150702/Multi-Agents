import asyncio
import streamlit as st

from orchestrator.workflow import get_workflow
from orchestrator.nodes import (
    initialize_agents,
    get_agents_status
)

from mcp_client.manager import MCPManager

from config.settings import Settings


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Syntera AI",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# Application Initialization
# ============================================================

@st.cache_resource
def initialize_application():

    config_settings = Settings()

    mcp_manager = MCPManager()

    async def initialize():

        # ----------------------------------------------------
        # Initialize MCP
        # ----------------------------------------------------

        await mcp_manager.register_server(
            "research",
            "mcp_servers/research_server.py"
        )

        # ----------------------------------------------------
        # Initialize Agents
        # ----------------------------------------------------

        await initialize_agents(
            config_settings=config_settings,
            mcp_manager=mcp_manager
        )

        # ----------------------------------------------------
        # Create Workflow
        # ----------------------------------------------------

        workflow = get_workflow(
            config_settings
        )

        return mcp_manager, workflow

    return asyncio.run(initialize())


# ============================================================
# Initialize Backend
# ============================================================

try:

    mcp_manager, workflow = initialize_application()

except Exception as exc:

    st.error(
        f"Failed to initialize application: {exc}"
    )

    st.stop()


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title("🤖 Syntera AI")

    st.markdown(
        """
        **Agentic AI Application**

        The system can route requests to:

        - 💬 General Agent
        - 🔎 Research Agent
        - 💻 Coding Agent
        """
    )

    st.divider()

    st.subheader("System Status")

    status = get_agents_status()

    if status["all_initialized"]:
        st.success("All agents initialized")
    else:
        st.warning("Some agents are not initialized")

    st.divider()

    st.caption(
        "Powered by LangGraph + LangChain + MCP"
    )


# ============================================================
# Main UI
# ============================================================

st.title("🤖 Syntera AI Assistant")

st.caption(
    "Ask a question and the system will route it to the appropriate agent."
)


# ============================================================
# Display Chat History
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# Chat Input
# ============================================================

query = st.chat_input(
    "Ask something..."
)


if query:

    # --------------------------------------------------------
    # Display User Message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    # --------------------------------------------------------
    # Generate Response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = asyncio.run(
                    workflow.ainvoke(
                        {
                            "user_query": query
                        }
                    )
                )

                # --------------------------------------------
                # Determine Response
                # --------------------------------------------

                if result.get("general_result"):

                    response = result[
                        "general_result"
                    ]

                elif result.get("research_result"):

                    response = result[
                        "research_result"
                    ]

                elif result.get("coding_result"):

                    response = result[
                        "coding_result"
                    ]

                else:

                    response = (
                        "I wasn't able to generate a response."
                    )

                # --------------------------------------------
                # Display
                # --------------------------------------------

                st.markdown(response)

                # --------------------------------------------
                # Store
                # --------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as exc:

                response = (
                    f"An error occurred: {str(exc)}"
                )

                st.error(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )