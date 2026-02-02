# 🤖 AI Agent Project

This repository contains a collection of AI-powered applications, each designed for a specific task, demonstrating various AI capabilities from web scraping to financial analysis and resume matching.

## ✨ Features

-   **Web Scraping Agent**: Intelligently scrapes website content using AI to extract desired information.
-   **Finance Agent**: Provides AI-driven assistance for financial analysis and tasks.
-   **Resume Job Matcher**: Matches resumes with job descriptions to find the best fit.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Each application has its own Python virtual environment and `requirements.txt`. Ensure you have Python 3.8+ installed.

### Installation

To set up an application locally, follow these steps:

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/your-username/Ai_agent.git
    cd Ai_agent
    ```

2.  **Navigate to the desired application's directory:**
    For example, for the Web Scraping Agent:
    ```bash
    cd LLM_APP/web_Scraping_agent
    ```

3.  **Activate the virtual environment:**
    -   **PowerShell (Windows):**
        ```bash
        . venv/Scripts/Activate.ps1
        ```
    -   **Bash/Zsh (Linux/macOS/Git Bash):**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    If you encounter issues with `playwright` (e.g., `NotImplementedError`), you might need to install its browser binaries:
    ```bash
    python -m playwright install
    ```

## 🛠️ Project Structure

```
d:\Ai_agent\
  - LLM_APP\
    - FInance_agent\
      - Xagent.py
      - requirements.txt
      - venv\
    - Resume_job_matcher\
      - main.py
      - README.md
      - requirements.txt
      - venv\
    - web_Scraping_agent\
      - local_scrapper.py
      - requirements.txt
      - venv\
  - README.md
```

## 🐛 Troubleshooting

### `NotImplementedError` with Playwright

If you encounter a `NotImplementedError` related to Playwright, it typically means the necessary browser binaries are not installed. Run the following command **after activating your virtual environment**:

```bash
python -m playwright install
```

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE.md file for details. (Note: You may need to create a `LICENSE.md` file.)
