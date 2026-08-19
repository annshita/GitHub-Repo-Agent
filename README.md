# GitHub Repo Agent

A GitHub repository exploration tool powered by the **Model Context Protocol (MCP)** and **Groq**.

This Streamlit app lets you interact with GitHub repositories using natural language queries.

## ✨ Features

- 🔍 Natural language queries for GitHub repositories
- 📊 Multiple query types:
  - **Info** — Repository overview from its README
  - **Issues** — Explore recent issues
  - **Pull Requests** — View recent merged pull requests
  - **Repository Activity** — Analyze code quality and activity trends
  - **Custom** — Ask anything about the repository
- 🎯 Interactive Streamlit UI with a minimal lavender-pastel design
- 🔐 Secure API key handling through environment variables or session-only input
- 📈 Clean Markdown responses with tables and GitHub links

## 🛠️ Prerequisites

- Python 3.10+
- Node.js / npx
- GitHub Personal Access Token
- Groq API Key

## 🚀 Installation

### 1. Clone the repository

    git clone https://github.com/Arindam200/awesome-ai-apps.git
    cd mcp_ai_agents/github_mcp_agent

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Configure environment variables

Create a `.env` file in the project root:

    GROQ_API_KEY=your_groq_api_key
    GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token

Optionally, override the default Groq model:

    GROQ_MODEL=openai/gpt-oss-20b

> Never commit your `.env` file or expose your API keys publicly.

## ▶️ Usage

Start the Streamlit application:

    streamlit run main.py

Then open:

    http://localhost:8501

### 🔑 API Key Handling

- If both keys are set in `.env`, the sidebar is hidden and you can start querying immediately.
- If a key is missing, enter it through the sidebar.
- Keys entered through the sidebar are stored only for the current session.

### 🔎 Running a Query

1. Enter a repository in the format `owner/repo`.
2. Select a query type.
3. Adjust the query if needed.
4. Click **Run Query**.
5. View the generated response.

## 📊 Query Types

| Query Type | Description |
|---|---|
| **Info** | Get an overview of the repository using its README |
| **Issues** | Explore recent repository issues |
| **Pull Requests** | View recently merged pull requests |
| **Repository Activity** | Analyze code quality and activity trends |
| **Custom** | Ask any question about the repository |

## 🔐 Security

The application supports two ways of providing API keys:

1. **Environment variables** using `.env`
2. **Session-only input** through the Streamlit sidebar

API keys entered through the sidebar are not stored permanently.

> Add `.env` to your `.gitignore` before pushing the project to GitHub.

## 📄 License

MIT License
