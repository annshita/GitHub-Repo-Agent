import asyncio
import os
import streamlit as st
from textwrap import dedent
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.openai import OpenAIChat
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
load_dotenv()

# Optional: override the Groq model in .env with GROQ_MODEL=...


# Page config
st.set_page_config(page_title="GitHub Repo Agent", layout="wide")

# Load external stylesheet (lavender pastel, minimal)
def load_css(path: str):
    try:
        with open(path, "r", encoding="utf-8") as css_file:
            st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


load_css("styles.css")

# Title and description
st.markdown('<h1 class="app-title">GitHub Repo Agent</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Explore GitHub repositories with natural language'    
    'using the Model Context Protocol</p>',
    unsafe_allow_html=True,
)

# Setup sidebar for API key
# with st.sidebar:
#     st.header("🔑 Authentication")
#     api_key = st.text_input("Groq API Key", type="password", help="Get a free key at console.groq.com")
#     if api_key:
#         os.environ["GROQ_API_KEY"] = api_key
        
#     st.divider()

#     st.header("🔑 Authentication")
#     github_token = st.text_input("GitHub Token", type="password", help="Create a token with repo scope at github.com/settings/tokens")
    
#     if github_token:
#         os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = github_token
#     st.markdown("---")

# Authentication
# If both credentials are already loaded from .env, hide the sidebar.
env_groq_key = os.getenv("GROQ_API_KEY", "").strip()
env_github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN", "").strip()

api_key = env_groq_key
github_token = env_github_token

if not (env_groq_key and env_github_token):
    with st.sidebar:
        st.header("🔑 Authentication")

        if not env_groq_key:
            api_key = st.text_input(
                "Groq API Key",
                type="password",
                help="Get a key at console.groq.com"
            )
            if api_key:
                os.environ["GROQ_API_KEY"] = api_key

        if not env_github_token:
            github_token = st.text_input(
                "GitHub Token",
                type="password",
                help="Create a token at github.com/settings/tokens"
            )
            if github_token:
                os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"] = github_token

        st.markdown("---")
else:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"],
            [data-testid="collapsedControl"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# # Query input
# col1, col2 = st.columns([3, 1])
# with col1:
#     repo = st.text_input("Repository", value="Arindam200/awesome-ai-apps", help="Format: owner/repo")
# with col2:
#     query_type = st.selectbox("Query Type", [
#         "Info", "Issues", "Pull Requests", "Repository Activity", "Custom"
#     ])

# # Create predefined queries based on type
# if query_type == "Info":
#     query_template = f"Tell me all about {repo}"
# elif query_type == "Issues":
#     query_template = f"Find recent issues in {repo}"
# elif query_type == "Pull Requests":
#     query_template = f"Show me recent merged PRs in {repo}"
# elif query_type == "Repository Activity":
#     query_template = f"Analyze code quality trends in {repo}"
# else:
#     query_template = ""

# query = st.text_area("Your Query", value=query_template, 
#                      placeholder="What would you like to know about this repository?")

# Query input
col1, col2 = st.columns([3, 1])
with col1:
    repo = st.text_input(
        "Repository",
        placeholder="Enter GitHub repository URL",
        help="Paste a repo URL, e.g. https://github.com/owner/repo",
    )
with col2:
    query_type = st.selectbox("Query Type", [
        "Info", "Issues", "Pull Requests", "Repository Activity", "Custom"
    ])

# Query type drives a natural placeholder (no prefilled text)
if query_type == "Info":
    query_placeholder = "Give me an overview of this repository"
elif query_type == "Issues":
    query_placeholder = "What are the recent issues in this repository?"
elif query_type == "Pull Requests":
    query_placeholder = "Show me the recent merged pull requests"
elif query_type == "Repository Activity":
    query_placeholder = "Summarize recent activity and code quality trends"
else:
    query_placeholder = "Ask anything about this repository"

query = st.text_area("Your Query", placeholder=query_placeholder)

# Main function to run agent
async def run_github_agent(message):
    if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        return "Error: GitHub token not provided"
    if not (api_key or os.getenv("GROQ_API_KEY")): return "Error: Groq API key not provided"
    
    # …rest of your implementation…
    try:
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
            }
        )
        
        # Create client session with proper error handling
        try:
            async with stdio_client(server_params) as (read, write):
                try:
                    async with ClientSession(read, write) as session:
                        # Initialize MCP toolkit
                        # mcp_tools = MCPTools(session=session)
                        # try:
                        #     await mcp_tools.initialize()
                        #     st.write("Available MCP tools:", mcp_tools.functions.keys())
                            
                        #     # Create agent
                        #     agent = Agent(
                        #         tools=[mcp_tools],
                        #         instructions=dedent("""\
                        #             You are a GitHub repository assistant.

                        #             Use the available GitHub tools to answer the user's question.
                        #             Give concise, factual answers based on GitHub data.
                        #             Use markdown tables when useful.
                        #             Include relevant GitHub links when available.
                            
                        #         """),
                        #         markdown=True,
                        #         model=OpenAIChat(
                        #             id=os.getenv(
                        #                 "GROQ_MODEL",
                        #                 "openai/gpt-oss-20b"
                        #             ),
                        #             base_url="https://api.groq.com/openai/v1",
                        #             api_key=api_key or os.getenv("GROQ_API_KEY")
                        #         )
                        #     )

                        mcp_tools = MCPTools(session=session)

                        await mcp_tools.initialize()

                        allowed_tools = {
                            "get_file_contents",
                            "list_issues",
                            "list_pull_requests",
                            "list_commits",
                        }

                        mcp_tools.functions = {
                            name: function
                            for name, function in mcp_tools.functions.items()
                            if name in allowed_tools
                        }

                        agent = Agent(
                            tools=[mcp_tools],
                            instructions=dedent("""
                                        You are a GitHub repository assistant.

                                        Use the available GitHub MCP tool to answer the user's question.
                                        The repository usually uses the "main" branch. When a branch/ref parameter
                                        is required and the user has not specified one, use "main".
                                        Be concise and factual.
                                        Use markdown when helpful.
                                    """),
                            markdown=True,
                            model=OpenAIChat(
                                id="openai/gpt-oss-20b",
                                base_url="https://api.groq.com/openai/v1",
                                api_key=api_key or os.getenv("GROQ_API_KEY")
                            )
                        )

                        # Run agent with error handling
                        try:
                            response = await agent.arun(message)
                            return response.content
                        except Exception as agent_error:
                            error_text = str(agent_error)
                            if "403" in error_text or "access" in error_text.lower() or "permission" in error_text.lower():
                                    model_id = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
                                    return (
                                        f"Groq model access error for `{model_id}`. "
                                        "Check your Groq project/model permissions, or set "
                                        "`GROQ_MODEL` in `.env` to a model your API key can access. "
                                        f"Original error: {error_text}"
                                    )
                            return f"Error running agent: {error_text}"
                                
                        except Exception as init_error:
                            return f"Error initializing MCP tools: {str(init_error)}"
                            
                except Exception as session_error:
                    return f"Error creating client session: {str(session_error)}"
                    
        except Exception as client_error:
            return f"Error creating stdio client: {str(client_error)}"
            
    except Exception as e:
        return f"Error setting up server parameters: {str(e)}"

# Run button
# if st.button("Run Query", type="primary", use_container_width=True):
#     if not github_token:
#         st.error("Please enter your GitHub token in the sidebar")
#     elif not query:
#         st.error("Please enter a query")
#     else:
#         with st.spinner("Analyzing GitHub repository..."):
#             try:
#                 # Ensure the repository is explicitly mentioned in the query
#                 if repo and repo not in query:
#                     full_query = f"{query} in {repo}"
#                 else:
#                     full_query = query
                    
#                 result = asyncio.run(run_github_agent(full_query))
                
#                 # Display results in a nice container
#                 st.markdown("### Results")
#                 st.markdown(result)
#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")

# Run button
if st.button("Run Query", type="primary", use_container_width=True):
    # Check if token exists in either UI or .env
    active_github_token = github_token or os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    
    if not active_github_token:
        st.error("GitHub token not provided. Add GITHUB_PERSONAL_ACCESS_TOKEN to .env or enter it in the sidebar.")
    elif not (api_key or os.getenv("GROQ_API_KEY")):
        st.error("Groq API key not provided. Add GROQ_API_KEY to .env or enter it in the sidebar.")
    elif not query:
        st.error("Please enter a query")
    else:
        with st.spinner("Analyzing GitHub repository..."):
            try:
                if repo and repo not in query:
                    full_query = f"{query} in {repo}"
                else:
                    full_query = query
                    
                result = asyncio.run(run_github_agent(full_query))
                
                st.markdown("### Results")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")