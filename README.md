# Financial Document Analyzer (Fixed & Improved Version)

## Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Getting Started
This project is a sophisticated **Financial Document Analyzer** built with **CrewAI**, designed to process and interpret financial reports. It leverages a multi-agent system to simulate a team of financial experts, including an analyst, a verifier, a risk assessor, and an investment advisor. The application is served through a **FastAPI** backend, allowing users to upload financial documents (e.g., quarterly reports) and receive a comprehensive analysis and investment recommendation.

This repository represents a significantly debugged and refactored version of the original codebase, featuring fixes for critical dependency conflicts, professionally rewritten AI prompts for high-quality analysis, and a stable, modern framework.

---
## 🐛 Bugs Found & Fixes Implemented

The original codebase was non-functional due to a combination of severe dependency conflicts, internal library bugs, and logical errors. The following is a summary of the debugging and refactoring process.

### 1. Dependency and Environment Resolution
The initial environment was completely broken due to a cascade of dependency conflicts.
* **Initial Conflicts:** Solved numerous direct version conflicts with packages like `onnxruntime`, `pydantic`, `click`, `packaging`, and `openai` by attempting to align versions.
* **Irreconcilable `crewai-tools` Conflict:** Discovered a fundamental, unresolvable conflict between `crewai==0.130.0` and all available versions of `crewai-tools` due to their mutually exclusive requirements for the `chromadb` and `langchain` libraries.
* **Strategic Solution - Framework Upgrade:** The only viable solution was to upgrade the core framework. The project was migrated from the buggy `crewai==0.130.0` to a modern, stable version (**`crewai==0.35.8`**). This resolved the deep-seated internal library bugs and dependency issues.
* **Surgical Dependency Removal:** To prevent future conflicts, the `crewai-tools` package was removed entirely. The required `SearchTool` was re-implemented manually in `tools.py` for a more stable, self-contained solution.

### 2. Code & Runtime Bug Fixes
After stabilizing the environment, numerous bugs in the Python code were addressed.
* **`ImportError`:** Fixed incorrect import paths for `Agent` class after library updates.
* **`NameError`:** Correctly initialized the LLM, fixing an error where the `llm` variable was referenced before assignment.
* **`AttributeError` & `ModuleNotFoundError`:** Refactored the custom tools to correctly inherit from LangChain's `BaseTool` and fixed incorrect instantiation and import paths in the `agents.py` and `task.py` files.
* **API Model `NotFoundError`:** Updated the requested OpenAI model from the deprecated `gpt-4-turbo` to the current `gpt-4o`.

### 3. Prompt Engineering
The initial prompts were sarcastic and designed to produce useless output.
* **Complete Rewrite:** All agent roles, goals, backstories, and task descriptions were rewritten to be professional, specific, and goal-oriented.
* **Logical Workflow:** The CrewAI tasks were structured with `context` passing to ensure a logical flow of information from the verifier to the analyst, and finally to the advisor.

---
## 🛠️ Setup & Installation

Follow these steps to set up and run the project locally.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/rprkash10/financial-analyzer-debug.git
    cd financial-analyzer-debug
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    This project uses a fully pinned and stable `requirements.txt` file to prevent dependency conflicts.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a `.env` file in the root directory and add your API keys. See the **API Key Configuration** section below for details.
    ```
    OPENAI_API_KEY="sk-..."
    SERPER_API_KEY="..."
    ```

---
## 🚀 Usage

1.  **Start the Server:**
    Run the `main.py` file to start the Uvicorn server. The `reload` flag is enabled, so the server will restart automatically when you save changes.
    ```bash
    python main.py
    ```

2.  **Access the API Documentation:**
    Open your web browser and navigate to the interactive documentation page:
    [**http://localhost:8000/docs**](http://localhost:8000/docs)

3.  **Run an Analysis:**
    * Click the `POST /analyze` endpoint to expand it.
    * Click the **"Try it out"** button.
    * Use the **"Choose File"** button to upload a financial document (e.g., a PDF report).
    * Click the blue **"Execute"** button to start the analysis.
    * The results will be displayed in the response body, and you can watch the agent's progress in the terminal where the server is running.

---
## 🔑 API Key Configuration

This application requires two API keys to function:

1.  **OpenAI API Key:** Used for the language model that powers the CrewAI agents.
    * **Important:** The OpenAI API is a paid service. You must have a valid API key with active billing and sufficient credits on your OpenAI account. The initial free trial credits often expire.
2.  **Serper API Key:** Used for the `SearchTool` to perform real-time internet searches. You can get a free key from [Serper.dev](https://serper.dev/).

Place these keys in a `.env` file in the project's root directory as shown in the setup instructions.
