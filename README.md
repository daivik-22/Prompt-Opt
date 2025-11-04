# PromptOpt - Interactive AI Prompt Optimizer

## ✨ Overview

PromptOpt is an interactive command-line interface (CLI) tool designed to help you analyze, optimize, and score your AI prompts. It provides an interactive experience, allowing you to experiment with different prompts and see their optimized variants and performance scores in real-time.

## 🚀 Features

*   **Interactive Interface:** A conversational CLI experience for easy prompt optimization.
*   **Prompt Analysis:** Get insights into your prompt's structure, potential issues, and estimated quality.
*   **Variant Generation:** Generate multiple optimized versions of your prompt using either a local heuristic engine or the powerful OpenAI API.
*   **Heuristic Scoring:** Evaluate the clarity, creativity, and overall quality of prompt variants.
*   **History Storage:** Automatically saves your prompt optimization history to a local SQLite database.
*   **Customizable Engine:** Choose between a local, fast engine or the OpenAI API for variant generation.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone <PromptOpt>
    cd promptopt_project
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 OpenAI API Key Setup

To use the AI engine (in this case OpenAI) for prompt optimization and creativity scoring, you need an AI API key.

1.  **Get your API Key:** Obtain your API key from the [OpenRouter website](https://openrouter.ai/models).

2.  **Create a `.env` file:** In the root of your project directory (`promptopt_project`), create a file named `.env`.

3.  **Add your API Key to `.env`:** Open the `.env` file and add the following line, replacing `your_actual_openai_api_key_here` with your key:
    ```
    AI_API_KEY="your_actual_ai_api_key_here"
    ```
    **Important:** Do not commit your `.env` file to version control! It contains sensitive information. The `.gitignore` file (which I will create next) will help prevent this.

## 🏃 How to Run

Start the interactive CLI by running:

```bash
python -m promptopt.cli
```

### Using the Interactive CLI

1.  **Welcome Screen:** You'll be greeted with the PromptOpt welcome screen.
2.  **Choose an Engine:** You'll be prompted to choose between `local` (fast, no API key needed) or `openai` (more powerful, requires API key).
3.  **Enter a Prompt:** Type the prompt you want to optimize and press Enter.
4.  **View Results:** The CLI will display:
    *   **Analysis:** Insights into your original prompt.
    *   **Generated Variants:** A table of optimized prompt versions with rationales.
    *   **Scores:** Clarity, creativity, and overall scores for each variant.
5.  **Continue or Exit:** You can enter another prompt or type `exit` or `quit` to close the application.

## 📂 Project Structure

```
promptopt_project/
├── promptopt/
│   ├── __init__.py
│   ├── cli.py              # Main interactive CLI application
│   ├── prompt_analyzer.py  # Analyzes prompt characteristics
│   ├── prompt_optimizer.py # Generates prompt variants
│   ├── prompt_scorer.py    # Scores prompt variants
│   ├── storage.py          # Handles SQLite database for history
│   └── utils.py            # Utility functions (e.g., save JSON/YAML)
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (e.g., OPENAI_API_KEY) - NOT committed to Git
└── README.md               # This file
```
