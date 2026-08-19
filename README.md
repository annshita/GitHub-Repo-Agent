# GitHub Repo Agent

A GitHub repository exploration tool powered by the Model Context Protocol (MCP)
and Groq. This Streamlit app lets you interact with GitHub repositories using
natural language queries.

## Features

- 🔍 Natural language queries for GitHub repositories
- 📊 Multiple query types:
  - Info: repository overview from its README
  - Issues: explore recent issues
  - Pull Requests: view recent merged PRs
  - Repository Activity: analyze code quality trends
  - Custom: ask anything about the repository
- 🎯 Interactive Streamlit UI (lavender pastel, minimal)
- 🔐 Secure API key handling (env vars or session-only sidebar input)
- 📈 Results in clean markdown with tables and GitHub links

## Prerequisites

- Python 3.10+
- Node.js / npx (for the `@modelcontextprotocol/server-github` MCP server)
- A GitHub Personal Access Token
- A Groq API Key

## Installation

1. Clone and enter the project:

bash
git clone https://github.com/Arindam200/awesome-ai-apps.git

cd mcp_ai_agents/github_mcp_agent


2. Install dependencies:

bash
pip install -r requirements.txt


3. Create a `.env` file in the project root:
   GROQ_API_KEY=your_groq_api_key
   GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
   # Optional: override the default model
   # GROQ_MODEL=openai/gpt-oss-20b

## Usage

bash
streamlit run main.py


Then open `http://localhost:8501`.

- If both keys are set in `.env`, the sidebar is hidden and you go straight to querying.
- If a key is missing, enter it in the sidebar (stored only for the session).
- Enter a repository (`owner/repo`), pick a query type, adjust the query, then
  click **Run Query**.

## Query Types

- **Info** — overview of the repository from its README
- **Issues** — recent issues
- **Pull Requests** — recent merged PRs
- **Repository Activity** — code quality / activity trends
- **Custom** — any question you like

## Security

- API keys come from `.env` or session-only sidebar input.
- Nothing sensitive is stored permanently.

## License

MIT — see the LICENSE file.